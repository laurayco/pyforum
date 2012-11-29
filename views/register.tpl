<div class="span8 offset2">
	<form method="POST" action="/member">
		<fieldset>
			<legend>Registration.</legend>
			<input type="email" name="email" class="input-block-level" placeholder="email"/>
			<input type="password" name="pass" class="input-block-level" placeholder="password">
			<input type="text" name="name" class="input-block-level" placeholder="username" />
			<span class="help-block">This is optional. This is what members of the community will see as your name.</span>
			<input type="submit" class ="btn btn-primary" value="Register" />
		</fieldset>
	</form>
</div>
%rebase header forum=forum, user=user