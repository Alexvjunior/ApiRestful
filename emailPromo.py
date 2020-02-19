from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from string import Template

class Email():
    def __init__(self):
        self.email = 'ticketspromocao@gmail.com'
        self.senha = 'ticketsPromo11111'


    def send_email(self, conteudo):
        self._create_corpo(conteudo)
        self._create_multi_part(self.email)
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(user=self.email, password=self.senha)
            smtp.send_message(self.msg)
            print('Email enviado com Sucesso')


    def _create_corpo(self, conteudo):
        with open('template.html', 'r') as html:
            template = Template(html.read())
            corpo_meg = template.substitute(data=conteudo)
            self.corpo = MIMEText(corpo_meg, 'html')
        
    def _create_multi_part(self, email_to):
        self.msg = MIMEMultipart()
        self.msg['from'] = 'Tickets Promo'
        self.msg['to'] = email_to
        self.msg['subject'] = 'URLs de Promoção'
        self.msg.attach(self.corpo)
