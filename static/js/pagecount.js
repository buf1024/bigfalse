$(function () {
	pagecount_setup();
});

function pagecount_setup() {
    $(window).bind("scroll", load_more);
}

function load_more() {
    if ($(document).scrollTop() + $(window).height() > $(document).height() - 20) {
        var d$ = $("#page_count");
        var role = d$.attr("data-role");
        var page = d$.attr("data-page");
        var page_total = d$.attr("page-total");
        
        if(page_total <= page) {
            return false;
        }
        
        page = parseInt(page)
        page += 1
        
        var url = "/" + role + "/page/" + page
        $.post(url, "", function(data) {
            if(data != "FAIL") {     
                d = data.split("|");
                if(d[0] == page) {                
                    $("#page_count").attr("data-page", page);
                    var len = d[0].length;
                    data = data.substring(len + 1);
                    $("#content").append(data);
                }
            }
        });
    }
}

