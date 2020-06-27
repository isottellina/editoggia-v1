// Code that has to be loaded on a Story page.
window.addEventListener('load', function() {
    // Configure like link
    $("#like-button").bind('click', function(e) {
	// Submit the form by hand
	$.post(
	    $("#like-form").attr('action'),
	    $("#like-form").serialize(),
	    success=function() {
		let icon = $("#like-button").find("[data-fa-i2svg]");
		
		if (icon.attr("data-prefix") == "far") {
		    icon.attr("data-prefix", "fas");
		} else {
		    icon.attr("data-prefix", "far");
		}
	    }
	);
    });

    // Configure button to show comment form
    $("#comment-appear").bind('click', function(e) {
	console.log($("#comment-form"));
	$("#comment-form").toggle();
    });
});
