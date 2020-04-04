from django.contrib.auth.mixins import UserPassesTestMixin


class OnlyYouMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        return user.pk == self.kwargs['pk'] or user.is_superuser


class OnlyProjectMemberMixin(UserPassesTestMixin):
    raise_exception = True

    def test_func(self):
        user = self.request.user
        project_id_list = [project.id for project in user.project_set.all()]
        return self.kwargs['pk'] in project_id_list or user.is_superuser
