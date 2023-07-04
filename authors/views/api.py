from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from ..serializers.author_serializer import AuthorSerializer


class AuthorsAPIv2ViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "head", "options", "post", "patch", "delete"]

    def get_queryset(self):
        User = get_user_model()
        qs = User.objects.filter(pk=self.request.user.pk)

        return qs

    def get_permissions(self):
        if self.request.method == "POST" and self.request.user.id is None:
            self.permission_classes = [AllowAny]

        return super().get_permissions()
