from django.core.mail import send_mail

from django.shortcuts import get_object_or_404
from django.db.models import Q

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.renderers import UserRenderers
from utils.permissions import IsLogin
from utils.response import success_response, success_created_response, bad_request_response

from authen.models import CustomUser
from authen.serializers import UserInformationSerializer

from chat.models import Conversation, ChatMessage, Feedback, Question
from chat.serializers import (
    ConversationListSerializer,
    ConversationSerializer,
    MessagesSerializer,
    MessageListSerializer
)






class StartConversationView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]
    filter_backends = [DjangoFilterBackend]
    serializer_class = UserInformationSerializer
    filterset_fields = ["email",]
    def get(self, request):
        search_email = request.query_params.get("email")
        if not search_email:
            return Response({"error": "Please provide an email for search."}, status=status.HTTP_400_BAD_REQUEST)

        queryset = CustomUser.objects.filter(email__icontains=search_email)
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return success_response(serializer.data)

    @swagger_auto_schema(
            request_body=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                }
            )
    )
    def post(self, request):
        data = request.data

        email = data['email']
        try:
            participant = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Вы не можете общаться с пользователем, которого не существует.'})
        conversation = Conversation.objects.filter(Q(initiator=request.user, receiver=participant) |
                                                   Q(initiator=participant, receiver=request.user))
        if conversation.exists():
            return Response({"message": "Разговор уже существует"}, status=status.HTTP_200_OK)
        else:
            conversation = Conversation.objects.create(initiator=request.user, receiver=participant)
            return Response(ConversationSerializer(instance=conversation).data, status=status.HTTP_200_OK)


class GetConversationView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]
    filterset_fields = ["text"]

    def get(self, request, convo_id):
        text = request.query_params.get("text", None)
        if text:
            conversation = ChatMessage.objects.select_related('conversation_id').filter(
                Q(conversation_id=convo_id), Q(text__icontains=text)
            )
            page = self.paginate_queryset(conversation)
            serializer = MessageListSerializer(conversation, many=True, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)

        conversation = get_object_or_404(Conversation, id=convo_id)
        messages = conversation.message_set.all()  # Retrieve all messages for the conversation
        # page = self.paginate_queryset(messages)
        serializer = ConversationSerializer(conversation, context={'request': request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetConversationView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]
    filterset_fields = ["text"]

    def get(self, request, convo_id):
        conversation = get_object_or_404(Conversation, id=convo_id)

        messages = conversation.messages.all()  # Retrieve all messages for the conversation
        # page = self.paginate_queryset(messages)

        serializer = ConversationSerializer(conversation, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, convo_id):
        conversation = get_object_or_404(Conversation, id=convo_id)
        serializer = MessagesSerializer(data=request.data, context={
            "request": request.user,
            "conversation": conversation
        })
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConversationView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    def get(self, request):

        conversation_list = Conversation.objects.filter(Q(initiator=request.user.id) |
                                                        Q(receiver=request.user.id))
        serializer = ConversationListSerializer(instance=conversation_list, many=True, context={"request": request})
        # serializer = super().page(conversation_list, ConversationListSerializer, request)

        return Response(serializer.data, status=status.HTTP_200_OK)



class FeedbackView(APIView):

    @swagger_auto_schema(
        tags=['Other'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description='name'),
                'email': openapi.Schema(type=openapi.FORMAT_EMAIL, description='email'),
            }
        )
    )
    def post(self, request):
        name = request.data.get('name', '')
        email = request.data.get('email', '')
        
        if not name:
            return Response({'message': 'Имя не может быть пустым'}, status=status.HTTP_400_BAD_REQUEST)
        if not email:
            return Response({'message': 'Электронная почта не может быть пустой'}, status=status.HTTP_400_BAD_REQUEST)

        feedback = Feedback(name=name, email=email)
        feedback.save()

        subject = 'Обратная связь'
        message = f'Имя: {name}\nEmail: {email}'
        from_email = 'ItBratrf@yandex.ru'  # Your from email
        recipient_list = ['ItBratrf@yandex.ru']  # Recipient list

        try:
            send_mail(subject, message, from_email, recipient_list)
            return Response({'message': 'Получен отзыв и отправлено электронное письмо'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'Не удалось отправить электронное письмо', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuestionView(APIView):

    @swagger_auto_schema(
        tags=['Other'],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'text': openapi.Schema(type=openapi.TYPE_STRING, description='text'),
            }
        )
    )
    def post(self, request):
        text = request.data.get('text', '')
        if not text:
            return Response({'message': 'Text cannot be empty'}, status=status.HTTP_400_BAD_REQUEST)
        concat_user = Question(text=text)
        concat_user.save()
         # Send email
        subject = 'Получен новый вопрос'
        message = f'Вопрос: {text}'
        from_email = 'ItBratrf@yandex.ru'  # Your from email
        recipient_list = ['ItBratrf@yandex.ru']  # Recipient list

        try:
            send_mail(subject, message, from_email, recipient_list)
            return Response({'message': 'Вопрос получен и электронное письмо отправлено'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': 'Не удалось отправить электронное письмо', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)