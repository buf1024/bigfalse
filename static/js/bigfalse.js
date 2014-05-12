$(function () {
	tiny_setup();
});

function tiny_setup() {
    $("#search_go").bind("click", search_go);
}

function search_go() {
    var txt = $("#search_text").val();
    if(txt == "") {
        alert("搜索字符为空");
        return false;
    }
    return true;
}
