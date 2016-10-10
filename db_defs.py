from google.appengine.ext import ndb

class Entry(ndb.Model):
	name = ndb.StringProperty(required=True)
	color = ndb.StringProperty(required=True)
	cuisine = ndb.StringProperty(repeated=True)
	num_sibs = ndb.StringProperty(required=True)
#	cubs_win = ndb.BooleanProperty(required=True)