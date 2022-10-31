const changemode = (mode)=>{
    $.ajax({
        url: '/change-mode/',
        type: 'POST',
        dataType: 'json',
        data: {
            mode:mode,
            csrfmiddlewaretoken: csrftoken
        },
        success: function(data) {
            if(data.status === 200){
                location.reload();
            }
        }
    });
}
