"""
Custom email backend for Gmail that handles SSL certificate issues on Windows.
"""
from __future__ import annotations

import ssl
import smtplib
from typing import Any
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
from django.core.mail.backends.base import BaseEmailBackend
from django.conf import settings

import json
from urllib.request import Request, urlopen


class GmailEmailBackend(SMTPBackend):
    """
    Custom SMTP backend that bypasses SSL certificate verification issues.
    Useful for development on Windows with Python 3.13+.
    """
    # Type hints to satisfy linters for parent class attributes
    host: str
    port: int
    username: str
    password: str
    use_tls: bool
    use_ssl: bool
    timeout: int | None
    connection: Any
    fail_silently: bool

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def open(self):
        """
        Open a connection to the email server.
        Override to handle SSL certificate verification issues.
        """
        if self.connection is not None:
            return False

        import sys
        # Use self.host which is already set by the SMTPBackend from Django settings
        print(f"[SMTP-DEBUG] Attempting connection to {self.host}:{self.port}", file=sys.stderr)
        print(f"[SMTP-DEBUG] Current Settings: TLS={self.use_tls}, SSL={self.use_ssl}", file=sys.stderr)

        try:
            # Force SSL for port 465 (SMTP_SSL), STARTTLS for port 587 (SMTP)
            if self.port == 465:
                print(f"[SMTP-DEBUG] Mode: SMTP_SSL (cert verification DISABLED)", file=sys.stderr)
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                self.connection = smtplib.SMTP_SSL(
                    self.host, self.port, timeout=self.timeout, context=context
                )
            else:
                print(f"[SMTP-DEBUG] Mode: Standard SMTP (STARTTLS if enabled)", file=sys.stderr)
                self.connection = smtplib.SMTP(
                    self.host, self.port, timeout=self.timeout
                )

            # For STARTTLS connections (usually port 587)
            if self.use_tls and self.port != 465:
                print("[SMTP-DEBUG] Enabling STARTTLS (cert verification DISABLED)", file=sys.stderr)
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                self.connection.starttls(context=context)

            if self.username:
                print(f"[SMTP-DEBUG] Login: {self.username} (Pass Len: {len(self.password)})", file=sys.stderr)
                self.connection.login(self.username, self.password)
            
            print("[SMTP-DEBUG] Connection and login successful", file=sys.stderr)
            return True
        except Exception as e:
            print(f"[SMTP-DEBUG] Connection/Login FAILED: {type(e).__name__}: {e}", file=sys.stderr)
            if self.fail_silently:
                return False
            raise e


class BrevoApiEmailBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        api_key = (
            getattr(settings, "BREVO_API_KEY", "")
            or getattr(settings, "SENDINBLUE_API_KEY", "")
            or ""
        ).strip()
        if not api_key:
            if self.fail_silently:
                return 0
            raise RuntimeError("BREVO_API_KEY is not configured.")

        sent = 0
        for msg in email_messages:
            if not getattr(msg, "to", None):
                continue

            from_email = (getattr(msg, "from_email", "") or getattr(settings, "DEFAULT_FROM_EMAIL", "") or "").strip()
            if not from_email:
                from_email = "no-reply@example.com"

            payload: dict[str, object] = {
                "sender": {"email": from_email},
                "to": [{"email": e} for e in (msg.to or []) if e],
                "subject": getattr(msg, "subject", "") or "",
            }

            text_body = getattr(msg, "body", "") or ""
            html_body = None
            alternatives = getattr(msg, "alternatives", None)
            if alternatives:
                for body, mimetype in alternatives:
                    if mimetype == "text/html":
                        html_body = body
                        break

            if html_body is not None:
                payload["htmlContent"] = str(html_body)
                if text_body:
                    payload["textContent"] = str(text_body)
            else:
                payload["textContent"] = str(text_body)

            body = json.dumps(payload).encode("utf-8")
            req = Request(
                "https://api.brevo.com/v3/smtp/email",
                data=body,
                headers={
                    "api-key": api_key,
                    "Content-Type": "application/json",
                    "accept": "application/json",
                },
                method="POST",
            )

            try:
                with urlopen(req, timeout=int(getattr(settings, "EMAIL_TIMEOUT", 10) or 10)) as resp:
                    status = getattr(resp, "status", 200)
                    if status >= 400:
                        raw = resp.read().decode("utf-8", errors="replace")
                        raise RuntimeError(f"Brevo API error {status}: {raw}")
            except Exception:
                if self.fail_silently:
                    continue
                raise

            sent += 1

        return sent
