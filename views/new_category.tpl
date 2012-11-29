%include header forum=forum, user=user
<div class='span8'>
	<div class='span8'>
		<form method="POST"><fieldset>
			<legend>New Category</legend>
			<input type='text' name='name' class='input-block-level' placeholder='name'/>
			<input type='text' name='desc' class='input-block-level' placeholder='description'/>
			<input type='text' name='tags' class='input-block-level' placeholder='tags'/>
			<input type='submit' value='Create' class='btn btn-info'/>
			<span class='help-block'>
				Tags are seperated by spaces.
			</span>
		</fieldset></form>
	</div>
</div>
%include footer forum=forum