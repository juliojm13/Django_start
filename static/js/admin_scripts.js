window.onload = function () {
    $('.user_age').on('click', 'input[type="number"]', function () {
        var t_href = event.target;

        $.ajax({
            url: "/admin/user/update/" + t_href.name + "/age/" + t_href.value + "/",

            success: function (data) {
                $('.user_age').html(data.result);
            },
        });

        event.preventDefault();
    });
}