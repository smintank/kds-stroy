$(document).ready(function() {
  const formData = new FormData();
  let imageNumbers = 0;

  function get_image_count() {
    return $('#imagePreviews').children().length;
  }

  $('#fileInput').change(function() {
    const files = this.files;
    const previewsContainer = $('#imagePreviews');

    let imageCount = get_image_count();
    console.log('imageCount: ' + imageCount);
    for (let i = 0; i < files.length; i++) {
      if ((imageCount + i + 1) === 5) {
        $('#addImage').hide();
      } else if ((imageCount + i + 1) > 5) {
        break;
      }
      const currentImageId = 'photo-' + imageNumbers;
      const reader = new FileReader();
      reader.onload = function(event) {
        const preview = $('<div class="preview-image"></div>');
        const image = $('<img alt="uploaded_image" src=\"' + event.target.result + '\">');
        preview.append(image);

        const removeButton = $('<div class="remove-button">&times</div>');
        removeButton.attr('image-id', currentImageId);
        preview.append(removeButton);

        previewsContainer.append(preview);
      };

      reader.readAsDataURL(files[i]);

      files[i].id = currentImageId;
      formData.append('photo-' + imageNumbers, files[i]);
      console.log('formData length: ' + formData.getAll('photo').length);
      formData.forEach((value, key) => console.log(key, value));
      imageNumbers++;
    }
    if (imageCount < 1) {
      $('#addImageText').hide();
    }
  });


  $(document).on('click', '.preview-image', function() {

    console.log($(this).find('.remove-button').attr('image-id'));

    for (let [key, value] of formData.entries()) {
      console.log(formData.entries())
      console.log('key: ' + key + ', value: ' + value.id);
      if (value.id === $(this).find('.remove-button').attr('image-id')) {
        formData.delete(key);
        break;
      }
    }
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
    originFormData.delete('photo');
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
