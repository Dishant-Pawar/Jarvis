import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from utils.logger import get_logger
from utils.helpers import format_response

logger = get_logger()

def send_email(settings_manager, recipient_email: str, subject: str, body: str) -> dict:
    # Load SMTP settings
    settings_manager.load_config()
    smtp_server = settings_manager.get_setting("smtp_server", "smtp.gmail.com")
    smtp_port = int(settings_manager.get_setting("smtp_port", 587))
    sender_email = settings_manager.get_setting("smtp_email", "")
    sender_password = settings_manager.get_setting("smtp_password", "")

    if not sender_email or not sender_password:
        logger.warning("SMTP email credentials are not configured in settings.")
        return format_response(
            False, 
            "SMTP email credentials are not configured. Please set 'smtp_email' and 'smtp_password' in config.json."
        )

    try:
        logger.info(f"Setting up SMTP connection to {smtp_server}:{smtp_port}...")
        
        # Build MIME message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect and authenticate
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Send
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()
        
        logger.info(f"Email successfully sent to: {recipient_email}")
        return format_response(True, f"Email sent successfully to {recipient_email}.", {"to": recipient_email})
    except Exception as e:
        logger.error(f"Failed to send email via SMTP: {e}")
        return format_response(False, f"Failed to send email: {str(e)}")
