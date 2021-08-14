from django.urls import path
from . import views

app='apppages'

urlpatterns = [
    path('<int:page_id>/', views.page, name="page"),
    
]