%setdefault('boards',forum.boards)
%setdefault('tags',forum.tags)
%setdefault('threads',forum.threads)
%setdefault('mode','overview')
%include header forum=forum,user=user
	%if mode=='overview':
		%if len(boards)<1:#>
		<div class='row'><div class='span6'>
			There aren't any categories to post in!
		</div><div class='span2'>
			%if 'all' in user.permissions or 'create-category' in user.permissions:
			<a href='category'>Create a New Category!</a>
			%end
		</div></div>
		%end
		%for category in boards:
		<div class='category row'>
			<div class='span8'>
				<h3><a href='category/{{category.slug}}/'>{{category.name}}</a></h3>
				%if len(category.description)>0:
					<h4>{{category.description}}</h4>
				%end
				%topics = list(category.topics)
				%if len(topics)>0:
					<ul class='tags clearfix'>
					%for tag in topics:
					<li>
						%include tag_link tag=tag
					</li>
					%end
				</ul>
			</div>
			<div class='span4'>
				[ extraneous info ]
			</div>
		</div>
		%end
	%end
	%elif mode=='trending':
		<div class='trend row'><div class='span8'>
		%for topic in trends:
			%include tag_link tag=topic
		%end
		</div></div>
	%end
	%for thread in threads:
		<div class='thread row'>
			<div class='span4'>
				<h1><a href='/thread/{{thread.slug}}/'>{{thread.name}}</a></h1>
				%if len(thread.description)>0:
					<p>{{thread.description}}</p>
				%end
			</div>
			<div class='span4'>
				Post Count / Participants
				Most Recent Post
			</div>
			<div class='span4'>
				%for topic in thread.tags:
					%include tag_link tag=topic
				%end
			</div>
		</div>
	%end
	%if len(threads)<1:#>
		<div class='span8'>
			<h2>There aren't any threads here!</h2>
			<p>Be the first to <a href='thread/'>create a thread!</a></p>
		</div>
	%end
%include footer forum=forum, tags=tags