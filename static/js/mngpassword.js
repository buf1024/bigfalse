$(function () {
	mngsetting_setup();
});

function mngsetting_setup() {
    $("#setting_opt_submit").bind("click", setting_opt_submit);
    $("#dialog_confirm_no").bind("click", dialog_confirm_no);
    $("#dialog_confirm_yes").bind("click", dialog_confirm_yes);
}

function dialog_confirm_yes() {
    var obj = new Object();
    obj.source = $("#setting_src_password").val();
    obj.newpass = $("#setting_new_password").val();
    var jobj = JSON.stringify(obj);
    
    $.post("/manage/password/update", jobj, function(data) {
        if(data == "SUCCESS") {
            $("#setting_success").html("操作成功,请牢记新密码");
            $("#setting_fail").hide();
            $("#setting_success").show();
        }else{
            $("#setting_fail").html(data);
            $("#setting_success").hide();
            $("#setting_fail").show();
        }
        $("#dialog_confirm").modal("hide");
    });
}

function dialog_confirm_no() {
    $("#dialog_confirm").modal("hide");
}

function setting_opt_submit() {
    var obj = new Object();
    obj.source = $("#setting_src_password").val();
    obj.newpass = $("#setting_new_password").val();
    obj.checkpass = $("#setting_check_password").val();
    if(obj.newpass != obj.checkpass) {
        alert("两次输入密码不一致");
        return;
    }
    if(obj.newpass.length < 6) {
        alert("新密码长度必须大于等于6");
        return;
    }
    if(obj.source.length <= 0) {
        alert("原密码不能为空");
        return;
    }
    if(obj.source == obj.newpass) {
        alert("新密码与旧密码一致");
        return;
    }
    $("#dialog_confirm").modal();
}
