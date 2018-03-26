$(document).ready(function(){

	$('.up-vote').on('click', (event)=>{
		// data = +1 or -1 ; user  who clicked it; image that was clicked
		console.log(event);
		let vote_val = 1,
			user_id = event.currentTarget.attributes["data-uid"].value,
			caption_id = event.currentTarget.attributes["data-capt"].value;
		$.ajax({
			url: '/user_vote/',
			type: 'POST',
			data: {vote_val, user_id, caption_id},
			success: function(data){
				console.log(data);
			}
		});
	});

	$('.down-vote').on('click', (event)=>{
		// data = +1 or -1 ; user  who clicked it; image that was clicked
		console.log(event);
	});

	/*
	 * CSRF Token Using jQuery 
	 */
	 function getCookie(name) {
	 	var cookieValue = null;
	 	if (document.cookie && document.cookie != '') {
	 		var cookies = document.cookie.split(';');
	 		for (var i = 0; i < cookies.length; i++) {
	 			var cookie = jQuery.trim(cookies[i]);
	            // Does this cookie string begin with the name we want?
	            if (cookie.substring(0, name.length + 1) == (name + '=')) {
	            	cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	            	break;
	            }
	        }
	    }
	    return cookieValue;
	}
	var csrftoken = getCookie('csrftoken');
	function csrfSafeMethod(method) {
	    // these HTTP methods do not require CSRF protection
	    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
	}
	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		}
	});

});