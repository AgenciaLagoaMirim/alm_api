from rest_framework.permissions import IsAuthenticated, BasePermission


class IsInGroupGeneralOrReadyOnly(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True

        return request.user.groups.filter(name="general").exists()

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        return obj.groups.filter(name="general").exists()
