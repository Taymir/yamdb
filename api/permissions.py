from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated, BasePermission


# class IsAuthorOrAdminOrModerator(BasePermission):
#     def has_permission(self):
#         pass
#
#     def has_object_permission(self, request, view, obj):
#         if request.user and request.user.is_authenticated:
#