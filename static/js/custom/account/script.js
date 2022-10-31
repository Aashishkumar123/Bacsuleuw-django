const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;


const validation_popup = ()=>{
    const config = {
        html: 'Sorry, looks like there are some errors detected, please try again.',
        type: 'error',
        icon: "error",
        confirmButtonText: 'Ok, got it!',    
      };
    sweetAlert.fire(config)
}


const signup = (e,url,success_url)=>{
    e.preventDefault();
    $('#kt_sign_up_submit').html('<span>Please wait... <span class="spinner-border spinner-border-sm align-middle ms-2"></span></span>');

    var first_name = e.target.first_name.value;
    var last_name = e.target.last_name.value;
    var email = e.target.email.value;
    var first_name = e.target.first_name.value;
    var password = e.target.password.value;
    var confirm_password = e.target.confirm_password.value;
    var terms = e.target.terms.checked;
    var account_type = e.target.account_type.value;
    $.ajax({
        url: url,
        type: 'post',
        dataType: 'json',
        data: {
            first_name : first_name,
            last_name : last_name,
            email : email,
            password : password,
            confirm_password : confirm_password,
            terms : terms,
            account_type : account_type,
            csrfmiddlewaretoken: csrftoken
        },
        success: function(data) {
            $('#kt_sign_up_submit').html('<span class="indicator-label">Sign Up</span>')
            $('#first_name-validation').text('');
            $('#last_name-validation').text('');
            $('#email-validation').text('');
            $('#password-validation').text('');
            $('#confirm_password-validation').text('');
            $('#terms-validation').text('');

            if(data.last_name !== undefined){
                $('#last_name-validation').text(data.last_name);
            }
            if(data.email !== undefined){
                $('#email-validation').text(data.email);
            }
            if(data.password !== undefined){
                $('#password-validation').text(data.password);
            }
            if(data.confirm_password !== undefined){
                $('#confirm_password-validation').text(data.confirm_password);
            }
            if(data.terms !== undefined){
                $('#terms-validation').text(data.terms);
            }
            if(data.first_name !== undefined){
                $('#first_name-validation').text(data.first_name);
            }
            if(data.status === 200){
                if(data.accounttype === 'customer'){
                    window.location = success_url
                }else{
                    window.location = '/verify_admin/'
                }
            }
            else{
                validation_popup()
            }
        }
    });
}

const signupbyadmin = (e,url)=>{
    e.preventDefault();
    document.getElementById('spinner-icon').classList.add('fa-spinner');
    document.getElementById('spinner-icon').classList.add('fa-spin');
    var first_name = e.target.first_name.value;
    var last_name = e.target.last_name.value;
    var email = e.target.email.value;
    var first_name = e.target.first_name.value;
    var password = e.target.password.value;
    var confirm_password = e.target.confirm_password.value;
    var terms = e.target.terms.checked;
    var account_type = e.target.account_type.value;
    $.ajax({
        url: url,
        type: 'post',
        dataType: 'json',
        data: {
            first_name : first_name,
            last_name : last_name,
            email : email,
            password : password,
            confirm_password : confirm_password,
            terms : terms,
            account_type : account_type,
            csrfmiddlewaretoken: csrftoken
        },
        success: function(data) {
            document.getElementById('spinner-icon').classList.remove('fa-spinner');
            document.getElementById('spinner-icon').classList.remove('fa-spin');
            $('#first_name-validation').text('');
            $('#last_name-validation').text('');
            $('#email-validation').text('');
            $('#password-validation').text('');
            $('#confirm_password-validation').text('');
            $('#terms-validation').text('');

            if(data.last_name !== undefined){
                $('#last_name-validation').text(data.last_name);
            }
            if(data.email !== undefined){
                $('#email-validation').text(data.email);
            }
            if(data.password !== undefined){
                $('#password-validation').text(data.password);
            }
            if(data.confirm_password !== undefined){
                $('#confirm_password-validation').text(data.confirm_password);
            }
            if(data.terms !== undefined){
                $('#terms-validation').text(data.terms);
            }
            if(data.first_name !== undefined){
                $('#first_name-validation').text(data.first_name);
            }
            if(data.status === 200){
                const config = {
                    html: 'New User Create Successfull',
                    type: 'success',
                    icon: "success",
                    confirmButtonText: 'Ok, got it!',    
                  };
                sweetAlert.fire(config)
                location.reload();
            }
            else{
                validation_popup()
            }
        }
    });
}

const edituserbyadmin = (e,url)=>{
    e.preventDefault();
    document.getElementById('spinner-icon').classList.add('fa-spinner');
    document.getElementById('spinner-icon').classList.add('fa-spin');
    var first_name = e.target.first_name.value;
    var last_name = e.target.last_name.value;
    var email = e.target.email.value;
    var user_id = e.target.user_id.value;
    $.ajax({
        url: url,
        type: 'post',
        dataType: 'json',
        data: {
            first_name : first_name,
            last_name : last_name,
            email : email,
            user_id : user_id,
            csrfmiddlewaretoken: csrftoken
        },
        success: function(data) {
            document.getElementById('spinner-icon').classList.remove('fa-spinner');
            document.getElementById('spinner-icon').classList.remove('fa-spin');

            if(data.status === 200){
                const config = {
                    html: 'User Update Successfull',
                    type: 'success',
                    icon: "success",
                    confirmButtonText: 'Ok, got it!',    
                  };
                sweetAlert.fire(config)
                if(data.account_type == 'customer'){
                    window.location = '/basculeadmin/customers/'
                }
                if(data.account_type == 'employee'){
                    window.location = '/basculeadmin/employee/'
                }
                if(data.account_type == 'agency'){
                    window.location = '/basculeadmin/agency/'
                }
            }
            else{
                validation_popup()
            }
        }
    });
}

const adminsignin = (e,url,success_url)=>{
    e.preventDefault();
    document.getElementById('spinner-icon').classList.add('fa-spinner');
    document.getElementById('spinner-icon').classList.add('fa-spin');

    $('#email-validation').text('');
    $('#password-validation').text('');
    $('#login-failed-msg').text('');

    var email = e.target.email.value;
    var password = e.target.password.value;

    $.ajax({
        url: url,
        type: 'post',
        dataType: 'json',
        data: {
            email : email,
            password : password,
            csrfmiddlewaretoken: csrftoken
        },
        success: function(data) {
            if(data.status == 200){
                window.location = success_url;
            }
            else if(data.error != undefined){
                $('#login-failed-msg').text(data.error);
                validation_popup();
            }
            else{
                $('#email-validation').text(data.email);
                $('#password-validation').text(data.password);
                validation_popup();
            }
            document.getElementById('spinner-icon').classList.remove('fa-spinner');
            document.getElementById('spinner-icon').classList.remove('fa-spin');
        }
    });
}

const signin = (e,url,success_url)=>{
    e.preventDefault();
    $('#kt_sign_in_submit').html('<span>Please wait... <span class="spinner-border spinner-border-sm align-middle ms-2"></span></span>');

    $('#email-validation').text('');
    $('#password-validation').text('');
    $('#login-failed-msg').text('');

    var email = e.target.email.value;
    var password = e.target.password.value;

    $.ajax({
        url: url,
        type: 'post',
        dataType: 'json',
        data: {
            email : email,
            password : password,
            csrfmiddlewaretoken: csrftoken
        },
        success: function(data) {
            if(data.status == 200){
                if(data.account_type == 'customer'){
                    window.location = '/dashboard/customer/equine'
                }
                if(data.account_type == 'employee'){
                    window.location = '/dashboard/employee/'
                }
                if(data.account_type == 'agency'){
                    window.location = '/dashboard/agency/'
                }
            }
            else if(data.error != undefined){
                $('#login-failed-msg').text(data.error);
                validation_popup();
            }
            else{
                $('#email-validation').text(data.email);
                $('#password-validation').text(data.password);
                validation_popup();
            }
            $('#kt_sign_in_submit').html('<span class="indicator-label">Sign In</span>')
        }
    });
}


$(document).ready(function(){

    $('#kt_sign_up_form').on('submit', function(e){
        signup(e,url='/register/',success_url='/verify_email/');
    });


    $('#kt_sign_in_form').on('submit', function(e){
        adminsignin(e,url="/basculeadmin/login/",success_url="/basculeadmin/"); // admin
    });


    $('#kt_sign_up__by_admin_form').on('submit', function(e){
        signupbyadmin(e,url='/basculeadmin/user/register/');  //admin signu
    });

    $('#kt_corporate_sign_in_form').on('submit', function(e){
        signin(e,url='/login/',success_url='/dashboard/agency-dashboard/');
    });

    $('#kt_edit_by_admin_form').on('submit', function(e){
        edituserbyadmin(e,url='/basculeadmin/user/register/',success_url='/dashboard/agency-dashboard/');
    });


    $("#kt_password_reset_form").on('submit', function(e){
        e.preventDefault();
        var email = e.target.email.value;
        var type = e.target.type.value;
        $('#email-validation').text('');
        document.getElementById('spinner-icon').classList.add('fa-spinner');
        document.getElementById('spinner-icon').classList.add('fa-spin');

        $.ajax({
            url: "/reset-password/",
            type: 'post',
            dataType: 'json',
            data: {
                email : email,
                type : type,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(data) {
                if(data.status == 200){
                    const config = {
                        html: 'We have send a password reset link to your email.',
                        type: 'success',
                        icon: "success",
                        confirmButtonText: 'Ok, got it!',    
                      };
                    sweetAlert.fire(config)
                }
                if(data.error != undefined){
                    $('#login-failed-corporate-msg').text(data.error)
                }
                if(data.email !== undefined){
                    $('#email-validation').text(data.email);
                    validation_popup()
                }
                document.getElementById('spinner-icon').classList.remove('fa-spinner');
                document.getElementById('spinner-icon').classList.remove('fa-spin');
            }
        });
    });

    $("#kt_new_password_form").on('submit', function(e){
        e.preventDefault();
        var password = e.target.password.value;
        var confirm_password = e.target.confirm_password.value;
        var password_reset_token = e.target.password_reset_uuid_token.value;
        var terms = e.target.terms.checked;
        var type = e.target.type.value;

        document.getElementById('spinner-icon').classList.add('fa-spinner');
        document.getElementById('spinner-icon').classList.add('fa-spin');

        $('#password-validation').text('');
        $('#confirm_password-validation').text('');
        $('#terms-validation').text('');

        $.ajax({
            url: `/new-password/${password_reset_token}/${type}/`,
            type: 'post',
            dataType: 'json',
            data: {
                password : password,
                confirm_password : confirm_password,
                terms : terms,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(data) {
                if(data.status == 200){
                    const config = {
                        html: 'You have successfully reset your password!',
                        type: 'success',
                        icon: "success",
                        confirmButtonText: 'Ok, got it!',    
                      };
                    sweetAlert.fire(config).then((is_confirm)=>{
                        if(is_confirm){
                            if(data.type == 'customer'){
                                window.location = '/login/'
                            }
                            if(data.type == 'corporate'){
                                window.location = '/corporate-login/'
                            }
                        }
                    })
                }
                if(data.password != undefined){
                    $('#password-validation').text(data.password)
                    validation_popup()
                }
                if(data.confirm_password !== undefined){
                    $('#confirm_password-validation').text(data.confirm_password);
                    validation_popup()
                }
                if(data.terms !== undefined){
                    $('#terms-validation').text(data.terms);
                    validation_popup()
                }
                document.getElementById('spinner-icon').classList.remove('fa-spinner');
                document.getElementById('spinner-icon').classList.remove('fa-spin');
            }
        });
    });

    $("#kt_account_profile_details_form").on('submit', function(e){
        e.preventDefault();
        formdata = new FormData();
        var avatar = e.target.avatar.files[0]
        var fname = e.target.fname.value;
        var lname = e.target.lname.value;
        var company = e.target.company.value;
        var phone = e.target.phone.value;
        var website = e.target.website.value;
        var country = e.target.country.value;
        var address = e.target.address.value;
        var occupation = e.target.occupation.value;
        formdata.append("avatar", avatar)
        formdata.append("fname", fname)
        formdata.append("lname", lname)
        formdata.append("company", company)
        formdata.append("phone", phone)
        formdata.append("website", website)
        formdata.append("country", country)
        formdata.append("address", address)
        formdata.append('occupation',occupation)
        formdata.append("csrfmiddlewaretoken", csrftoken)
        $.ajax({
            url: `/basculeadmin/ajax-profile/settings/`,
            type: 'post',
            dataType: 'json',
            data: formdata,
            processData: false,
            contentType: false,
            success: function(data) {
                if(data.status === 200){
                    const config = {
                        html: 'You have successfully update your account!',
                        type: 'success',
                        icon: "success",
                        confirmButtonText: 'Ok, got it!',    
                      };
                      sweetAlert.fire(config)
                }
            }
        });
    });


    $("#kt_choose_account_form").on('submit', function(e){
        window.location = '/register/'
        // e.preventDefault();
        // if(e.target.kt_create_account_form_account_type_personal.checked){
        //     window.location = '/register/'
        // }
    });
});


function SendPassword(email){
    $.ajax({
        url: "/send-mail-password/",
        type: 'post',
        dataType: 'json',
        data: {
            email : email,
            csrfmiddlewaretoken: csrftoken
        },
        success: function(data) {
            if(data.status == 200){
                const config = {
                    html: 'Email Sended.',
                    type: 'success',
                    icon: "success",
                    confirmButtonText: 'Ok, got it!',    
                  };
                sweetAlert.fire(config)
            }
        }
    });
}


function Searchuser(e,usertype){
        var data = $(`#${e.id}`).val()
        $('#searcheduser').html('')
        $.ajax({
            url: "/basculeadmin/search/user/",
            type: 'GET',
            dataType: 'json',
            data: {
                string : data,
                usertype : usertype,
            },
            success: function(data) {
                console.log(data);
                for (let index = 0; index < data.data.length; index++) {
                    $('#searcheduser').append(`
                    <tr class="odd">
                        <td>
                            <div class="form-check form-check-sm form-check-custom form-check-solid">
                                <input class="form-check-input checkboxinput" onclick="clickcheckbox()" type="checkbox" name="userid" value="{{user.id}}">
                            </div>
                        </td>
                        <td>
                            <a href="{% url 'myadmin:employee_dashboard' user.id %}" class="text-gray-800 text-hover-primary mb-1">${data.data[index].first_name} ${data.data[index].last_name}</a>
                        </td>
    
                        <td>
                            <a href="#" class="text-gray-600 text-hover-primary mb-1">${data.data[index].email}</a>
                        </td>
    
    
                        <td>
    
                            <label class="form-check form-switch form-check-custom form-check-solid">
                                <input class="form-check-input" name="billing" type="checkbox" onclick="AtiveDiactive('1',${data.data[index].id})" id="check" if(${data.data[index].is_active} == 1){ 'checked' } />
                            </label>
                        </td>
    
                        <td>
                            <div class="badge badge-light fw-bold">Yesterday</div>
                        </td>
                        <td>${data.data[index].date_joined}
                        </td>
    
    
                        <td>
                            <a href="/basculeadmin/employee/edit/?id=${data.data[index].id}"  class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm me-1">
                                <span class="svg-icon svg-icon-3">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path opacity="0.3" d="M21.4 8.35303L19.241 10.511L13.485 4.755L15.643 2.59595C16.0248 2.21423 16.5426 1.99988 17.0825 1.99988C17.6224 1.99988 18.1402 2.21423 18.522 2.59595L21.4 5.474C21.7817 5.85581 21.9962 6.37355 21.9962 6.91345C21.9962 7.45335 21.7817 7.97122 21.4 8.35303ZM3.68699 21.932L9.88699 19.865L4.13099 14.109L2.06399 20.309C1.98815 20.5354 1.97703 20.7787 2.03189 21.0111C2.08674 21.2436 2.2054 21.4561 2.37449 21.6248C2.54359 21.7934 2.75641 21.9115 2.989 21.9658C3.22158 22.0201 3.4647 22.0084 3.69099 21.932H3.68699Z" fill="currentColor"></path>
                                        <path d="M5.574 21.3L3.692 21.928C3.46591 22.0032 3.22334 22.0141 2.99144 21.9594C2.75954 21.9046 2.54744 21.7864 2.3789 21.6179C2.21036 21.4495 2.09202 21.2375 2.03711 21.0056C1.9822 20.7737 1.99289 20.5312 2.06799 20.3051L2.696 18.422L5.574 21.3ZM4.13499 14.105L9.891 19.861L19.245 10.507L13.489 4.75098L4.13499 14.105Z" fill="currentColor"></path>
    </svg>
                                </span>
                            </a>
    
                            <a onclick="DeleteUser(${data.data[index].id})"  class="btn btn-icon btn-bg-light btn-active-color-primary btn-sm">
                                <span class="svg-icon svg-icon-3">
                                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path d="M5 9C5 8.44772 5.44772 8 6 8H18C18.5523 8 19 8.44772 19 9V18C19 19.6569 17.6569 21 16 21H8C6.34315 21 5 19.6569 5 18V9Z" fill="currentColor"></path>
                                        <path opacity="0.5" d="M5 5C5 4.44772 5.44772 4 6 4H18C18.5523 4 19 4.44772 19 5V5C19 5.55228 18.5523 6 18 6H6C5.44772 6 5 5.55228 5 5V5Z" fill="currentColor"></path>
                                        <path opacity="0.5" d="M9 4C9 3.44772 9.44772 3 10 3H14C14.5523 3 15 3.44772 15 4V4H9V4Z" fill="currentColor"></path>
                                    </svg>
                                </span>
                            </a>
                        </td>
                    </tr>
    
                `)
    
                }
    
            }
        });
    }



//pagination
function pagenumber(id){
	$('#divcardbody').html('')
	$.ajax({
		type: "GET",
		url: '/basculeadmin/pagination/',
		data: {
			pagenu: id,
		},
		success: function (data) {
			$('#divcardbody').html(data)
		},
    });
}

function Addnewroll(){
    var about_group = document.getElementById('about_group').value;
    var group_pera = document.getElementById('group_pera').value;
    $.ajax({
		type: "POST",
		url: '/basculeadmin/all_groups/',
		data: {
            about_group:about_group,
			group_pera: group_pera,
            csrfmiddlewaretoken: csrftoken,
		},
		success: function(data) {
            if(data.status == 200){
                const config = {
                    html: 'Role Added Success.',
                    type: 'success',
                    icon: "success",
                    confirmButtonText: 'Ok, got it!',    
                  };
                sweetAlert.fire(config)
            }
        }
    });
}

function AddGroupPermition(){
    alert('s');
    var name = document.getElementById('name').value;
    var rolesid = document.getElementById('rolesid[]').value;
    debugger
    var userid = document.getElementById('userid').value;
    $.ajax({
		type: "POST",
		url: '/basculeadmin/create_groups/',
		data: {
            name:name,
			rolesid: rolesid,
            userid:userid,
            csrfmiddlewaretoken: csrftoken,
		},
		success: function(data) {
            if(data.status == 200){
                const config = {
                    html: 'Role Added Success.',
                    type: 'success',
                    icon: "success",
                    confirmButtonText: 'Ok, got it!',    
                  };
                sweetAlert.fire(config)
            }
        }
    });
}