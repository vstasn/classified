from django.views.generic.edit import CreateView
from django.contrib import messages, auth
from django.shortcuts import redirect
from django.urls import reverse_lazy


def login_view(request):
    """login"""
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = auth.authenticate(request, username=username, password=password)
    if user is not None:
        auth.login(request, user)
    else:
        messages.error(request, "Username or password is not correct")
    return redirect("/")


class UserCreate(CreateView):
    """user register"""
    form_class = auth.forms.UserCreationForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, "User created, sign in, please")

        return super(CreateView, self).form_valid(form)
