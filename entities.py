from pydatastore.datastore import Entity,APIEntity
import base58

class Usergroup(Entity):
	template={
		'name':'',
		'description':'',
		'permissons':[]
	}

class Member(APIEntity):
	access_levels=[
		['name','usergroups'],
		['email']
	]
	template={
		'name':'',
		'email':'',
		'password':'',
		'usergroups':[]
	}
	foreign={
		'usergroups':Usergroup.List()
	}
	@property
	def permissions(self):return sum([p.permissions for p in self.usergroups],[])

class OAuthApp(Entity):
	template={
		'secret':'',
		'key':'',
		'name':''
	}
	@property
	def consumer(self):return oauth.Consumer(key=self.key,secret=self.secret)

class OAuthToken(Entity):
	template={
		'secret':'',
		'key':'',
		'user':None,
		'app':None
	}
	foreign={
		'app':OAuthApp.Reference(),
		'user':Member.Reference()
	}

class Post(APIEntity):
	access_levels=[
		['content','owner']
	]
	template={
		'content':'',
		'owner':None
	}
	foreign={
		'owner':Member.Reference()
	}

class Thread(APIEntity):
	access_levels=[
		['name','owner','posts','description']
	]
	template={
		'name':'',
		'owner':None,
		'posts':[],
		'description':''
	}
	foreign={
		'posts':Post.List()
	}
	@property
	def slug(self):return base58.encode( base58.to_base128(self.key))

class Category(APIEntity):
	access_levels=[
		['name','threads','description','tags']
	]
	template={
		'name':'',
		'description':'',
		'tags':[],
		'threads':[]
	}
	foreign={
		'threads':Thread.List()
	}
	@property
	def categories(self):
		return []#A list of 'trending topics'
	@property
	def slug(self):return base58.encode( base58.to_base128(self.key))

class Forum(Entity):
	access_levels=[
		['name','threads','tags','boards','description']
	]
	template={
		'name':'',
		'boards':[],
		'threads':[],
		'tags':[]
	}
	foreign={
		'boards':Category.List(),
		'threads':Thread.List()
	}