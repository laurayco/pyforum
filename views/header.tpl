<html>
	<head>
		<link rel="stylesheet" href="/s/css/bootstrap.css" type="text/css" />
		<script type="text/javascript" src="/s/js/jquery.js"></script>
		%setdefault("title",forum.name)
		%setdefault("active_page","")
		%setdefault("pages",[])
		<title>{{title}}</title>
	</head>
	<body>
		<div class="navbar navbar-static-top">
			<div class="navbar-inner">
				<a class="brand" href="#">{{forum.name}}</a>
				<ul class="nav">
				%for page in pages:
					%if page[0].lower()==active_page.lower():
					<li class='active'>
						<a href="{{page[0]}}">{{page[1]}}</a></li>
					%else:
					<li>
						<a href="{{page[0]}}">{{page[1]}}</a>
					</li>
					%end
				%end
				</ul>
			</div>
		</div>
		<div class='container-fluid'><div class='row-fluid'>