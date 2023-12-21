from rest_framework.permissions import BasePermission

class IsNotAuthenticated(BasePermission):
    """
        Allows access only to non authenticated users.
    """
    def has_permission(self, request, view):
        return not request.user.is_authenticated



class IsStaff(BasePermission):
    """
        Allows access only to staff users.
    """
    def has_permission(self, request, view):
        return request.user.is_staff
