<html>
	<head>
		<link rel="stylesheet" href="/s/css/bootstrap.css" type="text/css" />
		<link rel="stylesheet" href="/s/css/bootstrap-responsive.css" type="text/css" />
		<link rel="stylesheet" href="/s/css/style.css" type='text/css' />
		<script type="text/javascript" src="/s/js/jquery.js"></script>
		%setdefault("title",forum.name)
		%setdefault("active_page","")
		%setdefault("pages",[])
		<title>{{title}}</title>
	</head>
	<body>
		<div class='body_area container-fluid'><div class='row'>
			<div class='span4'><div class='sidebar-fixed hidden-phone'>
				%include sidebar user=user,forum=forum
			</div><div class='sidebar visible-phone'>
				%include sidebar user=user,forum=forum
			</div></div>
			<div class='span8 main_content'>