from fastapi_mail import FastMail, MessageSchema
from app.utils.mail_config import conf
import asyncio

async def send_account_creation_email(to_email: str, first_name: str, password: str):
    """
    Sends a welcome email with account creation details to the specified email address.

    Args:
        to_email (str): Recipient's email address.
        first_name (str): Recipient's first name, used for personalizing the email.
        password (str): Temporary password assigned to the new account.

    The email contains the recipient's email and password and advises them
    to log in and change their password as soon as possible.
    """
    subject = "Welcome to Our Platform - Account Created"
    body = f"""
    Hi {first_name},<br><br>
    Your account has been successfully created.<br><br>
    <b>Email:</b> {to_email}<br>
    <b>Password:</b> {password}<br><br>
    Please log in and change your password as soon as possible.<br><br>
    Best regards,<br>
    The Team
    """

    message = MessageSchema(
        subject=subject,
        recipients=[to_email],
        body=body,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)


