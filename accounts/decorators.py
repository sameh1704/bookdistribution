from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden
from functools import wraps

def custom_permission_required(*permissions):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return HttpResponseForbidden("You must be logged in to access this page.")
            
            if request.user.is_admin:
                return view_func(request, *args, **kwargs)
            
            for permission in permissions:
                if getattr(request.user, permission, False):
                    return view_func(request, *args, **kwargs)
            
            return HttpResponseForbidden("نأسف لذلك ولكن هذا المستخدم لا يمتلك صلاحية الوصول الى هذه الصفحة شكرا لتفهمك مع تحيات مدارس المنار الخاصة للغات .")
        return _wrapped_view
    return decorator



from django.contrib.auth.mixins import UserPassesTestMixin

class CustomPermissionMixin(UserPassesTestMixin):
    permissions = []

    def test_func(self):
        if self.request.user.is_admin:
            return True
        return any(getattr(self.request.user, perm, False) for perm in self.permissions)
    

      
