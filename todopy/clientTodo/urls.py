from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'clientTodo'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/add-task/', views.create_task, name='add-task'),
    path('<int:id>', views.delete_card, name='delete'),
    path('add-card/', views.add_card, name='add-card'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


