from django.urls import path

from .views import SubmitData, DetailData

urlpatterns = [
    path('submit_data/', SubmitData.as_view()),
    path('submit_data/<int:id>', DetailData.as_view()),
]