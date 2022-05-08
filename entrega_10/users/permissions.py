from rest_framework.permissions import BasePermission
        
class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        
        if request.method == 'GET':
            if (request.user.is_authenticated and request.user.is_admin == True):
                return True

            return False

        return False