import smtplib
import ssl
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import sys
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)
from patogh import settings


def send_email(otp, receiver):
    try:
      message = f"""
                <html>
                <body>
                <p>Patogh email verification code<br>
                <br> your code:
                {otp}
                <br/>
                </p>
                </body>
                </html>
                """
      email = EmailMultiAlternatives(subject="OTP", to=[receiver])
      email.attach_alternative(message, "text/html")
      email.send()
      # print('*'*10, otp)
    except:
      return {'message': 'try again.'}
      # print('#'*10)


# def send_email(otp, receiver):
#     print(otp)
#     print(receiver)

#     try:
#         sender_password = settings.EMAIL_HOST_PASSWORD
#         sender = settings.EMAIL_HOST_USER
#         message = MIMEMultipart("alternative")
#         message["Subject"] = 'subject'
#         message["From"] = sender
#         message["To"] = receiver

#         # Create the plain-text (it isn't force to use it) and HTML version of your message
#         html = """\
#                 <html>
#                   <body>
#                     <p>Patogh email verification code<br>
#                        <br> your code:
#                         """ + otp + """<br/>
#                     </p>
#                   </body>
#                 </html>
#                 """
#         # Turn these into plain/html MIMEText objects
#         part = MIMEText(html, "html")

#         # Add HTML/plain-text parts to MIMEMultipart message
#         # The email client will try to render the last part first
#         message.attach(part)

#         # Create secure connection with server and send email
#         context = ssl.create_default_context()
#         with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT, context=context) as server:
#             server.login(sender, sender_password)
#             server.sendmail(
#                 sender, receiver, message.as_string()
#             )
#     except:
#         return {'message': 'try again.'}