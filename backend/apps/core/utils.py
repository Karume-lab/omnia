from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_templated_email(subject, to_email, template_name, context):
    """
    Sends an email using a Django HTML template and an auto-generated plain-text fallback.

    :param subject: Email subject
    :param to_email: A single email address or list of addresses
    :param template_name: Path to the HTML email template
    :param context: Dictionary to render the template with
    """
    # Render the HTML content
    html_content = render_to_string(template_name, context)

    # Auto-generate plain text version by stripping HTML
    text_content = strip_tags(html_content)

    # Build and send the email
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email] if isinstance(to_email, str) else to_email,
    )
    email.attach_alternative(html_content, "text/html")
    email.send()
