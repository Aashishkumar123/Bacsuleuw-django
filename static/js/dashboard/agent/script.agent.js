const getDocument = ()=>{
    $('#loading-document').removeClass('d-none');
    $('#document-preparing').addClass('d-none');
    $.ajax({
        url: '/dashboard/agency/get-document/',
        type: 'POST',
        dataType: 'json',
        data: {
            agency_name: $('#agency_name').val(),
            agency_address: $('#agency_address').val(),
            commissions: $('#commissions').val(),
            state: $('#state').val(),
            city: $('#city').val(),
            zip: $('#zip').val(),
            csrfmiddlewaretoken:csrftoken
        },
        success: function(data) {
            setTimeout(()=>{
                $('#loading-document').addClass('d-none');
                $('#document-preparing').removeClass('d-none');
                console.log(data);
            },3000)
        }
    })
}


const signDocument = ()=>{
    window.location = 'https://account-d.docusign.com/oauth/auth?response_type=code&scope=signature%20impersonation&client_id=96aa2b6a-cc5c-4031-9d2d-7cbe1a4d4c0a&redirect_uri=http://127.0.0.1:8000/auth/docusign/callback'                   
}


function randomString(len, charSet) {
    charSet = charSet || 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    var randomString = '';
    for (var i = 0; i < len; i++) {
        var randomPoz = Math.floor(Math.random() * charSet.length);
        randomString += charSet.substring(randomPoz,randomPoz+1);
    }
    return randomString;
}


const addmorelicenseDocument = ()=>{
    const random = randomString(10)
    $('#license-document').append(
       `<br />
       <div id="${random}div">
        <input type="file" name="license-input" id="${random}file">
        <a id="${random}" class="text-danger" onclick="removeDocument(id)"><i class="fa-regular fa-trash-can"></i></a>
       <div>`
    )
}


const addmoreotherDocument = ()=>{
    const random = randomString(10)
    $('#other-document').append(
        `<br />
        <div id="${random}div">
            <input id="document-name" type="text" class="form-control form-control-lg form-control-solid" placeholder="Document name">
            <br>
            <input type="file" id="${random}file">
            <a id="${random}" class="text-danger" onclick="removeDocument(id)"><i class="fa-regular fa-trash-can"></i></a>
        </div>
        `
    )
}


$('#documentType').on('change', function() {
    if(this.value == 'Others'){
        $('#other-document').removeClass('d-none');
        $('#other-document-btn').removeClass('d-none');
        $('#license-document').addClass('d-none');
        $('#license-document-btn').addClass('d-none');
    }
    if(this.value == 'State License'){
        $('#other-document').addClass('d-none');
        $('#other-document-btn').addClass('d-none');
        $('#license-document').removeClass('d-none');
        $('#license-document-btn').removeClass('d-none');
    }
});


const removeDocument = (id)=>{
    $(`#${id}div`).css('display','none');
}


$("#license-file").on('change',(e)=>{
    const license = e.target.files[0];
    const state_license = $("#state-license").val();

    formdata = new FormData();
    formdata.append('license',license);
    formdata.append('state_license',state_license)
    $.ajax({
        url: `/dashboard/agency/upload-document/`,
        type: 'post',
        dataType: 'json',
        data: formdata,
        processData: false,
        contentType: false,
        success: function(data) {
            $(`#${e.target.id}`).val('');
            $("#document-progress").removeClass('d-none');
            const loading_value = ['30%','50%','80%','100%']
            for (let index = 0; index < loading_value.length; index++) {
                setTimeout(() => {
                    $("#progress-value").css('width',loading_value[index]);
                    $("#progress-percentage").text(loading_value[index]);
                }, 3000);
            }
            setTimeout(() => {
                $("#document-progress").addClass('d-none');
            }, 2000);

            $("#all-license").append(
                ` <div>
                    <i class="fa-solid fa-file-circle-check"></i> 
                    <a href="${data.license}" target="_blank">${data.license}</a>
                </div>
                `
            )
        }
    });
})



$("#other-document-file").on('change',(e)=>{
    const document = e.target.files[0];
    const name = $("#document-name").val();

    formdata = new FormData();
    formdata.append('document',document);
    formdata.append('name',name)
    $.ajax({
        url: `/dashboard/agency/upload-document/`,
        type: 'post',
        dataType: 'json',
        data: formdata,
        processData: false,
        contentType: false,
        success: function(data) {
            $(`#${e.target.id}`).val('');
            $("#document-name").val('');
            $("#document-progress").removeClass('d-none');
            const loading_value = ['30%','50%','80%','100%']
            for (let index = 0; index < loading_value.length; index++) {
                setTimeout(() => {
                    $("#progress-value").css('width',loading_value[index]);
                    $("#progress-percentage").text(loading_value[index]);
                }, 3000);
            }
            setTimeout(() => {
                $("#document-progress").addClass('d-none');
            }, 2000);

            $("#all-documents").append(
                ` <div>
                    <i class="fa-solid fa-file-circle-check"></i> 
                    <a href="${data.license}" target="_blank">${data.license}</a>
                </div>
                `
            )
        }
    });
})
