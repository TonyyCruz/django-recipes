from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

app_name = "authors"

authors_API_v2_router = SimpleRouter()
authors_API_v2_router.register(
    prefix="api/v2",
    viewset=views.AuthorsAPIv2ViewSet,
    basename="author-api",
)

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("register/create/", views.register_create, name="register_create"),
    path("login/", views.login_view, name="login"),
    path("login/create/", views.login_create, name="login_create"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/<int:id>/", views.ProfileView.as_view(), name="profile"),
    path(
        "dashboard/recipe/create/",
        views.DashboardRecipe.as_view(),
        name="dashboard_recipe_create",
    ),
    path(
        "dashboard/recipe/<int:id>/edit/",
        views.DashboardRecipe.as_view(),
        name="dashboard_recipe_edit",
    ),
    path(
        "dashboard/recipe/<int:id>/delete/",
        views.DashboardRecipeDelete.as_view(),
        name="dashboard_recipe_delete",
    ),
]

urlpatterns += authors_API_v2_router.urls
