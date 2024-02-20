$(document).ready(function() {
  $('#fileInput').change(function() {
    console.log('Start script');
    var files = this.files;
    var previewsContainer = $('#imagePreviews');
    var imageCount = previewsContainer.children().length;
    console.log(imageCount);
    for (var i = 0; i < files.length; i++) {
      var reader = new FileReader();
      reader.onload = function(event) {
        var preview = $('<div class="preview-image"></div>');
        var image = $('<img alt="uploaded_image">');
        image.attr('src', event.target.result);
        preview.append(image);

        var removeButton = $('<div class="remove-button">&times</div>');
        preview.append(removeButton);

        previewsContainer.append(preview);
      };
      reader.readAsDataURL(files[i]);
    }
    console.log(imageCount);
    if (imageCount >= 4) {
      $('#addImage').hide();
    }
    if (imageCount <= 1) {
      $('#addImageText').hide();
    }
  });

  $(document).on('click', '.preview-image', function() {
    $(this).remove();
    var imageCount = $('#imagePreviews').children().length;
    console.log(imageCount);
    if (imageCount < 5) {
      $('#addImage').show();
    }
    if (imageCount === 0) {
      $('#addImageText').show();
    }
  });
});