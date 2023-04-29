from rest_framework.permissions import SAFE_METHODS, IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated, BasePermission


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
            request.user.is_staff
        )


class IsAuthorOrModeratorOrAdminOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS or
            request.user.role == 'moderator' or
            request.user.role == 'admin' or
            request.user == obj.author
        )
