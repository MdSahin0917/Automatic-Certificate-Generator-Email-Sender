import smtplib, ssl
from email.message import EmailMessage



# Email settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
SENDER_EMAIL = "your-email@gmail.com"  # Your email
SENDER_PASSWORD = "your app password"  # Use App Password for Gmail




def send_email(receiver_email, name, cert_path,email_content):
    msg = EmailMessage()
    msg["Subject"] = "Participation E-Certificate"
    msg["From"] = SENDER_EMAIL
    msg["To"] = receiver_email
    msg.set_content(f"Dear {name},\n\n{email_content}")

    # Attach certificate
    with open(cert_path, "rb") as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype="application", subtype="pdf", filename=f"{name}.pdf")

    # Send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
    
    print(f"Certificate sent to {name} ({receiver_email})")
