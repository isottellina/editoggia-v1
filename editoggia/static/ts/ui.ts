declare var $: any;

window.onload = () => {
    console.log($("#like-link > i"));
    
    $("#like-link").click(
	() => {
	    let icon = $("#like-link").find("[data-fa-i2svg]");
	    
	    if (icon.attr("data-prefix") == "far") {
		icon.attr("data-prefix", "fas");
	    } else {
		icon.attr("data-prefix", "far");
	    }
	}
    );
};
