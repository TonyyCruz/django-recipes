from rest_framework import permissions


class isOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user

    # def has_permission(self, request, view):
    #     try:
    #         obj = view.get_queryset().first()
    #         auth_id = view.request.auth["user_id"]
    #         query_id = obj.pk

    #         return auth_id == query_id

    #     except ValueError:
    #         return False
