from pydatastore.datastore import Entity,APIEntity
from tagger import Tagger
import base58
from hashlib import md5

tagger = Tagger()
extract_tags = lambda src:[s.string for s in src]

class Usergroup(Entity):
	template={
		'name':'',
		'description':''
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
		'usergroups':[],
		'_reputation':[]#Will only be 1 or -1.
	}
	foreign={
		'usergroups':Usergroup.List()
	}
	@property
	def permissions(self):return sum([p.permissions for p in self.usergroups],[])
	@property
	def reputation(self):
		reputation = self._reputation[:]
		return int(sum(reputation)/len(reputation)*100) if len(reputation)>0 else 50
	@property
	def avatar(self):
		hash = md5()
		hash.update(self.email.encode('utf-8'))
		hash = hash.hexdigest()
		optionstring = "d=retro&r=r&s=512"
		url = "http://www.gravatar.com/avatar/" + hash + ".jpg?" + optionstring
		return url
	def has_permission(self,permission):
		return 'all' in self.permissions or permission in user.permissions

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

class Score(Entity):
	template={
		'owner':None,
		'value':0
	}
	foreign={'owner':Member.Reference()}
	@property
	def weight(self):return int(self.owner.reputation * self.value)

class Post(APIEntity):
	access_levels=[
		['content','owner']
	]
	template={
		'content':'',
		'owner':None,
		'tags':[],
		'scores':[]
	}
	foreign={
		'owner':Member.Reference(),
		'scores':Score.List()
	}
	def update(self,dat):
		if 'content' in dat:#Updating the content field.
			new_tags = extract_tags(tagger(dat['content']))#Lol. dat content.
			if 'tags' in dat:dat['tags'].extend(new_tags)
			elif len(self.tags)>0:self.tags.extend(new_tags)
			else:dat['tags'] = new_tags
		return super(Post,self).update(dat)
	@property
	def score(self):
		scores=self.dat['scores']
		if len(scores)>0:
			return int(sum(score.weight for score in self.scores)//len(scores))
		return 50

class Thread(APIEntity):
	word_limit = -1
	tag_strength = 2
	access_levels=[
		['name','owner','posts','description']
	]
	template={
		'name':'',
		'owner':None,
		'posts':[],
		'description':'',
		'tags':[]
	}
	foreign={
		'posts':Post.List()
	}
	@property
	def slug(self):return base58.encode( base58.to_base128(self.key))
	@property
	def hot_words(self):
		word_score = {}
		for post in self.posts:
			for tag in post.tags:
				word_score[tag] = word_score.get(tag,0)+1
		sort=sorted(word_score.items(),key=lambda word:-1*word[1])
		tag_strength = self.tag_strength * sort[0][1] if len(sort)>0 else self.tag_strength
		for tag in self.tags:
			word_score[tag] = word_score.get(tag,0) + tag_strength
		word_score=sorted(word_score.items(),key=lambda word:-1*word[1])
		total,max = 0,self.word_limit
		for word in word_score:
			if max>-1:
				if total>=max:break
				total+=1
			yield word

class AccessException(Entity):
	template={
		'permissions':[],
		'usergroup':None#Applies to everybody, including public members
	}
	foreign={
		'usergroup':Usergroup.Reference()
	}

class Access(Entity):
	template={
		'default':None,
		'exceptions':[]
	}
	foreign={
		'exceptions':AccessException.List(),
		'default':AccessException.Reference()
	}
	def has_permission(self,user,permission):
		d = self.default
		ugs = user.usergroups if user else None
		#There are default rules, it's not a public area, silly willy.
		public = True if d is None else permission in d.permissions
		if public:return True
		#Okay, not public, does the user have a user group with permission to read?
		shared = [a for a in self.exceptions if a.usergroup in user.usergroups]
		for access in shared:#All relevant access permissions.
			if access.usergroup:#Use 'none' as a flag to say, no, you CAN'T read this. :P
				if 'read' in access.permissions:
					return True
		return False

class Category(APIEntity):
	trend_cutoff = -1
	access_levels=[
		['name','threads','description','tags']
	]
	template={
		'name':'',
		'description':'',
		'tags':[],
		'threads':[],
		'access':None
	}
	foreign={
		'threads':Thread.List(),
		'access':Access.Reference()
	}
	def topics(self,user):
		def fetch_hotwords():
			r={}
			for thread in self.threads:
				for word,score in thread.hot_words:
					r[word]=r.get(word,0)+score
			return sorted(r.items(),key=lambda i:-1*i[1])
		def gen():
			i,max=0,self.trend_cutoff
			for word,score in fetch_hotwords():
				if max>-1:
					if i>=max:break
					i+=1
				yield word
		if self.access:
			if self.access.has_permission(user,'list'):
				gen()
		else:gen()
	def list_threads(self,user):
		def fetch_hotwords():
			r={}
			for thread in self.threads:
				for word,score in thread.hot_words:
					r[word]=r.get(word,0)+score
			return sorted(r.items(),key=lambda i:-1*i[1])
		for thread in self.threads:
			yield thread
		if self.access:
			if self.access.has_permission(user,'list'):
				gen()
		else:gen()
	def has_permission(self,user,permi):
		if self.access:
			return self.access.has_permission(user,permi)
		return True
	@property
	def slug(self):return base58.encode( base58.to_base128(self.key))

class Theme(Entity):
	template={
		'css':[],
		'js':[],
		'name':"",
		'author':''
	}

class Forum(Entity):
	trend_cutoff = -1
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
	@property
	def topics(self):
		def fetch_hotwords():
			r={}
			for thread in self.threads:
				for word,score in thread.hot_words:
					r[word]=r.get(word,0)+score
			return sorted(r.items(),key=lambda i:-1*i[1])
		i,max=0,self.trend_cutoff
		for word,score in fetch_hotwords():
			if max>-1:
				if i>=max:break
				i+=1
			yield word