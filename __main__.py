from __future__ import print_function
from bottle import route,template,run,static_file
import bottle
from pydatastore.datastore import Query
from difflib import SequenceMatcher
from entities import Member, Forum, Category, Post, Thread
import base58 as encrypt

def decrypt(k):return encrypt.from_base128(encrypt.decode(k))

def parse_tags(t):return [a.strip() for a in t.split() if len(a.strip())>0]

def similar_filter(cmp,attr,close=.85):
	cmp = cmp.lower()
	seq = SequenceMatcher(isjunk=lambda x:x in " \n\t\r",a=cmp)
	def filter(elem):
		seq.set_seq2(elem.__getattr__(attr).lower())
		return seq.ratio() >= close
	return filter

def active_user():
	id=bottle.request.get_cookie("user",None)
	if id:
		ret = Member.load(id)
		passw = bottle.request.get_cookie("pass")
		if ret.password==passw:
			return ret

def has_permission(user,permission):return user.has_permission(permission) if user else False

def get_oath_token(app):return Query(OAuthApp,similar_filter(app,"name")).fetch_one()

def flash_message(message,target,title=None,duration=3):
	title = title or "Information"
	data={}
	data['name'] = title
	data['target'] = target
	data['message'] = message
	data['duration'] = duration
	data['forum'] = Forum.load(forum_key())
	return template("flash_message",**data)

def forum_key():return "1"

pending_activations = {}

@route('/')
def index_page():
	bottle.TEMPLATES.clear()
	user = active_user()
	data={}
	if user is None:
		msg = "You need to sign in before you can use this app."
		return flash_message(msg,"/login","Login Required")
	data['user'] = user
	data['forum'] = Forum.load(forum_key())
	return template('home',**data)

@route("/thread/:key")
@route("/thread/:key/")
def thread_view(key):
	thread = Thread.load(decrypt(key))
	forum = Forum.load(forum_key())
	user = active_user()
	return template("view_thread",forum=forum,user=user,thread=thread)

@route("/category/:key")
@route("/category/:key/")
def category_page(key):
	key=decrypt(key)
	user=active_user()
	forum = Forum.load(forum_key())
	board = Category.load(key)
	data={}
	data['user']=user
	data['forum']=forum
	data['threads']=board.threads
	data['trends']=board.topics
	data['tags'] = board.tags
	data['mode']='trending'
	return template("home",**data)

@route("/thread/")#Create a new thread
@route("/thread")#At the forum-level
@route("/category/:key/thread/")#At a category level.
@route("/category/:key/thread")
def new_thread_form(key=None):
	user = active_user()
	if has_permission(user,"new-thread"):
		forum = Forum.load(forum_key())
		target = Category.load(decrypt(key)) if key else forum
		return template("new_thread",target=target,user=user,forum=forum)
	raise bottle.HTTPError(404,
	"""Sorry, but we weren't able to find what you were looking for.
	  I hope that someday you do find it, but when you do, it won't be here.
	""")


@route("/thread/",method="POST")#Create a new thread
@route("/thread",method="POST")#At the forum-level
@route("/category/:key/thread/",method="POST")#At a category level.
@route("/category/:key/thread",method="POST")
def new_thread(key=None):
	user = active_user()
	if has_permission(user,'new-thread'):
		new_thread = Thread()
		first_post = Post()
		name = bottle.request.forms.get("name")
		content = bottle.request.forms.get("content")
		tags = parse_tags(bottle.request.forms.get("tags",""))
		first_post.update({
			"owner":user.key,
			"content":content
		})
		new_thread.update({
			"name":name,
			"owner":user.key,
			"posts":[first_post.key],
			"tags":tags
		})
		forum = Forum.load(forum_key())
		target = Category.load(decrypt(key)) if key else forum
		target.threads.append(new_thread.key)
		target.save()
		new_thread.save()
		return flash_message("Your thread has been created.","/thread/"+new_thread.slug+"/","Success")
	raise bottle.HTTPError(404,
	"""Sorry, but we weren't able to find what you were looking for.
	  I hope that someday you do find it, but when you do, it won't be here.
	""")

@route("/thread/:key/post",method="POST")
@route("/thread/:key/post/",method="POST")
def submit_post(key):
	user = active_user()
	if has_permission(user,'create-post'):
		post = Post()
		thread = Thread.load(decrypt(key))
		content = bottle.request.forms.get("content","").strip()
		assert len(content)>0
		post.update({"content":content,"owner":user.key})
		thread.posts.append(post)
		thread.save()
		post.save()

@route("/category")
def create_category_form():
	user = active_user()
	forum = Forum.load(forum_key())
	if has_permission(user,'create-board'):
		return template("new_category",forum=forum,user=user)
	raise bottle.HTTPError(404,
	"""Sorry, but we weren't able to find what you were looking for.
	  I hope that someday you do find it, but when you do, it won't be here.
	""")

@route("/category",method="POST")
def submit_category():
	name = bottle.request.forms.get("name")
	user = active_user()
	if not has_permission(user,'create-board'):
		return flash_message("You're not allowed to do that!","/","Error")
	elif name is None or len(name)<1:
		return flash_message("You need to enter a name!","/category","Error")
	else:
		tags = bottle.request.forms.get("tags","")
		description = bottle.request.forms.get("desc","")
		MIN_TAG_LENGTH = 3
		tags = [t.strip() for t in tags.split() if len(t.strip())>=MIN_TAG_LENGTH]
		board = Category()
		board.update({"name":name,"tags":tags,"description":description})
		return flash_message("Your board has been created!","/category/"+board.key,"Success")

@route("/login")
def login():return template("login",forum=Forum.load(forum_key()))

@route("/login",method="POST")
def set_user():
	user = bottle.request.forms.get("user",None)
	password = bottle.request.forms.get("pass",None)
	assert user is not None and password is not None
	correct_pass = lambda member:member.password==password
	correct_email = lambda member:member.email.lower()==user.lower()
	q = Query(Member,correct_pass,correct_email)
	user = q.fetch_one()
	if user is None:return "No such user, or incorrect password. Looser."
	else:
		bottle.response.set_cookie("user",user.key)
		bottle.response.set_cookie("pass",password)
		msg="You have been successfully logged in."
		return flash_message(msg,"/","Success")

@route("/login",method="DELETE")
def logout():
	bottle.response.delete_cookie("user")
	msg = "You have been logged out."
	return flash_message(msg,"/","Success")

@route("/logout",method="POST")
def proxy_logout():return logout()

@route("/member")
def register():return template("register",forum=Forum.load(forum_key()))

@route("/member",method="POST")
def make_member():
	email = bottle.request.forms.get("email",None)
	passw = bottle.request.forms.get("pass",None)
	name = bottle.request.forms.get("name",None)
	new_user = Member()
	new_user.update({"email":email,"password":passw,"name":name})
	new_user.save()
	return flash_message("You have registered! Now go sign in.","/login","Success")

@route('/s/:dir/:fn')
def serve_file(dir,fn):return static_file(fn,root=dir)

@route('/favicon.ico')
def favicon():return serve_file("./","favicon.ico")

bottle.debug(True)
run(reloader=True,host='0.0.0.0')