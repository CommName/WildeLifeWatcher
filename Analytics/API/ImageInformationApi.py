import cherrypy
import datetime
import json
import os

@cherrypy.expose
class InfomrationSearchAPI(object):

    Logic = None;

    def __init__(self, logic):
        self.Logic = logic


    def GET(self, animalName=None, feeding=None):
        if feeding is not None:
            if feeding.lower() in ['true', '1', 't', 'y', 'yes']:
                feeding = True
            else:
                feeding = False

        results = self.Logic.storage.getImagesWith(animalName, feeding)



        cherrypy.response.headers['Content-Type'] = 'application/json'

        for entry in results:
            entry['_id'] = str(entry['_id'])
            yield json.dumps(entry).encode()

    GET._cp_config = {'response.stream': True}
