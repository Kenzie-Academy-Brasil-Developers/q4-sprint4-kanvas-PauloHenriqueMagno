from rest_framework.permissions import BasePermission
        
class IsInstructor(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['POST', 'PATCH', 'DELETE', 'PUT']:
            if (request.user.is_authenticated and request.user.is_admin == True):
                return True
                    
        if request.method == 'GET':
            return True

        return False