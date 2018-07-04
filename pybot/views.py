from flask import Flask, render_template, request, jsonify

from datetime import datetime

from pybot import app, db
from pybot.models import NoResultUserRequest
import pybot.utils as utils
import pybot.config as conf


NO_RESULT_SENTENCE = "Euh... Non là, je n'ai rien d'intéressant à ce sujet ! "

#Use for display the correct year for the copyright in the footer
@app.context_processor
def inject_now():
    return dict(now=datetime.now())

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	return render_template('index.html', google_key=conf.GOOGLE_MAPS_KEY)


@app.route('/wiki_api')
def wiki_api():
	keywords = request.args.get('keywords', '')
	keywords = utils.parser(keywords)
	address = request.args.get('address','')

	keywords_try_1 = utils.parser_for_wiki(address) #Addresse of the place
	keywords_try_2 = utils.parser_for_name_of_road(keywords_try_1) # Only the name of the road
	keywords_try_3 = utils.parser(keywords) #Same keywords that in the google search
	keywords_try_4 = utils.parser_for_name_of_road(keywords_try_3) #If there is a city name in the question, remove it

	try:
		result = utils.get_data_from_wiki(keywords_try_1)
	except KeyError:
		try:
			result = utils.get_data_from_wiki(keywords_try_2)
		except KeyError:
			try:
				result = utils.get_data_from_wiki(keywords_try_3)
			except KeyError:
				try:
					result = utils.get_data_from_wiki(keywords_try_4)
				except KeyError:
					result = NO_RESULT_SENTENCE
	except ValueError:
		try:
			result = utils.get_data_from_wiki(keywords_try_3)
		except KeyError:
			try:
				result = utils.get_data_from_wiki(keywords_try_4)
			except KeyError:
				result = NO_RESULT_SENTENCE
	if result == '': #Case of wikipedia got an empty page
		result = NO_RESULT_SENTENCE			
	return jsonify(result)


@app.route('/google_api')
def google_api():
	keywords = request.args.get('keywords', '')
	keywords = utils.parser(keywords)
	try:
		result_lat, result_long, address = utils.get_data_from_google_maps(keywords)
		return jsonify(result_lat, result_long, address)
	except TypeError:
		#### New feature
		# Collect the data of User Request with no result
		no_result_case = NoResultUserRequest(request=keywords)
		db.session.add(no_result_case)
		db.session.commit()
		#### End new feature
		return jsonify('NORETURN')

#### New feature ####
@app.route('/no_result')
def no_result():
	"""This view is use to display the elements of the database as a table"""
	list_no_result = NoResultUserRequest.query.all()
	return render_template('no_result.html', list_no_result=list_no_result)