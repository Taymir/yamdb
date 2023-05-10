from rest_framework.permissions import SAFE_METHODS, BasePermission


# class IsAuthorOrAdminOrModerator(BasePermission):
#     def has_permission(self):
#         pass
#
#     def has_object_permission(self, request, view, obj):
#         if request.user and request.user.is_authenticated:
#
class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            (
                    request.user.is_staff or
                    request.user.is_superuser or
                    getattr(request.user, 'role', '') == 'admin'
            )
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            (
                request.user.is_staff or
                request.user.is_superuser or
                getattr(request.user, 'role', '') == 'admin'
            )
        )


class IsAuthorOrModeratorOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user == obj.author or
            request.user.is_staff or
            request.user.is_superuser or
            getattr(request.user, 'role', '') == 'moderator' or
            getattr(request.user, 'role', '') == 'admin'
        )
