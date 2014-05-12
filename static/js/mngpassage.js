$(function () {
	mngpassage_setup();
});

function mngpassage_setup() {
    $("button[id^='mngpassage_view']").bind("click", mngpassage_view);
    $("button[id^='mngpassage_modify']").bind("click", mngpassage_modify);
    $("button[id^='mngpassage_delete']").bind("click", mngpassage_delete);
    
    $("#mngpassage_new_passage").bind("click", mngpassage_new_passage);
    $("#mngpassage_backup_passage").bind("click", mngpassage_backup_passage);
    $("#dialog_confirm_no").bind("click", dialog_confirm_no);
    $("#dialog_confirm_yes").bind("click", dialog_confirm_yes);
}

function dialog_confirm_yes() {
    var id = $("#dialog_confirm_yes").attr("data");
    var obj = {"id":id};
    var jobj = JSON.stringify(obj);
    
    $.post("/manage/passage/delete", jobj, function(data) {
        if(data == "FAIL") {
            alert("操作失败!");
        }else{
            location.reload();
        }
    });
}

function dialog_confirm_no() {
    $("#dialog_confirm").modal("hide");
}

function mngpassage_new_passage() {
    location.href = "/manage/passage/new";
}

function mngpassage_backup_passage() {
    alert("not implement yet");
}

function mngpassage_view(event) {
    var id = $("#" + event.target.id).attr("data");
    var url = "/passage/" + id
    window.open(url)
}

function mngpassage_modify(event) {
    var id = $("#" + event.target.id).attr("data");
    var url = "/manage/passage/modify/" + id;
    location.href = url;
}

function mngpassage_delete() {
    var id = $("#" + event.target.id).attr("data");
    $("#dialog_confirm").modal();
    $("#dialog_confirm_yes").attr("data", id);
}

function rebind_event() {
    mngpassage_setup();
}

