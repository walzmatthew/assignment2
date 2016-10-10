import webapp2
import base_page
import jinja2
from google.appengine.ext import ndb
import db_defs

class Edit(base_page.MainPage):
	
	def get(self):
		entry_key = ndb.Key(urlsafe=self.request.get('key'))
		entry = entry_key.get()
		self.template_values['key'] = self.request.get('key')
		self.template_values['name'] = entry.name
		self.template_values['fav_color'] = entry.color
		for i in self.template_values['cuisines']:
			for j in entry.cuisine:
				if j == i['name']:
					i['picked'] = 'True'
		self.template_values['num_sibs'] = entry.num_sibs
		self.render('assignment2edit.html', self.template_values)
	
	def post(self):
		action = self.request.get('action')
		if action == 'edit_entry':
			entry_key = ndb.Key(urlsafe=self.request.get('key'))
			entry = entry_key.get()
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
						if i.key != entry.key:
							self.template_values['message_title'] = 'ERROR: Duplicate Entry'
							self.template_values['message'] = entry.name + ' already exists in the database. Please choose a different name.'
							duplicate = True
				if duplicate == True:
					self.redirect('/edit?key=' + entry_key.urlsafe() + '&type=entry')
				else:
					entry.put()
					self.template_values['message_title'] = 'Form Content Updated'
					self.template_values['message'] = entry.name + ' successfully updated in the database.'
					self.template_values['name'] = entry.name
					self.redirect('/edit?key=' + entry_key.urlsafe() + '&type=entry')
		else:
			self.template_values['message'] = 'Action ' + action + ' is unknown.'
			self.redirect('/edit?key=' + entry_key.urlsafe() + '&type=entry')