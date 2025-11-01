from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from ..service.about_service import AboutService
from ..models.about_model import About
from ..serializers.about_serializer import AboutSerializer

class AboutViewSet(viewsets.ModelViewSet):
    # GET /api/sample/about/ (list)
    # GET /api/sample/about/1/ (retrieve)
    # POST /api/sample/about/ (create)
    # PUT /api/sample/about/1/ (update)
    # DELETE /api/sample/about/1/ (destroy)

    queryset = About.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    service = AboutService()

    def get_serializer_class(self):
        if self.action == 'create':
            return AboutCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AboutUpdateSerializer
        return AboutSerializer

    # ----------------------------------------------------
    # ★ CRUDアクションを明示的に定義 (ModelViewSetの基本動作)
    # ----------------------------------------------------

    def get_list(self, request, *args, **kwargs):
        about = self.service.get_about(request)
        serializer = self.get_serializer(about, many=True)
        return Response(serializer.data)