window.addEventListener('load', function() {
    // Load select2 for rating
    $(".select2").select2();
    
    // Load Select2, with tags (dynamic option creation)
    $(".select2[multiple]").select2({
	tags: true
    });
});
