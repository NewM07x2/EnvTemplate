from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, extend_schema_view

from ..models import Category
from ..serializers.serializers import CategorySerializer
from ..service.category_service import CategoryService

# カテゴリ関連のビューを定義

def category_list(request):
    """
    カテゴリの一覧を表示するビュー。
    """
    pass

def category_detail(request, category_id):
    """
    特定のカテゴリの詳細を表示するビュー。
    """
    pass

@extend_schema_view(
    list=extend_schema(summary="すべてのカテゴリを一覧表示", tags=["categories"]),
    retrieve=extend_schema(summary="IDでカテゴリを取得", tags=["categories"]),
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    service = CategoryService()

    def list(self, request, *args, **kwargs):
        categories = self.service.get_all_categories()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        category = self.service.get_category(category_id=int(pk))
        serializer = self.get_serializer(category)
        return Response(serializer.data)