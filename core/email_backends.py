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

        try:
            if self.use_ssl:
                self.connection = smtplib.SMTP_SSL(
                    self.host, self.port, timeout=self.timeout
                )
            else:
                self.connection = smtplib.SMTP(
                    self.host, self.port, timeout=self.timeout
                )

            # For TLS connections, create a context that doesn't verify certificates
            # This is needed for Windows/Python 3.13+ SSL issues
            if self.use_tls:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                self.connection.starttls(context=context)

            if self.username:
                self.connection.login(self.username, self.password)
            return True
        except Exception as e:
            if self.fail_silently:
                return False
            raise
