from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
import traceback


def _safe_add_message(request, level_func, text: str) -> None:
    """Add a Django message if the messages framework is available.

    This prevents MessageFailure crashes when MessageMiddleware isn't installed
    (e.g., running with a different settings module / environment).
    """
    try:
        level_func(request, text)
    except Exception:
        # Intentionally swallow to avoid turning session timeout into a 500.
        return


class SessionTimeoutMiddleware:
    """Auto-logout after 10 minutes of inactivity (Module 1)."""

    TIMEOUT_SECONDS = 60 * 10

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        safe_prefixes = (
            reverse("login"),
            reverse("logout"),
            reverse("password_reset"),
            "/accounts/reset/",
            "/accounts/activate/",
            "/admin/",
            "/static/",
        )

        if user and user.is_authenticated and not request.path.startswith(safe_prefixes):
            last = request.session.get("last_activity")
            now_ts = int(timezone.now().timestamp())

            if last is not None and (now_ts - int(last)) > self.TIMEOUT_SECONDS:
                logout(request)
                request.session.flush()
                _safe_add_message(request, messages.info, "You have been logged out due to inactivity.")
                return redirect("login")

            request.session["last_activity"] = now_ts

        return self.get_response(request)


class ForcePasswordChangeMiddleware:
    """Redirect users to set a new password if they are flagged for first-login reset."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)
        if user and user.is_authenticated and getattr(user, "must_change_password", False):
            set_password_path = reverse("set_password")
            safe_prefixes = (
                set_password_path,
                reverse("logout"),
                reverse("login"),
                "/admin/",
                "/static/",
            )
            if not request.path.startswith(safe_prefixes):
                return redirect("set_password")

        return self.get_response(request)


class ExceptionLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            return self.get_response(request)
        except Exception:
            print("=== UNHANDLED EXCEPTION ===", flush=True)
            try:
                print(f"{request.method} {request.get_full_path()}", flush=True)
            except Exception:
                pass
            print(traceback.format_exc(), flush=True)
            raise
