$(document).ready(function() {
    // Handle file upload form submission
    $('#upload-form').submit(function(event) {
        event.preventDefault();

        var formData = new FormData(this);

        $.ajax({
            url: '/upload',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                // Show controls and start real-time threshold and sharpness adjustment
                $('#controls').show();
                realTimeProcess(response.file_path);
            }
        });
    });

    // Real-time threshold and sharpness slider adjustment
    function realTimeProcess(file_path) {
        $('#threshold, #sharpness').on('input', function() {
            var thresholdValue = $('#threshold').val();
            var sharpnessValue = $('#sharpness').val();

            $.ajax({
                url: '/process',
                type: 'POST',
                data: {
                    threshold: thresholdValue,
                    sharpness: sharpnessValue,
                    file_path: file_path
                },
                success: function(response) {
                    // Update the src of the img tag to point to the updated stencil image in the static folder
                    $('#stencil-image').attr('src', '/static/' + response.stencil_image + '?' + new Date().getTime());
                }
            });
        });
    }
});
