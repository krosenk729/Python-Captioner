$(document).ready(function(){
	/*
	 * Lazy Load Image
	 */
	 $('.lazy-load').each(function(){
	 	$(this).attr('src', $(this).attr('data-src')).toggleClass('lazy-load');
	 });

	/*
	 * Update DB When Vote Clicked 
	 */

	$('.up-vote').on('click', (event)=>{
		console.log(event);
		let is_zero = event.currentTarget.classList.value.match(/voted/i) ? true: false,
			vote_val = is_zero ? 0 : 1,
			user_id = event.currentTarget.attributes["data-uid"].value,
			caption_id = event.currentTarget.attributes["data-capt"].value;
		$.ajax({
			url: '/user_vote/',
			type: 'POST',
			data: {vote_val, user_id, caption_id},
			success: function(data){
				console.log(data);
				upVoteUpdate(event.currentTarget.nextElementSibling, data);
			}
		});
		$(event.currentTarget).toggleClass('voted');
	});

	/*
	 * Update DB When Vote Clicked 
	 */

	$('.down-vote').on('click', (event)=>{
		console.log(event);
		let vote_val = event.currentTarget.classList.value.match(/voted/i) ? 0 : -1,
			user_id = event.currentTarget.attributes["data-uid"].value,
			caption_id = event.currentTarget.attributes["data-capt"].value;
		$.ajax({
			url: '/user_vote/',
			type: 'POST',
			data: {vote_val, user_id, caption_id},
			success: function(data){
				console.log(data);
				upVoteUpdate(event.currentTarget.previousElementSibling, data);
			}
		});
		$(event.currentTarget).toggleClass('voted');
	});

	/*
	 * Update Vote Avg Shown 
	 */

	 function upVoteUpdate(counter, newval){
	 	$(counter).text(parseFloat(newval));
	 }

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