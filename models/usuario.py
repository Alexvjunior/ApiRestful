from sql_alchemy import banco
from flask import request, url_for
from requests import post
class UsuarioModel(banco.Model):
    __tablename__ = 'usuario'
    __API_KEY = 'a8c7e4aef21d0dfb83e1230189b53cd4-915161b7-d027a0c6'
    __MAIL_GUN = 'sandbox20f460aba6be45189d2b959ee0fa547a.mailgun.org'
    __FROM_TITLE = 'NO-REPLY'
    __FROM_EMAIL = 'no-reply@restapi.com'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40))
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)
    

    def __init__(self, login, senha, email,ativado):
        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = ativado


    def send_confirmation_email(self):
        # http://localhost:5000/confirmacao
        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)
        return post(f'https://api.mailgun.net/v3/{self.__MAIL_GUN}/messages',
            auth=('api', self.__API_KEY),
            data={"from":f"{self.__FROM_TITLE} <{self.__FROM_EMAIL}>",
                    "to":self.email,
                    "subject":"Confirmaço de Cadastro",
                    "text":f"Confirme seu cadastro no link: {link}"
                }
            )
        

    def json(self):
        return {
            "user_id": self.user_id,
            "login": self.login,
            "email": self.email,
            "ativado": self.ativado
        }

    @classmethod
    def find(cls, user_id):
        return cls.query.filter_by(user_id=user_id).first()

    @classmethod
    def find_by_login(cls, login):
        return cls.query.filter_by(login=login).first()
        
    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    def save(self):
        banco.session.add(self)
        banco.session.commit()

    def delete(self):
        banco.session.delete(self)
        banco.session.commit()
