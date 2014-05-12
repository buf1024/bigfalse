$(function () {
	passage_setup();
});

function passage_setup() {
    $("button[id^='comment_reply']").bind("click", comment_reply);
    $("button[id^='submit_comment']").bind("click", submit_comment);
}

function submit_comment() {
    var btn$ = $("#" + event.target.id);    
    var bid = btn$.attr("id");
    var sp = bid.split("_");
    var suf = sp[sp.length - 1];
    var rid = btn$.attr("data");
    var role = btn$.attr("role");
    var is_admin = btn$.attr("admin-flag");
    
    var name = $("#input_name_" + suf).val();
    var email = $("#input_email_" + suf).val();
    var comment = $("#input_comment_" + suf).val();
    
    if(is_admin == "False") {
        if(name == "" || email == "") {
            alert("昵称或电子邮箱为空!");
            return;
        }
    }
    if(comment.length <= 15) {
        alert("评论不能少于15个字符!");
        return;
    }
    var site = $("#input_site_" + suf).val(); 
    var obj = {
        "role":role,
        "id":rid,
        "name":name,
        "email":email,
        "site":site,
        "comment":comment
    };
    var jobj = JSON.stringify(obj);
    var url = "/comment/passage";
    $.post(url, jobj, function(data) {
        if(data == "SUCCESS") {            
            location.reload();
        }else{
            alert(data);
        }
    });
    return;
}

function comment_reply(event) {
    var btn$ = $("#" + event.target.id);    
    var id = btn$.attr("data");
    var status = btn$.attr("status");
    if(status == "hide"){
        $("#leave_comment_" + id).slideDown();
        btn$.attr("status", "show");
    }else{
        $("#leave_comment_" + id).slideUp();
        btn$.attr("status", "hide");
    }
}