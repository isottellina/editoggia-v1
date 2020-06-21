function like_link (story_id) {
    $.post(
	'/ajax/story/like',
	{
	    "story": story_id
	},
	success=function() {
	    let icon = $("#like-link").find("[data-fa-i2svg]");
	    
	    if (icon.attr("data-prefix") == "far") {
		icon.attr("data-prefix", "fas");
	    } else {
		icon.attr("data-prefix", "far");
	    }
	}
    );
}
