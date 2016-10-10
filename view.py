import webapp2
import base_page
import jinja2
from google.appengine.ext import ndb
import db_defs

class View(base_page.MainPage):
	
	def get(self):
		entry_key = ndb.Key(urlsafe=self.request.get('key'))
		entry = entry_key.get()
		self.template_values['name'] = entry.name
		self.template_values['color'] = entry.color
		for i in self.template_values['cuisines']:
			for j in entry.cuisine:
				if j == i['name']:
					i['picked'] = 'True'
		self.template_values['num_sibs'] = entry.num_sibs
		self.render('assignment2view.html', self.template_values)