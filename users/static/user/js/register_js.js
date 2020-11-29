
$(function(){
    $('.captcha').css({
    'cursor': 'pointer'
});

/*# ajax 刷新*/
    $('.captcha').click(function(){
        console.log('click');
        $.getJSON("/captcha/refresh/",function(result){
            $('.captcha').attr('src', result['image_url']);
            $('#id_captcha_0').val(result['key'])
        });
    });

    var error_name = false;
    var error_password = false;
    var error_check_password = false;
    var error_email = false;
    var error_check = false;
    var error_captcha = false;
// 注册页面
$('#name').blur(function () {
        if(check_name()){
            var username = $("#name").val();
            $.ajax({
                type:"GET",
                url: "/user/register/check_user",
                dataType: 'json',
                async:true,
                data:{
                    "username":username,
                    "csrfmiddlewaretoken":"{{ csrf_token }}",
                },
                success:function (data) {
                        if(data["code"]==100||data["code"]==102){
                            error_name = true;
                            $("#name").next().html(data["msg"]);
                            $("#name").next().show();
                        }else {
                            error_name=false;
                            $("#name").next().hide();
                        }
                },
                error:function (error) {
                    //请求失败
                }
            });
        }

    });
$('#email').blur(function () {
        if(check_email()){
            var email = $("#email").val();
            $.ajax({
                cache:false,
                type:"GET",
                url: '/user/register/check_email',
                dataType: 'json',
                async:true,
                data:{
                    "email":email,
                    "csrfmiddlewaretoken":"{{ csrf_token }}",
                },
                success:function (data) {
                        if(data["code"]==100||data["code"]==102){
                            error_email=true;
                             $("#email").next().html(data["msg"]);
                             $("#email").next().show();
                        }else {
                            error_email=false;
                             $("#email").next().hide();
                        }

                },
                error:function (error) {
                    //请求失败
                }
            });
        }

    });
$('#id_captcha_1').blur(function () {
        var captcha_1 = $("#id_captcha_1").val();
        var captcha_0 = $("#id_reg_captcha_0").val();
        $.ajax({
            cache:false,
            type:"GET",
            url: '/user/register/check_captcha',
            dataType: 'json',
            async:true,
            data:{
                "captcha_0":captcha_0,
                "captcha_1":captcha_1,
            },
            success:function (data) {
                    if(data["code"]==100||data["code"]==102){
                        error_captcha=true;
                         $("#id_reg_captcha_0").next().html(data["msg"]);
                         $("#id_reg_captcha_0").next().show();
                    }else {
                        error_captcha=false;
                         $("#id_reg_captcha_0").next().hide();
                    }

            },
            error:function (error) {
                //请求失败
            }
        });

    });
$('#pass').blur(function () {
        check_pass();
    });
$('#re_pass').blur(function () {
        check_re_pass();
    });

$('#register-form').submit(function () {
    check_email();
    check_name();
    check_pass();
    check_re_pass();
    if(error_email==false&&error_password==false&&error_name==false&&error_check_password==false){
        if($("#agree-term").prop("checked")){
            return true;
        }else {
            $("#check_tip").html("请同意服务条款");
            $("#check_tip").show();
            return false;
        }
    }else {
        return false;
    }
});

function check_name() {
    var len = $("#name").val().length;
    if(len<2||len>30){
        $("#name").next().html("请输入2-30个字符");
        $("#name").next().show();
        error_name=true;
        return false;
    }else {
        $("#name").next().hide();
        error_name=false;
        return true
    }
}
function check_email() {
    const re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
 if (re.test($("#email").val())) {
     $("#email").next().hide();
        error_email=false;
        return true;
  }else {
      $("#email").next().html("请输入正确的邮箱");
      $("#email").next().show();
      error_name=true;
      return false
 }
}
function check_pass() {
    var len = $("#pass").val().length;
    if(len<6||len>16){
        $("#pass").next().html("密码最少6位，最多16位");
        $("#pass").next().show();
        error_password=true;
    }else {
        $("#pass").next().hide();
        error_password=false;
    }
}
function check_re_pass() {
    var pass = $("#pass").val();
    var re_pass = $("#re_pass").val();
    if(pass!=re_pass){
        $("#re_pass").next().html("两次输入密码不同");
        $("#re_pass").next().show();
        error_password=true;
    }else {
        $("#re_pass").next().hide();
        error_password=false;
    }
}

});
