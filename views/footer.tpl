%setdefault('tags',[])
</div>
<div class="footer container-fluid"><div class='row-fluid'>
	<div class="span3">
	%if len(tags)>0:
		<h4>Tag Cloud</h4>
		<ul class='tags cloud'>
		%for tag in tags:
			<li>
			%include tag_link tag=tag
			</li>
		%end
		</ul>
	%end
	</div>
	<div class="span3">B</div>
	<div class="span3">C</div>
	<div class="span3">D</div>
</div></div>
<script type='text/javascript' src="/s/js/bootstrap.js"></script>
	</body>
</html>