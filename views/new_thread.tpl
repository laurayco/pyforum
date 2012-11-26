%include header forum=forum,user=user
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
%include footer forum=forum