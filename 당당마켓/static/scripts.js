$(document).ready(function () {
    $(".list-group-item-action").click(function () {
        let product_title = $(this).attr('id');
        $.get("/detail?title=" + product_title)
            .then(function (result) {
                $("#detailModalLabel").text(result.title);
                $("#detailModalContent").html(result.content);
                $("#detailModal").modal('show');
            });
    });
});