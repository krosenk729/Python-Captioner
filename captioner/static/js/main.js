$(document).ready(function(){
	/*
	 * Lazy Load Image
	 */
	 $('.lazy-load').each(function(){
	 	$(this).attr('src', $(this).attr('data-src')).toggleClass('lazy-load');
	 });


	/*
	 * Listen for Votes 
	 */
	$('.up-vote').on('click', function(event){
		handleVote(event, 1);
	});
	$('.down-vote').on('click', function(event){
		handleVote(event, -1);
	});


	/*
	 * Post Vote to Endpoint 
	 */

	function handleVote(event, which){
		let is_zero = event.currentTarget.classList.value.match(/voted/i) ? true: false,
			vote_val = is_zero ? 0 : which,
			user_id = event.currentTarget.attributes["data-uid"].value,
			caption_id = event.currentTarget.attributes["data-capt"].value,
			upvote_ref = which > 0 ? event.currentTarget.nextElementSibling : event.currentTarget.previousElementSibling;
		$.ajax({
			url: '/user_vote/',
			type: 'POST',
			data: {vote_val, user_id, caption_id},
			success: function(data){
				console.log(data);
				upVoteUpdate(upvote_ref, data);
			}
		});
		$(event.currentTarget).siblings().removeClass('voted');
		$(event.currentTarget).toggleClass('voted');
	}


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