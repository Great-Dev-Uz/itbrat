from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from utils.permissions import IsLogin
from utils.renderers import UserRenderers
from utils.pagination import CustomPagination

from resume.filter import ResumetFilter
from resume.models import Heading, ResumeModel, FavoritesResume
from resume.serializers import (
    HeadingSerializer,
    ResumesSerializer,
    ResumeSerializer,
    FavroitesResumeSerializer,
    FavroiteResumeSerializer,
)


class HeadingView(APIView):

    @swagger_auto_schema(tags=['Resume'], responses={200: HeadingSerializer(many=True)})
    def get(self, request):
        instance = Heading.objects.all().order_by('id')
        serializer = HeadingSerializer(instance, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResumesView(APIView):
    renderer_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ResumetFilter
    pagination_class = CustomPagination

    @swagger_auto_schema(
        tags=['Resume'],
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Filter by name", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Number of items per page", type=openapi.TYPE_INTEGER)
        ],
        responses={200: ResumesSerializer(many=True)}
    )
    def get(self, request):
        queryset  = ResumeModel.objects.all().order_by('-id')
        filter_backend = DjangoFilterBackend()
        filtered_queryset = filter_backend.filter_queryset(request, queryset, self)

        # Apply pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(filtered_queryset, request)
        serializer = ResumesSerializer(page, many=True, context={'request': request, 'owner':request.user})
        return paginator.get_paginated_response(serializer.data)
    
    @swagger_auto_schema(tags=['Resume'], request_body=ResumeSerializer)
    def post(self, request):
        serializers = ResumeSerializer(data=request.data, context={'request': request, 'owner': request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ResumeView(APIView):
    renderer_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(tags=['Resume'], responses={200: ResumesSerializer(many=True)})
    def get(self, request, pk):
        queryset = get_object_or_404(ResumeModel, id=pk)
        serializer = ResumesSerializer(queryset, context={'request': request, 'owner': request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(tags=['Resume'], request_body=ResumeSerializer)
    def put(self, request, pk):
        serializers = ResumeSerializer(instance=ResumeModel.objects.filter(id=pk)[0], context={"request": request}, data=request.data, partial=True,)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['Resume'], responses={204:  'No Content'})
    def delete(self, request, pk):
        answer = ResumeModel.objects.get(id=pk)
        answer.delete()
        return Response({"message": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class FavoritesResumeView(APIView):
    renderer_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        tags=['Resume'],
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Number of items per page", type=openapi.TYPE_INTEGER)
        ],
        responses={200: FavroitesResumeSerializer(many=True)}
    )
    def get(self, request):
        instance = FavoritesResume.objects.filter(owner=request.user).order_by('-id')
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(instance, request)
        serializer = FavroitesResumeSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    
    @swagger_auto_schema(tags=['Resume'], request_body=FavroiteResumeSerializer)
    def post(self, request):
        serializers = FavroiteResumeSerializer(data=request.data, context={'request': request, 'owner': request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FavoriteResumeView(APIView):
    renderer_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]    
    permission_classes = [IsLogin]

    @swagger_auto_schema(tags=['Resume'], responses={200: FavroitesResumeSerializer(many=True)})
    def get(self, request, pk):
        queryset = get_object_or_404(FavoritesResume, resume=pk)
        serializer = FavroitesResumeSerializer(queryset, context={'request': request, 'owner': request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=['Resume'], responses={204:  'No Content'})
    def delete(self, request, pk):
        favorite = FavoritesResume.objects.get(resume=pk)
        favorite.delete()
        return Response({"message": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
