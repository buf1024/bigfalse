$(function () {
	passageview_setup();
});

function passageview_setup() {
    $("button[id^='passage_view']").bind("click", passage_view);
}

function passage_view(event) {
    var id = $("#" + event.target.id).attr("data");
    location.href = "/passage/" + id
}
