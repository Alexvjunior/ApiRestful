from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from utility import errors, success, server_code
from flask_jwt_extended import jwt_required

class Hoteis(Resource):
    def get(self):
        return {'hoteis':[hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help="This field 'nome' canot be null")
    argumentos.add_argument('estrelas', type=float)
    argumentos.add_argument('diaria', type=float)

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