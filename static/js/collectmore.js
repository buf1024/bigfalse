$(function () {
	collectmore_setup();
});

function collectmore_setup() {
    $("button[id^='collect_view']").bind("click", collect_view);
}

function collect_view(event) {
    var link = $("#" + event.target.id).attr("data");
    location.href = link
}
function rebind_event() {
    collectmore_setup();
}