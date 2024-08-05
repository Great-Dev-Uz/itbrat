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

from project.filter import ProjectFilter
from project.models import CategoriyaProject, Project, FavoritesProject
from project.serializers import (
    CategoryProjectSerializer,
    ProjectsSerializer,
    ProjectSerializer,
    FavoritesProjectSerializer,
    FavoriteProjectSerializer,
)


class ProjectCategoryView(APIView):
    ''' Project Category '''

    @swagger_auto_schema(tags=['Project'], responses={200: CategoryProjectSerializer(many=True)})
    def get(self, request):
        instance = CategoriyaProject.objects.all().order_by('id')
        serializer = CategoryProjectSerializer(instance, many=True, context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectsView(APIView):
    ''' Project View '''
    renderer_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProjectFilter
    pagination_class = CustomPagination

    @swagger_auto_schema(
        tags=['Project'],
        manual_parameters=[
            openapi.Parameter('name', openapi.IN_QUERY, description="Filter by name", type=openapi.TYPE_STRING),
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Number of items per page", type=openapi.TYPE_INTEGER)
        ],
        responses={200: ProjectsSerializer(many=True)}
    )
    def get(self, request):
        queryset  = Project.objects.all().order_by('-id')
        filter_backend = DjangoFilterBackend()
        filtered_queryset = filter_backend.filter_queryset(request, queryset, self)

        # Apply pagination
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(filtered_queryset, request)
        serializer = ProjectsSerializer(page, many=True, context={'request': request, 'owner':request.user})
        return paginator.get_paginated_response(serializer.data)
    
    @swagger_auto_schema(tags=['Project'], request_body=ProjectSerializer)
    def post(self, request):
        serializers = ProjectSerializer(data=request.data, context={'request': request, 'owner': request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class ProjectView(APIView):
    ''' Project CRUD View '''
    renderer_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]

    @swagger_auto_schema(tags=['Project'], responses={200: ProjectsSerializer(many=True)})
    def get(self, request, pk):
        queryset = get_object_or_404(Project, id=pk)
        serializer = ProjectsSerializer(queryset, context={'request': request, 'owner': request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(tags=['Project'], request_body=ProjectSerializer)
    def put(self, request, pk):
        serializers = ProjectSerializer(instance=Project.objects.filter(id=pk)[0], context={"request": request}, data=request.data, partial=True,)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(tags=['Project'], responses={204:  'No Content'})
    def delete(self, request, pk):
        answer = Project.objects.get(id=pk)
        answer.delete()
        return Response({"message": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

class FavoritesProjectView(APIView):
    ''' Favorites Project View '''
    renderer_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsLogin]
    pagination_class = CustomPagination

    @swagger_auto_schema(
        tags=['Project'],
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('limit', openapi.IN_QUERY, description="Number of items per page", type=openapi.TYPE_INTEGER)
        ],
        responses={200: FavoritesProjectSerializer(many=True)}
    )
    def get(self, request):
        instance = FavoritesProject.objects.filter(owner=request.user).order_by('-id')
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(instance, request)
        serializer = FavoritesProjectSerializer(page, many=True, context={'request': request})
        return paginator.get_paginated_response(serializer.data)
    
    @swagger_auto_schema(tags=['Project'], request_body=FavoriteProjectSerializer)
    def post(self, request):
        serializers = FavoriteProjectSerializer(data=request.data, context={'request': request, 'owner': request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    

class FavoriteProjectView(APIView):
    ''' Favorite Project CRUD View '''
    renderer_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]    
    permission_classes = [IsLogin]

    @swagger_auto_schema(tags=['Project'], responses={200: FavoritesProjectSerializer(many=True)})
    def get(self, request, pk):
        queryset = get_object_or_404(FavoritesProject, project=pk)
        serializer = FavoritesProjectSerializer(queryset, context={'request': request, 'owner': request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(tags=['Project'], responses={204:  'No Content'})
    def delete(self, request, pk):
        try:
            favorite = FavoritesProject.objects.get(owner=request.user, project__id=pk)
            favorite.delete()
            return Response({"message": "Deleted successfully."}, status=status.HTTP_200_OK)
        except FavoritesProject.MultipleObjectsReturned:
            # Handle multiple instances returned, possibly log or raise an error
            return Response({"error": "Multiple favorite projects found. Contact support."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except FavoritesProject.DoesNotExist:
            return Response({"error": "Favorite project not found."}, status=status.HTTP_404_NOT_FOUND)