from djoser import email
from django.conf import settings


class CustomPasswordResetEmail(email.PasswordResetEmail):
    template_name = "accounts/templates/accounts/email/password_reset.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["protocol"] = "https" if self.request.is_secure() else "http"
        context["domain"] = settings.DOMAIN
        context["site_name"] = settings.SITE_NAME

        return context
