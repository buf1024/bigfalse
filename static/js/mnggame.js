$(function () {
	mnggame_setup();
});

function mnggame_setup() {
    $("button[id^='mnggame_modify']").bind("click", mnggame_modify);
    $("button[id^='mnggame_delete']").bind("click", mnggame_delete);
    $("#mnggame_new_game").bind("click", mnggame_new_game);
    $("#dialog_game_save").bind("click", dialog_game_save);
    $("#dialog_confirm_no").bind("click", dialog_confirm_no);
    $("#dialog_confirm_yes").bind("click", dialog_confirm_yes);
}

function dialog_confirm_yes() {
    var id = $("#dialog_confirm_yes").attr("data");  
    var obj = {"id":id};
    var jobj = JSON.stringify(obj);
    $.post("/manage/game/delete", jobj, function(data) {
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

function mnggame_modify(event) {
    var id = $("#" + event.target.id).attr("data");
    $("#dialog_game_title").html("修改游戏");
    $.get("/manage/game/" + id + ".json", function (data) {
        $("#dialog_game_save").attr("role", "update");  
        data = JSON.parse(data);
        var id = data.id;
        var name = data.name;
        var desc = data.desc;
        var image = data.image;
        var width = data.width;
        var height = data.height;
        var visiable = data.visiable;
        var cat = data.catalog;
        $("#game_title").val(name);
        $("#game_desc").val(desc);
        $("#game_image").val(image);
        $("#game_width").val(width);
        $("#game_height").val(height);
        $("#game_visiable").prop("checked", visiable);
        var sel = "#game_catalog option[value='" + cat.id +"'";
        $(sel).attr("selected", true);
        $("#dialog_game_save").attr("data", id);  
              
        $("#dialog_game").modal();
    });
}

function mnggame_delete(event) {
    var id = $("#" + event.target.id).attr("data");
    $("#dialog_confirm").modal();
    $("#dialog_confirm_yes").attr("data", id);  
}
function mnggame_new_game() {
    $("#dialog_game_title").html("增加游戏");
    $("#game_title").val("");
    $("#game_desc").val("");
    $("#game_image").val("");
    $("#game_width").val("");
    $("#game_height").val("");
    $("#game_visiable").attr("selected", false);
    var sel = "#game_opt_type option[value='1'";
    $(sel).attr("selected", true);
    $("#dialog_game_save").attr("role", "new");
    $("#dialog_game").modal();
}

function dialog_game_save() {
    var title = $("#game_title").val();
    var desc = $("#game_desc").val();
    var image = $("#game_image").val();
    var width = $("#game_width").val();
    var height = $("#game_height").val();
    var visiable = $("#game_visiable").is(":checked");
    var cat = $("#game_catalog").val();
    
    var role = $("#dialog_game_save").attr("role");
    var id = $("#dialog_game_save").attr("data");
    
    if(title == "" || desc == "" || image == "" || width == "" || height == "") {
        alert("名称或描述或图片路径或高度或宽带为空");
    }else{
        var jobj = "";
        var url = "";
        if(role == "new") {
            var obj = {"title":title, "desc":desc, "image":image,
                    "width":width, "height":height, "visiable":visiable,
                    "catalog":{"id":cat}};
            
            jobj = JSON.stringify(obj);
            url = "/manage/game/new";
        }
        if(role == "update") {
            var obj = {"id":id, "title":title, "desc":desc, "image":image,
                    "width":width, "height":height,
                    "visiable":visiable, "catalog":{"id":cat}};
            jobj = JSON.stringify(obj);
            url = "/manage/game/update";
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
