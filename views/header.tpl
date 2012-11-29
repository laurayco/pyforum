%setdefault("title",forum.name)
%setdefault("active_page","")
%setdefault("pages",[])
%setdefault("tags",[])
%setdefault("theme_name","metro")
%from entities import Theme
%from pydatastore.datastore import Query
%theme_name = theme_name.lower()
%theme = Query(Theme,lambda n:n.name.lower()==theme_name).fetch_one()
<html>
	<head>
		%for css in theme.css:
		<link rel="stylesheet" href="/s/css/{{css}}" />
		%end
		%for js in theme.js:
		<script type="text/javascript" src="/s/js/{{js}}"></script>
		%end
		<title>{{title}}</title>
	</head>
	<body>
		<div class='body_area container-fluid'><div class='row'>
			%include sidebar user=user,forum=forum
			<div class='span8 main_content'>
			%include
			</div>
		</div></div>
		<div class="footer container-fluid"><div class='row-fluid'>
			<div class="span3">
				Forum Affiliates:
			</div>
			<div class="span3">
				External Links:
			</div>
			<div class="span3">
				Some Boring stuff, like copyrights.
			</div>
			<div class="span3">
				<p>{{forum.name}} is powered by Hotwords software, written
				by Tyler Elric. 2012.</p>
			</div>
		</div></div>
		<script type='text/javascript' src="/s/js/bootstrap.js"></script>
	</body>
</html>