from .views import addView, ShowData, UpdateDetails, DeleteDetails
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordResetDoneView
from .views import SignInView, LoginView,  UserProfile
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path("add/", addView.as_view(), name="add-details"),
    path("index/", ShowData.as_view(), name="show"),
    path("<str:showType>/", views.sort_list, name="showsortlist"),

    path("update-details/<slug:slug>",
         UpdateDetails.as_view(), name="update-details"),
    path("delete-details/<slug:slug>",
         DeleteDetails.as_view(), name="delete-details"),


    # auth
    path("signin/", SignInView.as_view(), name="signin"),
    path("", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),

    # password rest generator
    path("password-reset", PasswordResetView.as_view(
        template_name="password-reset.html"), name="password-reset"),
    path("password-reset-done", PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
         name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/",
         PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete", PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
         name="password_reset_complete"),
    path("user-profile", UserProfile.as_view(), name="user-profile"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
