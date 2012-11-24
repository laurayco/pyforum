%include header forum=forum
<div class='span4'>
	Welcome, <em>{{user.name}}</em>
	<form method="POST" action="logout">
		<input type='submit' class='btn btn-info' value="Logout"/>
	</form>
</div>
<div class='span8'>
	%for post in thread.posts:
	<div class='row'>
	<div class='span4'>
		{{post.owner.name}}
	</div>
	<div class='span8'>
		{{post.content}}
	</div>
	</div>
	%end
	<div class='row'>
		<div class='span12'>
			<form action="post" method="POST"><fieldset>
				<legend>Quick Reply</legend>
				<textarea name='content' class='input-block-level' rows='5'></textarea>
				<input type='submit' value="Post" class='btn btn-primary'/>
			</fieldset></form>
		</div>
	</div>
</div></div>
%include footer forum=forum