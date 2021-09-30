# Imports
from email import message
import smtplib
import email
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase

# The Mailer class


class Mailer:
    def __init__(self, mailid, password, server):
        # mailid and password are the credentials for the mail account
        self.mailid = mailid
        self.password = password
        # server is the server to be used and server_details() is used to get the details
        self.server = self.server_details(server)

    def send_mail(self, to, subject, body, bcc=None, attachment=None, html=None):
        """ This function sends an email to the specified recipient.

        Parameters:
        to (str): The recipient of the email.
        subject (str): The subject of the email.
        body (str): The body of the email.
        bcc (str): The bcc of the email.
        attachment (file): The attachment of the email.
        html (str): Whether the email is html or not.

        """
        # Create the message
        message = MIMEMultipart()
        message["From"] = self.mailid
        message["To"] = to
        message["Subject"] = subject
        # if bcc is available, add it to the message
        if bcc is not None:
            message["Bcc"] = bcc

        # if html is available, add it to the message
        if html is not None:
            message.attach(MIMEText(body, 'text'))
            message.attach(MIMEText(html, 'html'))
        else:
            message.attach(MIMEText(body, 'text'))

        # if attachment is available, add it to the message
        if attachment is not None:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())             # Read the file
            email.encoders.encode_base64(part)              # Encode the file
            part.add_header(
                "Content-Disposition",
                "attachment; filename=%s" % attachment.filename,
            )                                            # Add the header
            message.attach(part)

        context = ssl.create_default_context()              # Create the SSL context
        # connect to the server
        try:
            server = smtplib.SMTP(self.server['address'], 587)
            server.ehlo_or_helo_if_needed()         # Identify the server
            server.starttls(context=context)        # Start TLS encryption
            server.ehlo_or_helo_if_needed()         # Ping the server
            server.login(self.mailid, self.password)    # Login to the server
            server.sendmail(self.mailid, to, message.as_string()
                            )       # Send the email

        # if the connection fails, print the error
        except Exception as e:
            print(e)
            return False

        # quit the server
        finally:
            server.quit()

    def server_details(self, server):
        """ This function returns the details of the server."""
        servers = {
            "gmail": {
                "address": "smtp.gmail.com",
            },
            "yahoo": {
                "address": "smtp.mail.yahoo.com",
            },
            "outlook": {
                "address": "smtp-mail.outlook.com",
            },
            "hotmail": {
                "address": "smtp.live.com",
            },
            "icloud": {
                "address": "smtp.mail.me.com",
            },

        }
        return servers[server]
