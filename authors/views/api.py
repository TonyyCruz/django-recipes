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

    def update(self, request, *args, **kwargs):
        print("update call >>>")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        print("partial_update call >>>")
        return super().partial_update(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        `.dispatch()` is pretty much the same as Django's regular dispatch,
        but with extra hooks for startup, finalize, and exception handling.
        """
        self.args = args
        self.kwargs = kwargs
        request = self.initialize_request(request, *args, **kwargs)
        self.request = request
        self.headers = self.default_response_headers  # deprecate?

        try:
            self.initial(request, *args, **kwargs)

            # Get the appropriate handler method
            if request.method.lower() in self.http_method_names:
                handler = getattr(
                    self, request.method.lower(), self.http_method_not_allowed
                )
            else:
                handler = self.http_method_not_allowed

            response = handler(request, *args, **kwargs)

        except Exception as exc:
            response = self.handle_exception(exc)

        self.response = self.finalize_response(
            request, response, *args, **kwargs
        )
        return self.response

    def initial(self, request, *args, **kwargs):
        """
        Runs anything that needs to occur prior to calling the method handler.
        """
        self.format_kwarg = self.get_format_suffix(**kwargs)

        # Perform content negotiation and store the accepted info on the request
        neg = self.perform_content_negotiation(request)
        request.accepted_renderer, request.accepted_media_type = neg

        # Determine the API version, if versioning is in use.
        version, scheme = self.determine_version(request, *args, **kwargs)
        request.version, request.versioning_scheme = version, scheme

        # Ensure that the incoming request is permitted
        self.perform_authentication(request)
        self.check_permissions(request)
        self.check_throttles(request)
