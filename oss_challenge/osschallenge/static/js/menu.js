$( window ).on("load", function() {
    $(".language-selection").on("click", function() {
        $('#language-input').attr('value', $(this).attr('id'));
        $('#language-form').submit();
    });
});
