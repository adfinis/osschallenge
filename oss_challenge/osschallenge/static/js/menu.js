$( window ).on("load", function() {
    $(".language-selection").each(function() {
        $(this).on("click", function() {
            $('#language-input').attr('value', $(this).attr('id'));
            $('#language-form').submit();
        });
    });
});
