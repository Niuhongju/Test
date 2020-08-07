$(function () {
    //判断用户名是否可用
    var $username = $("#username_input");
    $username.change(function () {
        var username = $username.val().trim();
        if (username.length) {
            //    将用户名送给服务器进行预校验
            $.getJSON('/axf/checkuser/', {'username': username}, function (data) {
                console.log(data);
                var $username_info=$("#username_info")
                if(data['status']===200){
                    $username_info.html('用户名可用').css('color','green');
                }else if (data['status']===901){
                    $username_info.html('用户名已存在').css('color','red');
                }
            });
        }
    })

    //判断邮箱是否可用
    var $email=$("#email_input");
    $email.change(function () {
        var email=$email.val().trim()
        if (email.length){
        //    将邮箱送给服务器进行预校验
            $.getJSON('/axf/checkemail/',{'email':email},function (data) {
                var $email_info=$("#email_info")
                if(data['status']===200){
                    $email_info.html('邮箱可用').css('color','green')
                }else if(data['status']===901){
                    $email_info.html('邮箱已存在').css('color','red')
                }
            })
        }
    })

    //判断密码是否一致
    var $password_confirm=$("#password_confirm_input");
    $password_confirm.change(function () {
        var $password=$("#password_input");
        var password=$password.val().trim();
        var password_confrim=$password_confirm.val().trim();
        console.log(password_confrim)
        console.log(password)
        if(password==password_confrim){
            $("#password_confirm_info").html('密码一致').css('color','green')
        }else if(password!=password_confrim){
            $("#password_confirm_info").html('密码不一致').css('color','red')
        }
    })
})

//登录验证
function check() {
    //用户名不能为空且不重复
    var username=$("#username_input").val().trim()
    if(!username){
        return false
    }
    var username_color=$("#username_info").css('color')
    console.log(username_color)
    if(username_color=='rgb(255, 0, 0)'){
        return false
    }
    //邮箱不能为空且不重复
    var email=$("#email_input").val().trim()
    if(!email){
        return false
    }
    var email_color=$("#email_info").css('color')
    if(username_color=='rgb(255, 0, 0)'){
        return false
    }

    //密码不能为空
    var password=$("#password_input").val().trim()
    if(!password){
        return  false
    }
    //确认密码不能为空
    var password_confirm=$("#password_confirm_input")
    if(!password_confirm){
        return  false
    }
    //密码不能重复
    var password_confirm_color=$("#password_confirm_info").css('color')
    if(password_confirm_color=='rgb(255, 0, 0)'){
        return false
    }

    //头像不能为空
    var icon=$("#icon_input").val().trim()
    if(!icon){
        return false
    }

    var $password_input=$("#password_input")
    var password=$password_input.val().trim()
    console.log(password)
    $password_input.val(md5(password))
    // console.log($("#password_input").val())
    return  true

}