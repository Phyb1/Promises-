from django.urls import path
from . import views

app_name = "promises"

urlpatterns = [
    path("", views.PromiseListView.as_view(), name="list"),
    path("search/", views.PromiseSearchView.as_view(), name="search"),
    path("tag/<str:group>/<slug:slug>/", views.PromiseByTagView.as_view(), name="by_tag"),
    path("<int:pk>/", views.PromiseDetailView.as_view(), name="detail"),
]
