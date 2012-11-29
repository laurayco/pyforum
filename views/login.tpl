<form method="POST" action="/login">
	<fieldset>
		<legend>You need to login.</legend>
		<input type="email" name="user" class="input-block-level" placeholder="email"/>
		<input type="password" name="pass" class="input-block-level" placeholder="password">
		<input type="submit" class ="btn btn-primary" value="Login" />
		<a href="/member" class="btn btn-info">Register</a>
	</fieldset>
</form>
%rebase header forum=forum, user=user