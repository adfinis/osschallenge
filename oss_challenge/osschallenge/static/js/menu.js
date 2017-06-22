function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$( window ).on("load", function() {
    $(".language-selection").each(function() {
        $(this).on("click", function() {
            var csrftoken = Cookies.get('csrftoken');
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });
            $.ajax({
                method: "POST",
                url: "/i18n/setlang/",
                context: $(document),
                data: { language: $(this).attr('id')}
            }).done(function(msg) {
                location.reload();
            });
        });
    });
});
