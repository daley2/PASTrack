"""
Custom email backend for Gmail that handles SSL certificate issues on Windows.
"""
import ssl
import smtplib
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend


class GmailEmailBackend(SMTPBackend):
    """
    Custom SMTP backend that bypasses SSL certificate verification issues.
    Useful for development on Windows with Python 3.13+.
    """

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
        print(f"[SMTP-DEBUG] Attempting connection to {self.host}:{self.port} (TLS={self.use_tls}, SSL={self.use_ssl})", file=sys.stderr)

        try:
            # Force SMTP for port 587 (TLS), SMTP_SSL for port 465 (SSL)
            if self.port == 465:
                print(f"[SMTP-DEBUG] Using SMTP_SSL for port {self.port}", file=sys.stderr)
                self.connection = smtplib.SMTP_SSL(
                    self.host, self.port, timeout=self.timeout
                )
            else:
                print(f"[SMTP-DEBUG] Using standard SMTP for port {self.port}", file=sys.stderr)
                self.connection = smtplib.SMTP(
                    self.host, self.port, timeout=self.timeout
                )

            # For TLS connections, create a context that doesn't verify certificates
            # This is needed for Windows/Python 3.13+ SSL issues
            if self.use_tls:
                print("[SMTP-DEBUG] Enabling STARTTLS with custom SSL context (cert verification DISABLED)", file=sys.stderr)
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                self.connection.starttls(context=context)

            if self.username:
                print(f"[SMTP-DEBUG] Attempting login for {self.username} (Password Length: {len(self.password)})", file=sys.stderr)
                self.connection.login(self.username, self.password)
            
            print("[SMTP-DEBUG] Connection and login successful", file=sys.stderr)
            return True
        except Exception as e:
            print(f"[SMTP-DEBUG] Connection/Login FAILED: {e}", file=sys.stderr)
            if self.fail_silently:
                return False
            raise e
