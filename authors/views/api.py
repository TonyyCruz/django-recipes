from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
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
        user_id = self.request.user.pk or ""
        pk = self.kwargs.get("pk", user_id)
        qs = self.queryset.filter(pk=pk)

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

    @action(methods=["get"], detail=False)
    def me(self, request, *args, **kwargs):
        obj = self.get_queryset().first()
        serializer = self.get_serializer(
            instance=obj,
        )

        return Response(data=serializer.data)
