from flask import Flask, request
from flask_restful import Resource, Api

from Analyzer import Analyzer
from TensorBoard import Visualize

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

class ShowBoard(Resource):
    def get(self):
        mid = request.args.get('mid')
        if mid:
            tb = Visualize(mid)
            if an.error:
                return {'message': 'cannot found talk'}
            else:
                an.start()
                return {'path': tb.path}
        else:
            return {'message': 'cannot found mid'}

api.add_resource(AnalyzeMeeting, '/')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)