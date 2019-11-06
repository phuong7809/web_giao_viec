$(document).ready(function (event) {
    $(":button").click(function (event) {
        let status = event.target.id;
        console.log(status)
        let token = '{{csrf_token}}';
        $.ajax({
            headers: { "X-CSRFToken": token },
            url: '/ajax_get_status/',
            method: 'POST',
            data: {
                'status': status,
            },
            dataType: 'json',
            success: function (data) {
                console.log(data);
                location.reload(true);
            }
        })

    })
})