$(function(){
    var error_password1=false;
    var error_password2=false;
function check_pass1() {
    var len = $("#new_password1").val().length;
    if(len<6||len>16){
        $("#new_password1").next().html("密码最少6位，最多16位");
        $("#new_password1").next().show();
        error_password1=true;
    }else {
        $("#new_password1").next().hide();
        error_password1=false;
    }
};
function check_pass2() {
    var pass = $("#new_password1").val();
    var re_pass = $("#new_password2").val();
    if(pass!=re_pass){
        $("#new_password2").next().html("两次输入密码不同");
        $("#new_password2").next().show();
        error_password2=true;
    }else {
        $("#new_password2").next().hide();
        error_password2=false;
    }
}
$('#new_password1').blur(function () {
        check_pass1();
    });
$('#new_password2').blur(function () {
        check_pass2();
    });
$('#btn_submit').click(function () {
        check_pass1();
        check_pass2();
        if(!error_password1&&!error_password2){
            $('#reset_password_form').submit();
            return true;
        }
        return false;
    });
});
