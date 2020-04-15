from sql_alchemy import banco

class SiteModel(banco.Model):
    __tablename__ = 'sites'
    site_id = banco.Column(banco.Integer, primary_key=True)
    url = banco.Column(banco.String)
    hoteis = banco.relationship('HotelModel')

    def __init__(self, url):
        self.url = url

    def json(self):
        return {
            "site_id": self.site_id,
            "url": self.url,
            "hoteis":[hotel.json() for hotel in self.hoteis]
        }
    
    @classmethod
    def find(cls, url):
        return cls.query.filter_by(url=url).first()

    def save(self):
        banco.session.add(self)
        banco.session.commit()
    
    def update(self, url):
        self.url = url
        self.save_hotel()

    def delete(self):
        [hotel.delete_hotel() for hotel in self.hoteis]
        banco.session.delete(self)
        banco.session.commit()

    @classmethod
    def find_by_id(cls, site_id):
        return cls.query.filter_by(site_id=site_id).first()