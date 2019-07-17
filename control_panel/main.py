from flask import Flask
from flask import request
from flask import redirect
from flask import url_for
from flask import render_template
from flask_pymongo import PyMongo

app = Flask(__name__)

link_to_connection = 'mongodb://localhost:27017'
database_name = 'bot'
collection_name = 'moderation'

app.config['MONGO_URI'] = '/'.join([link_to_connection, database_name, collection_name])
mongo = PyMongo(app)
collection = mongo.db [collection_name]


@app.route('/', methods=['GET'])
def index():
	return '''

	<h1>See text channel info via ID:</h1>
	<form method='GET' action='/channel_info'>
		<input type='text' name='id'>
		<input type='submit'>
	</form>
	<h1>See server info:</h1>
	<form method='GET' action='/server_info''>
		<input type='text' name='server_name'>
		<input type='submit'>
	</form>
'''


@app.route('/channel_info', methods=['GET'])
def channel_info():
	id = request.args['id']
	channel = collection.find_one_or_404({'channel_id': id})
	return f'''
	{channel}
	'''


@app.route('/server_info', methods=['GET'])
def server_info():
	server_name = request.args['server_name']
	channel = mongo.db.moderation.find_one_or_404({'server_name': server_name})
	return render_template('server_info.html', myJSON=channel)


if __name__ == '__main__':
	app.run(debug=True)
