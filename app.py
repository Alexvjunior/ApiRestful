from flask import Flask, jsonify
from flask_restful import Api
from utility import server_code
from resources.hotel import Hoteis, Hotel
from resources.usuario import Usuario, UsuarioRegister, Login, Logout, UserConfirm
from resources.sites import Sites, Site
from flask_jwt_extended import JWTManager
from blacklist import BLACKLIST

_APP = Flask(__name__)
_APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
_APP.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
_APP.config['JWT_SECRET_KEY'] = "DontTellAnyone"
_APP.config['JWT_BLACKLIST_ENABLED'] = True
_API = Api(_APP)
_JWT = JWTManager(_APP)

@_APP.before_first_request
def create_data_base():
    banco.create_all()

@_JWT.token_in_blacklist_loader
def verify_blacklist(token):
    return token['jti'] in BLACKLIST

@_JWT.revoked_token_loader
def token_invalidate():
    return jsonify({'message':'You have been logged out.'}), server_code.UNAUTHORIZED

_API.add_resource(Hoteis, '/hoteis')
_API.add_resource(Hotel, '/hotel/<string:hotel_id>')
_API.add_resource(Usuario, '/usuario/<int:user_id>')
_API.add_resource(UsuarioRegister, '/cadastro')
_API.add_resource(Login, '/login')
_API.add_resource(Logout, '/logout')
_API.add_resource(Sites, '/sites')
_API.add_resource(Site, '/site/<string:url>')
_API.add_resource(UserConfirm, '/confirmacao/<int:user_id>')

if __name__ == '__main__':
    from sql_alchemy import banco
    banco.init_app(_APP)
    _APP.run(host="0.0.0.0", port=5000, debug=True)
