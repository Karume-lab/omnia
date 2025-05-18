from django.urls import include, path
from apps.users.views import CustomJWTTokenCreateView


app_name = "users"


urlpatterns = [
    path("auth/jwt/create/", CustomJWTTokenCreateView.as_view(), name="token_create"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
