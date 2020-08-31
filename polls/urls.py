from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'polls'
urlpatterns = [
  path('',views.search,name='top'),
  path('detail/<int:category>/<str:id>', views.detail, name='detail'),
  path('users/<int:pk>/', views.users_detail, name='users_detail'),
  path('save/<int:category>/<str:id>', views.save, name='save'),
  path('login/',auth_views.LoginView.as_view(template_name='polls/login.html'),name='login'),
  path('logout/',auth_views.LogoutView.as_view(),name='logout'),
  path('signup/',views.signup, name='signup'),
]
