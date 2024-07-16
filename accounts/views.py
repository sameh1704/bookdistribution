from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

class CustomLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    
    def get_success_url(self):
        return reverse_lazy('store:home')  # أو أي صفحة افتراضية أخرى
    



from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('login')