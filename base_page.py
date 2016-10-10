import webapp2
import os
import jinja2
from google.appengine.ext import ndb
import db_defs

class MainPage(webapp2.RequestHandler):
	
	def __init__(self, request, response):
		self.initialize(request, response)
		self.template_values = {}
		self.template_values['colors'] = [{'name':'Red'},{'name':'Orange'},{'name':'Yellow'},{'name':'Green'},{'name':'Blue'},{'name':'Indigo'},{'name':'Violet'}]
		self.template_values['cuisines'] = [{'name':'Greek','picked':'False'},{'name':'Mexican','picked':'False'},{'name':'Italian','picked':'False'},{'name':'Sushi','picked':'False'},{'name':'Indian','picked':'False'},{'name':'Vegetarian','picked':'False'}]
	
	@webapp2.cached_property
	def jinja2(self):
		return jinja2.Environment(
		loader=jinja2.FileSystemLoader(os.path.dirname(__file__) + '/templates'),
		extensions=['jinja2.ext.autoescape'],
		autoescape=True
		)
	
	def render(self, template, template_variables={}):
		template = self.jinja2.get_template(template)
		self.template_values['entries'] = [{'name':x.name, 'key':x.key.urlsafe()} for x in db_defs.Entry.query(ancestor=ndb.Key(db_defs.Entry, 'base-data')).fetch()]
		self.response.write(template.render(template_variables))
		
	def get(self):
		self.render('assignment2.html', self.template_values)
	
	def post(self):
		action = self.request.get('action')
		if action == 'new_entry':
			k = ndb.Key(db_defs.Entry, 'base-data')
			entry = db_defs.Entry(parent=k)
			entry.name = self.request.get('username')
			entry.color = self.request.get('color')
			entry.cuisine = self.request.get_all('cuisine')
			entry.num_sibs = self.request.get('num_sibs')
			if entry.name == '':
				self.template_values['message_title'] = 'ERROR: Missing Required Field'
				self.template_values['message'] = 'The name field is required. Please enter a name before submitting to database.'
				self.render('assignment2.html', self.template_values)
			else:
				list = {}
				list = db_defs.Entry.query(ancestor=ndb.Key(db_defs.Entry, 'base-data')).fetch()
				duplicate = False
				for i in list:
					if i.name == entry.name:
						self.template_values['message_title'] = 'ERROR: Duplicate Entry'
						self.template_values['message'] = entry.name + ' already exists in the database. Please choose a different name.'
						duplicate = True
				if duplicate == True:
					self.render('assignment2.html', self.template_values)
				else:
					entry.put()
					self.template_values['message_title'] = 'Form Content Submitted'
					self.template_values['message'] = 'Added ' + entry.name + ' to the database.'
					self.render('assignment2.html', self.template_values)
		else:
			self.template_values['message'] = 'Action ' + action + ' is unknown.'
			self.render('assignment2.html', self.template_values)