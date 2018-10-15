from flask import Flask, request
from flask_restful import Resource, Api

from Analyzer import Analyzer

app = Flask(__name__)
api = Api(app)

class AnalyzeMeeting(Resource):
    def get(self):
        mid = request.args.get('mid')
        if mid:
            an = Analyzer(mid)
            if an.error:
                return {'message': 'cannot found talk'}
            else:
                an.start()
                return {'status': 'success'}
        else:
            return {'message': 'cannot found mid'}

api.add_resource(AnalyzeMeeting, '/')

if __name__ == "__main__":
    app.run(debug=True, port=5000)