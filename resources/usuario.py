from flask_restful import Resource, reqparse
from models.usuario import UsuarioModel
from utility import errors, success, server_code
from flask_jwt_extended import create_access_token, jwt_required, get_raw_jwt
from blacklist import BLACKLIST
import traceback
from flask import make_response, render_template

_ARGUMENTOS = reqparse.RequestParser()
_ARGUMENTOS.add_argument('login', type=str, required=True,
                         help="This field canot be null")
_ARGUMENTOS.add_argument('senha', type=str, required=True,
                         help="This field canot be null")
_ARGUMENTOS.add_argument('email', type=str, required=True,
                         help="This field canot be null")
_ARGUMENTOS.add_argument('ativado', type=bool)


class Usuario(Resource):
    def get(self, user_id):
        user = UsuarioModel.find(user_id)
        if user is None:
            return errors._NOT_FOUND
        return user.json(), server_code.OK


class UsuarioRegister(Resource):

    def post(self):
        dados = _ARGUMENTOS.parse_args()
        if UsuarioModel.find_by_login(dados.get('login')) is not None:
            return errors._EXISTENT, server_code.BAD_REQUEST
        if UsuarioModel.find_by_email(dados.get('email')) is not None:
            return errors._EXISTENT, server_code.BAD_REQUEST

        user = UsuarioModel(**dados)
        user.ativado = False
        try:
            user.save()
            user.send_confirmation_email()
        except Exception as e:
            user.delete()
            traceback.print_exc()
            return errors._SAVE_ERROR, server_code.INTERNAL_SERVER_ERROR
        return user.json(), server_code.OK

    @jwt_required
    def delete(self, user_id):
        user = UsuarioModel.find(user_id)
        if user is None:
            return errors._NOT_FOUND, server_code.NOT_FOUND
        try:
            user.delete()
        except:
            return errors._DELETE_ERROR, server_code.INTERNAL_SERVER_ERROR
        return success._DELETED, server_code.OK


class Login(Resource):

    @classmethod
    def post(cls):
        dados = _ARGUMENTOS.parse_args()
        user = UsuarioModel.find_by_login(dados.get('login'))
        if user is None or user.senha != dados.get('senha'):
            return errors._NOT_FOUND, server_code.NOT_FOUND
        if not user.ativado:
            return {'message': "user has not been activated"}, 400
        token_access = create_access_token(identity=user.user_id)
        return {"access_token": token_access}, 200


class Logout(Resource):

    @jwt_required
    def post(self):
        jwt_id = get_raw_jwt()['jti']
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfuly'}, server_code.OK


class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id):
        user = UsuarioModel.find(user_id)
        if user is None:
            return errors._NOT_FOUND, server_code.NOT_FOUND
        user.ativado = True
        try:
            user.save()
            headers = {"Content-Type":"text/html"}
            return make_response(render_template('confirm.html', email=user.email, login=user.login), 200, headers)
        except:
            return errors._SAVE_ERROR, server_code.INTERNAL_SERVER_ERROR