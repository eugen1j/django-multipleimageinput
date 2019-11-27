$(function () {
    $(".js-image-input").each(function () {
        let $widget = $(this);
        let mediaPrefix = $widget.data('media-prefix');
        let $input = $widget.find('input[type=hidden]');
        let $container = $widget.find('> div');
        let $fileinput = $widget.find('input[type=file]');
        $container.sortable({
            update: function () {
                return $input.val(imageInputValue($container, mediaPrefix));
            }
        });

        $fileinput.change(function () {
            let $label = $fileinput.prev();
            $label.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Загрузка...');
            let formData = new FormData();
            if ($(this)[0]) {
                formData.append("csrfmiddlewaretoken", $('meta[name="csrf-token"]').attr("content"));
                for (const file of $(this)[0].files) {
                    formData.append("images", file);
                }
                $.ajax({
                    url: $(this).data('url'),
                    type: 'POST',
                    data: formData,
                    processData: false,
                    contentType: false,
                    success: function (data) {
                        for (const url of data) {
                            $container.append(imageHtml(mediaPrefix, url));
                        }
                        $input.val(imageInputValue($container, mediaPrefix));
                        $label.html("Добавить фото");
                    }
                });
            }
        });
    });
});

function imageHtml(mediaPrefix, data) {
    return '<div class="image-block">' +
        '<i class="fa fa-times"></i>' +
        '<img src="' + mediaPrefix + data + '" alt="">' +
        '</div>';
}

function imageInputValue($container, mediaPrefix) {
    return $container.find('img').map(function () {
        return $(this).attr('src').replace(mediaPrefix, '');
    }).get().join(',');
}

$(document).on('click', '.js-image-input .fa-times', function () {
    let $widget = $(this).parent().parent().parent();
    let mediaPrefix = $widget.data('media-prefix');
    let $input = $widget.find('> input');
    let $container = $widget.find('> div');
    $(this).parent().remove();
    $input.val(imageInputValue($container, mediaPrefix));
});
