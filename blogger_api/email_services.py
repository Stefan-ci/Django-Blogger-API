import ssl
from django.utils.functional import cached_property
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend


class DevEmailBackend(SMTPBackend):
    """
    Email backend to use (only) in dev mode (it doesn't check hostname while creating connection).
    While being in dev mode Django doesn't allow email sending directly to email address (only console backend works).
    To override this and to be able to send actual email in dev mode, use this as email backend.

    Args:
        SMTPBackend (_type_): A wrapper that manages the SMTP network connection.

    Returns:
        SSLContext: SSLContext instance
    """
    @cached_property
    def ssl_context(self):
        if self.ssl_certfile or self.ssl_keyfile:
            ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.load_cert_chain(self.ssl_certfile, self.ssl_keyfile)
            return ssl_context
        else:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            return ssl_context
