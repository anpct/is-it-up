import threading 
import time
import requests
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


smtp_server = "smtp.gmail.com"
port = 587  # For starttls
sender_email = "my@gmail.com"
password = "opo"

# Create the plain-text and HTML version of your message
text = """\
Hi,
How are you?
Real Python has many great tutorials:
www.realpython.com"""
html = """\
<html>
  <body>
    <p>Hi,<br>
       How are you?<br>
       <a href="http://www.realpython.com">Real Python</a> 
       has many great tutorials.
    </p>
  </body>
</html>
"""

class RepeatedTimer(object):
  def __init__(self, interval, function, *args, **kwargs):
    self._timer = None
    self.interval = interval
    self.function = function
    self.args = args
    self.kwargs = kwargs
    self.is_running = False
    self.next_call = time.time()
    self.start()

  def _run(self):
    self.is_running = False
    self.start()
    self.function(*self.args, **self.kwargs)

  def start(self):
    if not self.is_running:
      self.next_call += self.interval
      self._timer = threading.Timer(self.next_call - time.time(), self._run)
      self._timer.start()
      self.is_running = True

  def stop(self):
    self._timer.cancel()
    self.is_running = False

class Website():
    def __init__(self, name, url, emails):
        self.name = name
        self.url = url
        self.emails = emails

    def send_mail(self):
        context = ssl.create_default_context()

        # Try to log in to server and send email
        try:
            server = smtplib.SMTP(smtp_server,port)
            server.ehlo() # Can be omitted
            server.starttls(context=context) # Secure the connection
            server.ehlo() # Can be omitted
            server.login(sender_email, password)
            for mail in self.emails:
                message = MIMEMultipart("alternative")
                message["Subject"] = "multipart test"
                message["From"] = sender_email
                message["To"] = mail
                part1 = MIMEText(text, "plain")
                part2 = MIMEText(html, "html")
                message.attach(part1)
                message.attach(part2)           
                server.sendmail(
                    sender_email, mail, message.as_string()
                )


        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            server.quit()

    def test(self):
        try:
            request = requests.get(self.url)
            if request.status_code == 200:
                return True
            else:
                print("Website returned response code: {code}".format(code=request.status_code))
        except ConnectionError:
            print('Web site does not exist')


from time import sleep

def hello(name):
    print("Hello %s!" % name)

print("starting...")
rt = RepeatedTimer(1, hello, "World")
