from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from authors.permissions import isOwner

from ..serializers.author_serializer import AuthorSerializer

User = get_user_model()


class AuthorsAPIv2ViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()

    http_method_names = [
        "get",
        "head",
        "options",
        "post",
        "patch",
        "delete",
    ]

    def get_queryset(self):
        pk = self.kwargs.get("pk", "")
        qs = User.objects.filter(pk=pk)

        return qs

    def get_object(self):
        pk = self.request.user.pk
        obj = get_object_or_404(
            self.get_queryset(),
            pk=pk,
        )

        self.check_object_permissions(request=self.request, obj=obj)

        return obj

    def get_permissions(self):
        if self.request.method == "POST" and self.request.user.id is None:
            return [AllowAny()]

        if self.request.method in ["PATCH", "DELETE"]:
            return [isOwner()]

        return super().get_permissions()
