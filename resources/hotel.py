from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from models.site import SiteModel
from utility import errors, success, server_code
from flask_jwt_extended import jwt_required
import sqlite3
from resources import filters


class Hoteis(Resource):
    path_params = reqparse.RequestParser()
    path_params.add_argument('cidade', type=str)
    path_params.add_argument('estrelas_min', type=float)
    path_params.add_argument('estrelas_max', type=float)
    path_params.add_argument('diaria_min', type=float)
    path_params.add_argument('diaria_max', type=float)
    path_params.add_argument('limit', type=float)
    path_params.add_argument('offset', type=float)

    def get(self):
        connection = sqlite3.connect('banco.db')
        cursor = connection.cursor()

        dados = self.path_params.parse_args()
        dados_valids = {chave: valor for chave,
                        valor in dados.items() if valor is not None}
        params = filters.normalize_path_params(**dados_valids)
        tupla = tuple([value for value in params.values()])
        consulta = filters.create_sql(**params)
        result = cursor.execute(consulta, tupla)
        hoteis = []
        for hotel in result:
            hoteis.append({
                "hotel_id":hotel[0],
                "nome":hotel[1],
                "estrelas":hotel[2],
                "diaria":hotel[3],
                "cidade":hotel[4],
                "site_id":hotel[5],
            })
        return {'hoteis':hoteis}, server_code.OK



class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True,
                            help="This field 'nome' canot be null")
    argumentos.add_argument('estrelas', type=float)
    argumentos.add_argument('diaria', type=float)
    argumentos.add_argument('cidade', type=str)
    argumentos.add_argument('site_id', type=int, required=True)

    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is None:
            return errors._NOT_FOUND
        return hotel.json(), server_code.OK

    @jwt_required
    def post(self, hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return errors._EXISTENT, server_code.BAD_REQUEST
        dados = self.argumentos.parse_args()
        hotel = HotelModel(hotel_id, **dados)
        if SiteModel.find_by_id(hotel.site_id) is None:
            return errors._NOT_FOUND, server_code.NOT_FOUND
        try:
            hotel.save_hotel()
        except:
            return errors._SAVE_ERROR, server_code.INTERNAL_SERVER_ERROR
        return hotel.json(), server_code.OK

    @jwt_required
    def put(self, hotel_id):
        dados = self.argumentos.parse_args()
        hotel_found = HotelModel.find_hotel(hotel_id)
        if hotel_found is not None:
            hotel_found.update_hotel(**dados)
            return hotel_found.json(), server_code.OK
        hotel = HotelModel(hotel_id, **dados)
        try:
            hotel.save_hotel()
        except:
            return errors._SAVE_ERROR, server_code.INTERNAL_SERVER_ERROR
        return hotel.json(), server_code.CREATED

    @jwt_required
    def delete(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel is None:
            return errors._NOT_FOUND, server_code.NOT_FOUND
        try:
            hotel.delete_hotel()
        except:
            return errors._DELETE_ERROR, server_code.INTERNAL_SERVER_ERROR
        return success._DELETED, server_code.OK
