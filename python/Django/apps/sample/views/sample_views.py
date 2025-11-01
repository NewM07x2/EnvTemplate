from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from drf_spectacular.utils import extend_schema, extend_schema_view

from ..models import Sample
from ..serializers.sample_serializer import (
    SampleSerializer,
    SampleCreateSerializer,
    SampleUpdateSerializer
)
from ..service.sample_service import SampleService

# サンプル関連のビューを定義

# def sample_list(request):
#     """
#     サンプルの一覧を表示するビュー。
#     """
#     pass

# def sample_detail(request, sample_id):
#     """
#     特定のサンプルの詳細を表示するビュー。
#     """
#     pass

@extend_schema_view(
    list=extend_schema(summary="すべてのサンプルを一覧表示", tags=["samples"]),
    retrieve=extend_schema(summary="IDでサンプルを取得", tags=["samples"]),
    create=extend_schema(summary="新しいサンプルを作成", tags=["samples"]),
    update=extend_schema(summary="サンプルを更新", tags=["samples"]),
    partial_update=extend_schema(summary="サンプルを部分的に更新", tags=["samples"]),
    destroy=extend_schema(summary="サンプルを削除", tags=["samples"]),
)
class SampleViewSet(viewsets.ModelViewSet):
    queryset = Sample.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    service = SampleService()

    def get_serializer_class(self):
        if self.action == 'create':
            return SampleCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return SampleUpdateSerializer
        return SampleSerializer

    def list(self, request, *args, **kwargs):
        skip = int(request.query_params.get('skip', 0))
        limit = int(request.query_params.get('limit', 100))
        published_only = request.query_params.get('published', 'false').lower() == 'true'

        samples = self.service.get_samples(skip=skip, limit=limit, published_only=published_only)
        serializer = self.get_serializer(samples, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        sample = self.service.get_sample(sample_id=int(pk))

        if not request.user.is_authenticated or request.user.id != sample.author_id:
            self.service.increment_views(sample_id=int(pk))

        serializer = self.get_serializer(sample)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sample = self.service.create_sample(
            author_id=request.user.id,
            **serializer.validated_data
        )
        output_serializer = SampleSerializer(sample)

        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sample = self.service.update_sample(
            sample_id=int(pk),
            user_id=request.user.id,
            is_staff=request.user.is_staff,
            **serializer.validated_data
        )
        output_serializer = SampleSerializer(sample)

        return Response(output_serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        self.service.delete_sample(
            sample_id=int(pk),
            user_id=request.user.id,
            is_staff=request.user.is_staff
        )
        return Response(
            {'message': 'サンプルが正常に削除されました'},
            status=status.HTTP_204_NO_CONTENT
        )

    @extend_schema(
        summary="著者によるサンプルの取得",
        tags=["samples"],
    )
    @action(detail=False, methods=['get'])
    def by_author(self, request):
        author_id = int(request.query_params.get('author_id'))
        skip = int(request.query_params.get('skip', 0))
        limit = int(request.query_params.get('limit', 100))

        samples = self.service.get_samples_by_author(
            author_id=author_id,
            skip=skip,
            limit=limit
        )
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="サンプルの検索",
        tags=["samples"],
    )
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        samples = self.service.search_samples(query=query)
        serializer = SampleSerializer(samples, many=True)
        return Response(serializer.data)