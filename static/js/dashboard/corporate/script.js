// Corporate dashboard js code
//const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

const userAction = (url,email,type)=>{
    $.ajax({
        url: url,
        type: 'post',
        dataType: 'json',
        data: {
            email : email,
            csrfmiddlewaretoken: csrftoken
        },
        success: function(data) {
            if(data.status === 200){
                const config = {
                    html: `Successfully ${type} Customer.`,
                    type: 'success',
                    icon: "success",
                    confirmButtonText: 'Ok, got it!',    
                  };
                sweetAlert.fire(config)
            }
        }
    });
}

const activate_user = (email)=>{
    userAction(
        url = '/dashboard/customer-listing/activate-customer/',
        email = email,
        type = 'activate'
        )
}


const deactivate_user = (email)=>{
    userAction(
        url = '/dashboard/customer-listing/deactivate-customer/',
        email = email,
        type = 'deactivate'
        )
}


function AtiveDiactive(status,id){
    $.ajax({
        url: '/basculeadmin/active_user/',
        type: 'POST',
        dataType: 'json',
        data: {
            id : id,
            status: status,
            csrfmiddlewaretoken: csrftoken
        },
        success: function(data) {
            if(data.status === 200){
                const config = {
                    html: `Successfully Update Customer.`,
                    type: 'success',
                    icon: "success",
                    confirmButtonText: 'Ok, got it!',    
                  };
                sweetAlert.fire(config)
            }
            //location.reload();
        }
    });
}

function DeleteUser(id){
    var result = confirm("Are You Sure. You Want to delete?");
    if (result) {
        $.ajax({
            url: '/basculeadmin/delete_user/',
            type: 'POST',
            dataType: 'json',
            data: {
                id : id,
                csrfmiddlewaretoken: csrftoken
            },
            success: function(data) {
                if(data.status === 200){
                    const config = {
                        html: `Successfully Delete Customer.`,
                        type: 'success',
                        icon: "success",
                        confirmButtonText: 'Ok, got it!',    
                    };
                    sweetAlert.fire(config)
                }
                location.reload();
            }
        });
    }
}

function clickcheckbox(){
    var a_smpid = [];
    $.each($("input[name='userid']:checked"), function(){
        a_smpid.push($(this).val());
    });
    if (a_smpid.length == 0){
		document.getElementById('DeleteCheckedUser').classList.add('d-none')
    }else{
        document.getElementById('DeleteCheckedUser').classList.remove('d-none')
    }
}

function DeleteCheckedUser() {
    var a_smpid = [];
    $.each($("input[name='userid']:checked"), function(){
        a_smpid.push($(this).val());
    });
    console.log(a_smpid);
    if (a_smpid.length == 0){
		alert('select checkbox');
    }else{
        console.log(a_smpid);
        var result = confirm("Are You Sure. You Want to delete?");
        if (result) {
            $.ajax({
                url: '/basculeadmin/delete_user/',
                type: 'POST',
                dataType: 'json',
                data: {
                    id : a_smpid,
                    csrfmiddlewaretoken: csrftoken
                },
                success: function(data) {
                    if(data.status === 200){
                        const config = {
                            html: `Successfully Delete Customer.`,
                            type: 'success',
                            icon: "success",
                            confirmButtonText: 'Ok, got it!',    
                        };
                        sweetAlert.fire(config)
                    }
                    location.reload();
                }
            });
        }
    }
}

