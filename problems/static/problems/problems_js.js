$(function () {

// 提交按钮
$("#submit_btn").click(function () {
    var code = $("#codes").text();
    alert(code);
    alert(code.length);
    if(code.length<50){
        $("#submit_error").html("代码太短了");
        $("#submit_error").show();
    }
    else {
    $("#submit_error").hide();
    var url = '/problems/'+ $("#problem_slug").val();
    $.ajax({
        cache: false,
        url: url,
        type: "POST",
        dataType: 'json',
        data:$('#submit_form').serialize(),
        async: true,
        success: function (data) {
            if(data.status=='success'){
            alert(data.result);
            }else {
                alert("提交失败");
            }
        }
    });
    }

});
// 下拉框显示选中内容
$(".dropdown-menu a").click(function(){
  var selText = $(this).text();
  // $(this).parents('.btn-group').find('.dropdown-toggle').html(selText+' <span class="caret"></span>');
  $(this).parents('.btn-group').find('.dropdown-toggle').html(selText);
});
// 下拉框选中进行异步提交
    $(".dropdown-menu").click(function () {
    var url = '/problems/'
    var data = {
        'difficulty':$.trim($("#difficulty").text()),
        'tag':$.trim($("#tag").text()),
        'status':$.trim($("#status").text()),
    };
    $.ajax({
        cache: false,
        url: url,
        type: "GET",
        dataType: 'json',
        data:data,
        async: true,
        success: function (data) {
            if(data['status']=='success'){
                $("#problems").html(data['problem_list'])
            }
        }
    });
});
});
