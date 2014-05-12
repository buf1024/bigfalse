$(function () {
	mnglabel_setup();
});

function mnglabel_setup() {
    $("button[id^='mnglabel_modify']").bind("click", mnglabel_modify);
    $("button[id^='mnglabel_delete']").bind("click", mnglabel_delete);
    $("#mnglabel_new_label").bind("click", mnglabel_new_label);
    $("#dialog_label_save").bind("click", dialog_label_save);
    $("#dialog_confirm_no").bind("click", dialog_confirm_no);
    $("#dialog_confirm_yes").bind("click", dialog_confirm_yes);
}

function dialog_confirm_yes() {
    var id = $("#dialog_confirm_yes").attr("data");  
    var obj = {"id":id};
    var jobj = JSON.stringify(obj);
    $.post("/manage/label/delete", jobj, function(data) {
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

function mnglabel_modify(event) {
    var id = $("#" + event.target.id).attr("data");
    $("#dialog_label_title").html("修改标签");
    $.get("/manage/label/" + id + ".json", function (data) {
        $("#dialog_label_save").attr("role", "update");        
        $("#dialog_label").modal();
        data = JSON.parse(data);
        var id = data.id;
        var name = data.name;
        var desc = data.desc;
        $("#label_title").val(name);
        $("#label_desc").val(desc);
        $("#dialog_label_save").attr("data", id);  
    });
}

function mnglabel_delete(event) {
    var id = $("#" + event.target.id).attr("data");
    $("#dialog_confirm").modal();
    $("#dialog_confirm_yes").attr("data", id);  

}

function mnglabel_new_label() {
    $("#dialog_label_title").html("增加标签");
    $("#label_title").val("");
    $("#label_desc").val("");
    $("#dialog_label_save").attr("role", "new");
    $("#dialog_label").modal();
}

function dialog_label_save() {
    var title = $("#label_title").val();
    var desc = $("#label_desc").val();
    
    var role = $("#dialog_label_save").attr("role");
    var id = $("#dialog_label_save").attr("data");
    
    if(title == "" || desc == "") {
        alert("名称或描述为空");
    }else{
        var jobj = "";
        var url = "";
        if(role == "new") {
            var obj = {"title":title, "desc":desc};
            
            jobj = JSON.stringify(obj);
            url = "/manage/label/new";
        }
        if(role == "update") {
            var obj = {"id":id, "title":title, "desc":desc};
            jobj = JSON.stringify(obj);
            url = "/manage/label/update";
        }
        
        $.post(url, jobj, function(data) {
            if(data == "FAIL") {
                alert("操作失败!");
            }else{
                location.reload();
            }
        });
    }
}
