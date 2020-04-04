from django.shortcuts import render, resolve_url
from django.contrib.auth import login, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    LoginView, LogoutView,
)
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView, UpdateView, DeleteView,
)

from .forms import (
    EmailAuthenticationForm, UserCreateForm, UserUpdateForm,
    ProjectCreateForm, ProjectUpdateForm,
)
from .models import (
    Project,
)
from .mixins import (
    OnlyYouMixin, OnlyProjectMemberMixin,
)

UserModel = get_user_model()


def index(request):
    return render(request, 'cms/index.html', {})


def about(request):
    return render(request, 'cms/about.html', {})


def contact(request):
    return render(request, 'cms/contact.html', {})


class Login(LoginView):
    form_class = EmailAuthenticationForm
    template_name = 'registration/login.html'


class Logout(LogoutView):
    template_name = 'cms/index.html'


class UserCreate(CreateView):
    form_class = UserCreateForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        self.object = user
        return HttpResponseRedirect(self.get_success_url())


class UserDetail(DetailView):
    model = UserModel
    template_name = 'user/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class UserUpdate(OnlyYouMixin, UpdateView):
    model = UserModel
    form_class = UserUpdateForm
    template_name = 'user/user_update.html'

    def get_success_url(self):
        return resolve_url('cms:user_detail', pk=self.kwargs['pk'])


class MyPage(LoginRequiredMixin, OnlyYouMixin, DetailView):
    model = UserModel
    template_name = 'user/mypage.html'


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectCreateForm
    template_name = 'project/project_create.html'
    success_url = reverse_lazy('cms:project_welcome')

    def form_valid(self, form):
        project = form.save(commit=False)
        project.members.add(self.request.user)
        project.save()
        return HttpResponseRedirect(self.get_success_url())


@login_required
def project_welcome(request):
    return render(request, 'project/project_welcome.html', {})


class ProjectUpdate(LoginRequiredMixin, OnlyProjectMemberMixin, UpdateView):
    model = Project
    template_name = 'project/project_update.html'
    form_class = ProjectUpdateForm

    def get_success_url(self):
        return resolve_url('cms:project_detail', pk=self.kwargs['pk'])


class ProjectDetail(DetailView):
    model = Project
    template_name = 'project/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context


class ProjectDashboard(LoginRequiredMixin, OnlyProjectMemberMixin, DetailView):
    model = Project
    template_name = 'project/dashboard.html'

