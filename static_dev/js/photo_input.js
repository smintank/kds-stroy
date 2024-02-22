$(document).ready(function() {
  const formData = new FormData();

  function get_image_count() {
    return $('#imagePreviews').children().length;
  }

  $('#fileInput').change(function() {
    const files = this.files;
    const previewsContainer = $('#imagePreviews');

    for (let i = 0; i < files.length; i++) {
      const reader = new FileReader();
      reader.onload = function(event) {
        const preview = $('<div class="preview-image"></div>');
        const image = $('<img alt="uploaded_image" src=\"' + event.target.result + '\">');
        preview.append(image);

        const removeButton = $('<div class="remove-button">&times</div>');
        preview.append(removeButton);

        previewsContainer.append(preview);
      };

      reader.readAsDataURL(files[i]);
      formData.append('photo', files[i]);
      console.log('formData length: ' + formData.getAll('photo').length);
      console.log(formData.getAll('photo'));
    }
    let imageCount = get_image_count();
    if (imageCount >= 4) {
      $('#addImage').hide();
    }
    if (imageCount <= 1) {
      $('#addImageText').hide();
    }
  });


  $(document).on('click', '.preview-image', function() {

    formData.delete($(this).find('img').attr('src').split('/').pop());
    $(this).remove();

    console.log(this);
    console.log('formData length: ' + formData.getAll('photo').length);
    console.log(formData.getAll('photo'));

    const imageCount = get_image_count();

    if (imageCount < 5) {
      $('#addImage').show();
    }
    if (imageCount === 0) {
      $('#addImageText').show();
    }
  });

  $('#orderForm').submit(function(event) {
    event.preventDefault();
    $('#formContent').hide();
    $('#loadingMessage').show();


    const originFormData = new FormData(this);
    for (let [key, value] of formData.entries()) {
      originFormData.append(key, value);
    }

    $.ajax({
      type: 'POST',
      url: '/',
      data: originFormData,
      processData: false,
      contentType: false,
      success: function(response, status, xhr) {
        if (xhr.status === 201) {
          $('#loadingMessage').hide();
          $('#resultMessage').show();
        }
      },
      error: function(xhr, status, error) {
        $('#loadingMessage').hide();
        $('#errorMessage').show();
      }
    });
  });
});
