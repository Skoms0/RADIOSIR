from flask import Flask, jsonify
import sys
import os
from dataProcess import DataProcess

class SocketAPI:
    def __init__(self, db_path='data.db'):
        self.db_path = db_path
        self.dp = DataProcess()
        self.app = Flask(__name__)
        self.setup_routes()
    
    def setup_routes(self):
        @self.app.route('/last', methods=['GET'])
        def get_last_record():
            try:
                record = self.dp.get_last_record(self.db_path)
                if record:
                    return jsonify(record), 200
                else:
                    return jsonify({'error': 'No data found'}), 404
            except Exception as e:
                return jsonify({'error': str(e)}), 500
            
        @self.app.route('/last_all', methods=['GET'])
        def get_last_all_record():
            try:
                record = self.dp.get_all_records(self.db_path)
                if record:
                    return jsonify(record), 200
                else:
                    return jsonify({'error': 'No data found'}), 404
            except Exception as e:
                return jsonify({'error': str(e)}), 500

    def run(self, host='0.0.0.0', port=5000):
        self.app.run(host=host, port=port)

if __name__ == '__main__':
    api = SocketAPI('data.db')
    api.run(port=5005)
