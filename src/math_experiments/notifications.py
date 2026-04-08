"""Email notification support for math experiments."""

from __future__ import annotations

import logging
import os
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)


def send_alert(subject: str, body: str) -> None:
    """Send an email alert using SMTP credentials from environment variables.

    Required env vars:
        SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD, ALERT_RECIPIENT.
        ALERT_RECIPIENT can be comma-separated for multiple recipients.

    Args:
        subject: Email subject line.
        body: Plain text email body.

    Raises:
        KeyError: If required environment variables are not set.
        smtplib.SMTPException: If sending fails.
    """
    smtp_server = os.environ["SMTP_SERVER"]
    port = int(os.environ.get("SMTP_PORT", "465"))
    sender = os.environ["SMTP_USER"]
    password = os.environ["SMTP_PASSWORD"]
    recipients = [r.strip() for r in os.environ["ALERT_RECIPIENT"].split(",")]

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message.attach(MIMEText(body, "plain"))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, password)
        for recipient in recipients:
            server.sendmail(sender, recipient, message.as_string())

    logger.info("Alert sent to %s", recipients)
