$(function () {
	login_setup();
});

function login_setup() {
    $("#login_summit").bind("click", login_summit);
}

function login_summit() {
    var name = $("#inputName").val();
    var password = $('#inputPassword').val();
    if(name == "" || password == "") {
        alert("登陆名或登陆密码为空!");
        return false;
    }
    
    var obj = {"name":name, "password":password};
    var jobj = JSON.stringify(obj);
    var url = "/manage/login";
    
    $.post(url, jobj, function(data) {
        if(data == "SUCCESS") {
            location.href = "/manage/passage"
        }else{
            $("#login_alert").html(data);
            $("#login_alert").show();
        }
    });
}
