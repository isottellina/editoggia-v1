// Has the multi-chapter part of the form already been revealed?
already_revealed = false;

window.addEventListener('load', function() {
    // If checkbox is already checked (by the browser),
    // reveal the div.
    if ($("#multi-chapter").is(':checked')) {
	$("#multi-chapter-reveal").show();
	already_revealed = true;
    }
    
    // Bind event to checkbox
    $("#multi-chapter").bind('change', function() {
	$("#multi-chapter-reveal").toggle();

	if (!already_revealed) {
	    // If this is the first time we reveal this part,
	    // set the total_chapters field to '?', because
	    // it should be the default for multi-chapter fics.
	    $("[name=total_chapters]").val('?');
	    already_revealed = true;
	}
    })
});
