$(function () {

// 提交按钮
$("#submit_btn").click(function () {
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
});
});
