"""Stripe webhook handler (FastAPI).

This module exposes a `router` (FastAPI `APIRouter`) so it can be included
into the main application without creating a second FastAPI instance.

Supports SMTP and SendGrid email backends. Local testing instructions are in
`docs/CONSULTATION.md`.

Example .env.local:
    STRIPE_SECRET_KEY=sk_test_...
    STRIPE_WEBHOOK_SECRET=whsec_...
    EMAIL_BACKEND=smtp
    EMAIL_HOST=smtp.gmail.com
    EMAIL_PORT=587
    EMAIL_USERNAME=your-email@gmail.com
    EMAIL_PASSWORD=app-password
    EMAIL_FROM=noreply@your-domain.com

Or use SendGrid:
    SENDGRID_API_KEY=SG.xxx
    EMAIL_FROM=noreply@your-domain.com
"""

import json
import logging
import os
from pathlib import Path

import stripe
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, Request

load_dotenv()

router = APIRouter()


def _get_env_keys():
    return os.getenv("STRIPE_SECRET_KEY"), os.getenv("STRIPE_WEBHOOK_SECRET")


def send_confirmation_email(email: str, session: dict):
    """Send a confirmation email after successful checkout.

    Supports SMTP and SendGrid (via env vars in .env.local).
    """
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText

    email_backend = os.getenv("EMAIL_BACKEND", "smtp").lower()
    email_from = os.getenv("EMAIL_FROM", "noreply@luminai-genesis.local")
    email_host = os.getenv("EMAIL_HOST")
    email_port = int(os.getenv("EMAIL_PORT", "587"))
    email_user = os.getenv("EMAIL_USERNAME")
    email_pass = os.getenv("EMAIL_PASSWORD")
    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")

    subject = "LuminAI Genesis Consultation: Booking Confirmed"
    body = (
        f"Hi there,\n\n"
        "Thank you for purchasing a consultation slot!\n\n"
        "Next step: Please pick a time here: https://calendly.com/"
        "elidorascodex/luminai-consultation\n\n"
        "We look forward to talking with you.\n\n"
        "— The Elidoras Codex\n\n"
        f"Session ID: {session.get('id')}\n"
    )

    logger = logging.getLogger(__name__)
    try:
        if sendgrid_api_key:
            # SendGrid integration
            from sendgrid import SendGridAPIClient
            from sendgrid.helpers.mail import Mail

            message = Mail(
                from_email=email_from,
                to_emails=email,
                subject=subject,
                plain_text_content=body,
            )
            sg = SendGridAPIClient(sendgrid_api_key)
            sg.send(message)
            logger.info("[Webhook] Sent confirmation email to %s via SendGrid", email)
        elif email_backend == "smtp" and email_host and email_user and email_pass:
            # SMTP integration
            msg = MIMEMultipart()
            msg["From"] = email_from
            msg["To"] = email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            with smtplib.SMTP(email_host, email_port) as server:
                server.starttls()
                server.login(email_user, email_pass)
                server.send_message(msg)
            logger.info("[Webhook] Sent confirmation email to %s via SMTP", email)
        else:
            # Fallback: log (development)
            logger.info("[Webhook] (DEV MODE) Would send email to %s", email)
    except ImportError as e:
        # Missing dependency for SendGrid or SMTP
        logger.exception("[Webhook] Missing dependency for sending email to %s: %s", email, e)
    except smtplib.SMTPException as e:
        logger.exception("[Webhook] SMTP error while sending email to %s: %s", email, e)
    except Exception as e:
        logger.exception("[Webhook] Error sending email to %s: %s", email, e)


def save_session_info(session: dict):
    # Simple local persistence for bookkeeping (append to a file). Replace with
    # DB as needed.
    try:
        p = Path("/tmp/stripe_sessions.log")
        with p.open("a", encoding="utf-8") as f:
            f.write(json.dumps(session) + "\n")
    except OSError:
        # Disk write failure or permission problem; ignore to avoid disrupting webhook
        pass


@router.post("/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events.

    Signature verification is optional (for local dev).
    Handles checkout.session.completed to send confirmation emails.
    """
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    stripe_key, webhook_secret = _get_env_keys()

    if stripe_key:
        stripe.api_key = stripe_key

    # If a webhook secret is configured, verify signatures. Otherwise parse payload
    # without verification (useful for local dev but DO NOT use in production).
    if webhook_secret:
        if not sig_header:
            raise HTTPException(
                status_code=400,
                detail="Missing stripe-signature header",
            )
        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid signature")
    else:
        # Best-effort parse (development only)
        try:
            event = json.loads(payload.decode("utf-8"))
        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON payload: {e}")

    # Handle the event
    if event.get("type") == "checkout.session.completed":
        # In both verified and unverified payloads, path to object differs slightly
        session = event.get("data", {}).get("object") or event.get("object") or event
        customer_email = None
        if isinstance(session, dict):
            customer_email = session.get("customer_details", {}).get("email")
        save_session_info(session)
        if customer_email:
            send_confirmation_email(customer_email, session)

    return {"status": "success"}
