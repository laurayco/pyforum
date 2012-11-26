from pydatastore.datastore import Entity,APIEntity
from tagger import Tagger
import base58
from hashlib import md5

tagger = Tagger()
extract_tags = lambda src:[s.string for s in src]

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
			

class Category(APIEntity):
	trend_cutoff = -1
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