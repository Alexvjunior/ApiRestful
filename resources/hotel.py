from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from utility import errors, success, server_code
from flask_jwt_extended import jwt_required
import sqlite3


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
        params = self.normalize_path_params(**dados_valids)
        tupla = tuple([value for value in params.values()])
        consulta = self.create_sql(**params)
        result = cursor.execute(consulta, tupla)
        hoteis = []
        for hotel in result:
            hoteis.append({
                "hotel_id":hotel[0],
                "nome":hotel[1],
                "estrelas":hotel[2],
                "diaria":hotel[3],
                "cidade":hotel[4],
            })
        return {'hoteis':hoteis}, server_code.OK

    def create_sql(self, **kwargs):
        if kwargs.get('cidade') is None:
            return "SELECT * FROM hoteis \
                WHERE (estrelas >= ? AND estrelas <= ?)\
                    AND (diaria > ? AND diaria <= ?)\
                        LIMIT ? OFFSET ?"
        return "SELECT * FROM hoteis \
                WHERE cidade = ?\
                    AND (estrelas >= ? AND estrelas <= ?)\
                    AND (diaria > ? AND diaria <= ?)\
                        LIMIT ? OFFSET ?"

    def normalize_path_params(self, cidade=None, estrelas_min=0, estrelas_max=5, diaria_min=0, diaria_max=10000, limit=50, offset=0, **kwargs):
        result = {
            "cidade": cidade,
            "estrelas_min": estrelas_min,
            "estrelas_max": estrelas_max,
            "diaria_min": diaria_min,
            "diaria_max": diaria_max,
            "limit": limit,
            "offset": offset
        }
        if cidade is None:
            del(result['cidade'])

        return result


class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True,
                            help="This field 'nome' canot be null")
    argumentos.add_argument('estrelas', type=float)
    argumentos.add_argument('diaria', type=float)
    argumentos.add_argument('cidade', type=str)

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
