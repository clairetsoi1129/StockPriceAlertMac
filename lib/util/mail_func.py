import smtplib, ssl #enables you to send emails
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
### Add new subclass for adding attachments
from email.mime.application import MIMEApplication
## The pandas library is only for generating the current date, which is not necessary for sending emails
import pandas as pd

def send_email(sender, passwd, receiver, msg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, passwd) #logs into your email account
    
    print("Login Success")#confirms that you have logged in succesfully
    server.sendmail(sender, receiver, msg)#send the email with your custom mesage
    print("Email was sent") #confirms that the email was sent
    server.quit()

def send_email_ssl(sender, passwd, receiver, msg):
    # Connect to the Gmail SMTP server and Send Email
    # Create a secure default settings context
    context = ssl.create_default_context()
    # Connect to Gmail's SMTP Outgoing Mail server with such context
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        # Provide Gmail's login information
        server.login(sender, passwd)
        # Send mail with from_addr, to_addrs, msg, which were set up as variables above
        server.sendmail(sender, receiver, msg)

def send_email_ssl_html(sender, passwd, receiver, subject, html, imgs=None, attachments=None):
    # Create a MIMEMultipart class, and set up the From, To, Subject fields
    email_message = MIMEMultipart()
    email_message['From'] = sender
    email_message['To'] = receiver
    email_message['Subject'] = subject

    # Attach the html doc defined earlier, as a MIMEText html content type to the MIME message
    email_message.attach(MIMEText(html, "html"))

    # Attach more (documents)
    ## Apply function with extra_header on chart.png. This will render chart.png in the html content
    ##############################################################
    if imgs is not None:
        attach_file_to_email(email_message, imgs, {'Content-ID': '<myimageid>'})
    ##############################################################
    if attachments is not None:
        attach_file_to_email(email_message, attachments)

    # Convert it as a string
    email_string = email_message.as_string()

    # Connect to the Gmail SMTP server and Send Email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, passwd)
        server.sendmail(sender, receiver, email_string)

def send_email_ssl_price_alert(sender, passwd, receiver, ticker, target_price, imgs=None, attachments=None):
    # Define the HTML document
    html = '''
        <html>
            <body>
                <h1>Price Alert</h1>
                <p>Stock ##TICKER## reach target price ##TARGET_PRICE##</p>
                <img src='cid:myimageid' width="700">
            </body>
        </html>
        '''
    html = html.replace("##TICKER##", ticker)
    html = html.replace("##TARGET_PRICE##", str(target_price))
    subject = f'Price Alert - {ticker}'

    send_email_ssl_html(sender, passwd, receiver, subject, html)

def attach_file_to_email(email_message, filename, extra_headers=None):
    # Open the attachment file for reading in binary mode, and make it a MIMEApplication class
    with open(filename, "rb") as f:
        file_attachment = MIMEApplication(f.read())
    # Add header/name to the attachments    
    file_attachment.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    # Set up the input extra_headers for img
      ## Default is None: since for regular file attachments, it's not needed
      ## When given a value: the following code will run
         ### Used to set the cid for image
    if extra_headers is not None:
        for name, value in extra_headers.items():
            file_attachment.add_header(name, value)
    # Attach the file to the message
    email_message.attach(file_attachment)