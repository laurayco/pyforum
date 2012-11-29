<div class='span4'>
%if user is not None:
%include sidebar_user forum=forum,user=user
%end
%include sidebar_public forum=forum
</div>