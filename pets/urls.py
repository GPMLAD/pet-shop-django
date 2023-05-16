from django.urls import path
from .views import PetViews, PetDetailsViews

urlpatterns = [
    path("pets/", PetViews.as_view()),
    path("pets/<int:pet_id>/", PetDetailsViews.as_view()),
]
