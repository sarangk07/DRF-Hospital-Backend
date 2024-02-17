from rest_framework import permissions

class CustomPermission(permissions.BasePermission):
    def deny_admin(self, request, view):
        if request.user and request.user.is_staff:
            return False
        return True