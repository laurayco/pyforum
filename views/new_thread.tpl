%include header forum=forum
<div class='span4'>
	Welcome, <em>{{user.name}}</em>
	<form method="POST" action="logout">
		<input type='submit' class='btn btn-info' value="Logout"/>
	</form>
</div>
<div class='span8'>
	<form method="POST"><fieldset>
		<legend>New Thread</legend>
		<input type='text' name='name' class='input-block-level' placeholder='title'/>
		<textarea rows=10 name='content' class='input-block-level' placeholder='content'></textarea>
		<input type='text' name='tags' class='input-block-level' placeholder='tags'/>
		<input type='submit' value='Create' class='btn btn-info'/>
		<span class='help-block'>
			Tags are seperated by spaces.
		</span>
	</fieldset></form>
</div>
%include footer forum=forum