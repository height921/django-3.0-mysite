// 提交按钮
$("#submit_btn").click(function () {
    $.ajax({
        cache: false,
        url: "{% url 'problem:problem_detail' problem.slug %}",
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
})
