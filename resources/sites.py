from flask_restful import Resource, reqparse
from models.site import SiteModel
from utility import errors, success, server_code


class Sites(Resource):
    def get(self):
        return {"sites": [site.json() for site in SiteModel.query.all()]}


class Site(Resource):
    def get(self, url):
        site = SiteModel.find(url)
        return site.json(), server_code.OK if site is not None else errors._NOT_FOUND, server_code.NOT_FOUND

    def post(self, url):
        site = SiteModel.find(url)
        if site is not None:
            return errors._EXISTENT, server_code.BAD_REQUEST
        site = SiteModel(url)
        try:
            site.save()
        except:
            return errors._SAVE_ERROR, server_code.INTERNAL_SERVER_ERROR
        return site.json()

    def put(self, url):
        site = SiteModel.find(url)
        if site is None:
            site = SiteModel(url)
            try:
                site.save()
            except:
                return errors._SAVE_ERROR, server_code.INTERNAL_SERVER_ERROR
            return site.json(), server_code.OK
        try:
            site.update()
        except:
            return errors._SAVE_ERROR, server_code.INTERNAL_SERVER_ERROR
        return site.json(), server_code.OK

    def delete(self, url):
        site = SiteModel.find(url)
        if site is None:
            return errors._DELETE_ERROR, server_code.NOT_FOUND
        site.delete()
