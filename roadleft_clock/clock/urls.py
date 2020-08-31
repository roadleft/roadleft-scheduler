
from django.urls import path, include
from . import views

urlpatterns = [
    path('<ttype>/<int:pk>/', views.notify)
]
