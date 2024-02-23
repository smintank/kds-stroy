$(document).ready(function() {
  const formData = new FormData();
  let imageNumbers = 0;

  function get_photo_amount() {
    return $('#imagePreviews').children().length;
  }

  function containsFile(formData, photoName) {
    for (const photo of formData.entries()) {
      console.log('Photo in formData: ' + photo[1].name);
      if (photo[1].name === photoName) {
        return true;
      }
    }
    return false;
    }

  $('#fileInput').change(function() {
    const photos = this.files;
    const previewsContainer = $('#imagePreviews');
    var photoPreviewAmount;

    for (let i = 0; i < photos.length; i++) {
      console.log('Photo in input: ' + photos[i].name);

      if (!containsFile(formData, photos[i].name)) {

        photoPreviewAmount = get_photo_amount();
        console.log('photoPreviewAmount: ' + photoPreviewAmount);

        if (photoPreviewAmount >= 5) {
          $('#addImage').hide();
          break;
        }

        const currentPhotoId = 'photo-' + imageNumbers;

        const reader = new FileReader();
        reader.onload = function(event) {
          const imageSrc = event.target.result;
          const preview = $(
            `<div class="preview-image">
              <img alt="uploaded_image" src="${imageSrc}">
              <div class="remove-button" image-id="${currentPhotoId}">&times;</div>
            </div>`);
          previewsContainer.append(preview);
        };

        reader.readAsDataURL(photos[i]);
        formData.append(currentPhotoId, photos[i]);

        // formData.forEach((value, key) => console.log(key, value));

        imageNumbers++;
      } else {
        console.log('File already exists: ' + photos[i].name);
      }
    }
    photoPreviewAmount = get_photo_amount();
    console.log('photoPreviewAmount: ' + photoPreviewAmount);
    if (photoPreviewAmount + 1 > 0) {
      $('#addImageText').hide();
    }
  });


  $(document).on('click', '.preview-image', function() {

    const imageId = $(this).find('.remove-button').attr('image-id');
    formData.delete(imageId);

    // formData.forEach((value, key) => console.log(key, value));

    $(this).remove();

    const imageCount = get_photo_amount();

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
