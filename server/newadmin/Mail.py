from django.core.mail import EmailMessage
from django.conf import settings

import ssl



def send_email(recipient, subject, message):
    subject =subject
    message = message
    sender = settings.EMAIL_HOST_USER
    recipient = recipient
    
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=sender,
        to=[recipient],
        connection=None,
    )

    email.connection = get_ssl_connection() # Use an SSL connection to send the email

    email.send(fail_silently=False) 
    return True

def get_ssl_connection():
    from django.core.mail.backends.smtp import EmailBackend

    backend = EmailBackend(
        host=settings.EMAIL_HOST,
        port=settings.EMAIL_TLS_PORT,
        username=settings.EMAIL_HOST_USER,
        password=settings.EMAIL_HOST_PASSWORD,
        use_tls= settings.EMAIL_USE_TLS,
        use_ssl= settings.EMAIL_USE_SSL,
        ssl_context = settings.EMAIL_SSL_CONTEXT,
    )

    return backend
