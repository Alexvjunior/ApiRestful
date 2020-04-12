from sql_alchemy import banco

class HotelModel(banco.Model):
    __tablename__ = 'hoteis'

    hotel_id = banco.Column(banco.String, primary_key=True)
    nome = banco.Column(banco.String(80))
    estrelas = banco.Column(banco.Float(precision=1))
    diaria = banco.Column(banco.Float(precision=2))

    def __init__(self, hotel_id, nome, estrelas, diaria):
        self.hotel_id = hotel_id
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria

    def json(self):
        return {
            "hotel_id": self.hotel_id,
            "nome": self.nome,
            "estrelas": self.estrelas,
            "diaria": self.diaria
        }

    @classmethod
    def find_hotel(cls, hotel_id):
        return cls.query.filter_by(hotel_id=hotel_id).first()

    def save_hotel(self):
        banco.session.add(self)
        banco.session.commit()

    def update_hotel(self, nome, estrelas, diaria):
        self.nome = nome
        self.estrelas = estrelas
        self.diaria = diaria
        self.save_hotel()

    def delete_hotel(self):
        banco.session.delete(self)
        banco.session.commit()