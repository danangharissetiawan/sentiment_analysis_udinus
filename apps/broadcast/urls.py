from django import urls

from . import views

app_name = 'broadcast'

urlpatterns = [
    urls.path('', views.broadcast, name='home'),
    urls.path('api/docs/', views.api_docs, name='docs'),
    urls.path('api/broadcast/<str:email>/', views.BroadcastApiView.as_view(), name='api'),
]