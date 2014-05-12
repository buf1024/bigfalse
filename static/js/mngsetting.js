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
    obj.id = $("#setting_opt_submit").attr("data");
    obj.title = $("#setting_opt_title").val();
    obj.brand = $("#setting_opt_brand").val();
    obj.copy = $("#setting_opt_copy_info").val();
    obj.display_count = $("#setting_opt_display_count").val();
    obj.notify = $("#setting_opt_notify").is(":checked");
    obj.overview = $("#setting_opt_overview").is(":checked");
    obj.game_count = $("#setting_opt_game_menu_count").val();
    var module = new Array();
    $("input[id^='setting_opt_module']").each(function (i, e){
        var id = $("#" + e.id).attr("data");
        var m = new Object();
        m.id = id;
        m.visiable = e.checked;
        module.push(m);
    });
    obj.module = module;
    var jobj = JSON.stringify(obj);
    
    $.post("/manage/setting/update", jobj, function(data) {
        if(data == "FAIL") {
            alert("操作失败！");
        }else{
            location.reload();
        }
    });
}

function dialog_confirm_no() {
    $("#dialog_confirm").modal("hide");
}

function setting_opt_submit() {
    $("#dialog_confirm").modal();
}
