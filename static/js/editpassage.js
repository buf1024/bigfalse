$(function () {
	passage_setup();
});

function passage_setup() {
    tinymce.init({selector:"#tinymce_editor"});
    $("#passage_save").bind("click", passage_save);
    $("#passage_save_draft").bind("click", passage_save_draft);
    $("#passage_catalog").bind("change", passage_catalog);
    $("#dialog_catalog_save").bind("click", dialog_catalog_save);
    $('#dialog_catalog').on('hidden.bs.modal', dialog_hidden);
}

function dialog_hidden() {    
    var sel$ =  $("#passage_catalog");
    var val = sel$.find(':selected').val();
    if(val == -1) {
        var sel = "#passage_catalog option[value='-1000'";
        $(sel).attr("selected", true);
    }
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
        var obj = {"title":title, "desc":desc, "sel":sel};
            
        jobj = JSON.stringify(obj);
        url = "/manage/catalog/new";
        
        $.post(url, jobj, function(data) {
            if(data == "FAIL") {
                alert("操作失败!");
                sel = "#passage_catalog option[value='-1000'";
                $(sel).attr("selected", true);
            }else{
                d = data.split("|");
                opt = "<option value='" + d[1] + "'>" + title +"</option>";
                $("#passage_catalog").prepend(opt);
                sel = "#passage_catalog option[value='" + d[1] + "'";
                $(sel).attr("selected", true);
                $("#dialog_catalog").modal("hide");
            }
        });
    }
}

function passage_catalog() {
    var sel$ =  $("#passage_catalog");
    var val = sel$.find(':selected').val();
    if(val == -1) {
        $("#catalog_opt_type").attr("disabled", "disabled");
        $("#dialog_catalog").modal();
    }
}
function passage_save() {
    edit_passage(false);
}

function passage_save_draft() {
    edit_passage(true);
}
function edit_passage(isdraft) {
    var title = $("#passage_title").val();
    if(title == "") {
        alert("文章标题为空!");
        return 0;
    }
    var content = tinymce.get("tinymce_editor").getContent();
    if(content == "") {
        alert("文章内容为空!");
        return 0;
    }
    var sumary = $("#passage_summary").val();
    if(sumary == "") {
        alert("文章摘要为空!");
        return 0;
    }
    var cat = $("#passage_catalog").val();
    if(cat <= 0) {
        alert("文章分类无效!");
        return 0;
    }
    var visiable = $("#passage_visiable").is(":checked");    
    var front = $("#passage_front").is(":checked");
    var comment = $("#passage_commentable").is(":checked");    
    var tags = $("#passage_tags").val();
    
    var obj = new Object();
    obj.title = title;
    obj.content = content;
    obj.sumary = sumary;
    obj.catalog = cat;
    obj.visiable = visiable;
    obj.front = front;
    obj.commentable = comment;
    obj.tags = tags;
    
    obj.isdraft = isdraft;
    
    var role = $("#passage_save").attr("role");
    
    obj.role = role;
    
    if(role == "update") {
        obj.id = $("#passage_save").attr("data");
    }
    
    var jobj = JSON.stringify(obj);
       
    $.post("/manage/passage/edit", jobj, function (data) {
        if(data == "FAIL") {
            alert("保存文件失败!");
        }else{
            location.href = "/manage/passage";
        }
    });
}
