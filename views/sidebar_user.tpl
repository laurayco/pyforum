<ul class="nav nav-list">
  <li class="nav-header">Welcome, {{user.name}}</li>
  <li><a href='/usercp'>Options</a></li>
  <li><a href='/avatar'>Change Avatar</a></li>
  <li><a href='/logout'>Log out</a></li>
  <li class="nav-header">{{forum.name}}</li>
  %for category in forum.boards:
  <li class='' title='{{forum.name}}'>
	<a href='/'>Home</a>
  </li>
  <li class='' title='{{category.description}}'>
	<a href='/category/{{category.slug}}/'>{{category.name}}</a>
  </li>
  %end
  <li class="divider"></li>
	#if user.has_permission("new-thread"):
	<li title='Create a new thread!'><a href='thread'>New Thread</a></li>
	#end
	#if user.has_permission("new-category"):
	<li title='Create a new category!'>
		<a href='/category'>New Category</a>
	</li>
	#end
</ul>