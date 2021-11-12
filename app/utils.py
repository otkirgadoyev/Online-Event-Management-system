from django.core import mail
from django.utils.html import strip_tags

class Util: 
    @staticmethod
    def send_email(data):

        subject = data['email_subject']
        html_message = data['email_body']
        plain_message = strip_tags(data['email_body'])
        from_email = 'From <from@example.com>'
        to = data['to_email']

        mail.send_mail(subject, plain_message, from_email,
                        [to], html_message=html_message)