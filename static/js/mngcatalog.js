$(function () {
	mngcatalog_setup();
});

function mngcatalog_setup() {
    $("button[id^='mngcatalog_modify']").bind("click", mngcatalog_modify);
    $("button[id^='mngcatalog_delete']").bind("click", mngcatalog_delete);
    $("#mngcatalog_new_catalog").bind("click", mngcatalog_new_catalog);
    $("#dialog_catalog_save").bind("click", dialog_catalog_save);
    $("#dialog_confirm_no").bind("click", dialog_confirm_no);
    $("#dialog_confirm_yes").bind("click", dialog_confirm_yes);
}

function dialog_confirm_yes() {
    var id = $("#dialog_confirm_yes").attr("data");  
    var obj = {"id":id};
    var jobj = JSON.stringify(obj);
    $.post("/manage/catalog/delete", jobj, function(data) {
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

function mngcatalog_modify(event) {
    var id = $("#" + event.target.id).attr("data");
    $("#dialog_catalog_title").html("修改分类");
    $.get("/manage/catalog/" + id + ".json", function (data) {
        $("#dialog_catalog_save").attr("role", "update");        
        $("#dialog_catalog").modal();
        data = JSON.parse(data);
        var id = data.id;
        var name = data.name;
        var desc = data.desc;
        var type = data.type;
        $("#catalog_title").val(name);
        $("#catalog_desc").val(desc);
        var sel = "#catalog_opt_type option[value='" + type +"'";
        $(sel).attr("selected", true);
        $("#dialog_catalog_save").attr("data", id);  
    });
}

function mngcatalog_delete(event) {
    var id = $("#" + event.target.id).attr("data");
    var count = $("#" + event.target.id).attr("count");
    if(count > 0) {
        alert("归属文章或归属游戏大于0, 不允许删除该分类!");
    }else{
        $("#dialog_confirm").modal();
        $("#dialog_confirm_yes").attr("data", id);  
    }
}

function mngcatalog_new_catalog() {
    $("#dialog_catalog_title").html("增加分类");
    $("#catalog_title").val("");
    $("#catalog_desc").val("");
    var sel = "#catalog_opt_type option[value='1'";
    $(sel).attr("selected", true);
    $("#dialog_catalog_save").attr("role", "new");
    $("#dialog_catalog").modal();
}

function dialog_catalog_save() {
    var title = $("#catalog_title").val();
    var desc = $("#catalog_desc").val();
    var sel = $("#catalog_opt_type").val();
    
    var role = $("#dialog_catalog_save").attr("role");
    var id = $("#dialog_catalog_save").attr("data");
    
    if(title == "" || desc == "") {
        alert("名称或描述为空");
    }else{
        var jobj = "";
        var url = "";
        if(role == "new") {
            var obj = {"title":title, "desc":desc, "sel":sel};
            
            jobj = JSON.stringify(obj);
            url = "/manage/catalog/new";
        }
        if(role == "update") {
            var obj = {"id":id, "title":title, "desc":desc, "sel":sel};
            jobj = JSON.stringify(obj);
            url = "/manage/catalog/update";
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
