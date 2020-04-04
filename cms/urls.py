from django.urls import path

from . import views

app_name = 'cms'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/', views.UserCreate.as_view(), name='signup'),
    path('user/<int:pk>/update/', views.UserUpdate.as_view(), name='user_update'),
    path('user/<int:pk>/', views.UserDetail.as_view(), name='user_detail'),
    path('mypage/<int:pk>/', views.MyPage.as_view(), name='mypage'),
    path('project/create/', views.ProjectCreate.as_view(), name='project_create'),
    path('project/welcome/', views.project_welcome, name='project_welcome'),
    path('project/<int:pk>/', views.ProjectDetail.as_view(), name='project_detail'),
    path('project/<int:pk>/update/', views.ProjectUpdate.as_view(), name='project_update'),
    #path('project/<int:pk>/delete/', views.ProjectDelete.as_view(), name='project_delete'),
    path('project/<int:pk>/dashboard/', views.ProjectDashboard.as_view(), name='dashboard'),
    #path('project/<int:pk>/dashboard/commit/', views.ProjectDashboardCommit.as_view(), name='dashboard_commit'),
    #path('project/<int:pk>/dashboard/plan/', views.ProjectDashboardPlan.as_view(), name='dashboard_plan'),
]
