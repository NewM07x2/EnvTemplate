from rest_framework import viewsets
from ..models.about_model import About
from ..serializers.about_serializer import AboutSerializer

class AboutViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = About.objects.all()
    serializer_class = AboutSerializer