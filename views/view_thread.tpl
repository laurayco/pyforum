%for post in thread.posts:
<div class='post row'>
	<div class='info span2'>
		<div class='avatar'>
			<img src="{{post.owner.avatar}}"/>
			<strong>{{post.owner.name}}</strong>
		</div>
	</div>
	<div class='content span6'>
		{{post.content}}
	</div>
</div>
%end
<div class='new-post row'>
	<div class='span8'>
		<form action="post" method="POST"><fieldset>
			<legend>Quick Reply</legend>
			<textarea name='content' class='input-block-level' rows='5'></textarea>
			<input type='submit' value="Post" class='btn btn-primary'/>
		</fieldset></form>
	</div>
</div>
%rebase header forum=forum, user=user