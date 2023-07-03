from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet

from ..serializers.author_serializer import AuthorSerializer


class AuthorsAPIv2ViewSet(ModelViewSet):
    queryset = User.objects.get_published()
    serializer_class = AuthorSerializer
    # pagination_class = RecipeAPIv2Pagination
    # permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ["get", "head", "options", "post", "patch", "delete"]
