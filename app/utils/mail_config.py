from pydantic_settings import BaseSettings
from fastapi_mail import ConnectionConfig

class MailSettings(BaseSettings):
    """
    Configuration settings for the mail server loaded from environment variables.

    Attributes:
        mail_server (str): SMTP server address (e.g., smtp.gmail.com).
        mail_port (int): SMTP server port (e.g., 587 for STARTTLS).
        mail_username (str): SMTP authentication username (usually the email).
        mail_password (str): SMTP authentication password or app password.
        mail_from (str): Email address that appears as the sender.
    """

    mail_server: str
    mail_port: int
    mail_username: str
    mail_password: str
    mail_from: str

    model_config = {
        "env_file": ".env",
        "extra": "allow"  # allow extra keys in the .env file without errors
    }

# Load mail settings from the environment variables in .env file
mail_settings = MailSettings()

# Create FastAPI-Mail ConnectionConfig using the loaded settings
conf = ConnectionConfig(
    MAIL_USERNAME=mail_settings.mail_username,
    MAIL_PASSWORD=mail_settings.mail_password,
    MAIL_FROM=mail_settings.mail_from,
    MAIL_PORT=mail_settings.mail_port,
    MAIL_SERVER=mail_settings.mail_server,
    MAIL_STARTTLS=True,      # Gmail requires STARTTLS on port 587
    MAIL_SSL_TLS=False,      # SSL should be False when using STARTTLS
    USE_CREDENTIALS=True     # Enable authentication with credentials
)