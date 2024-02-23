$(document).ready(function() {
  const formData = new FormData();
  let imageNumbers = 0;

  function containsFile(formData, photoName) {
    return Array.from(formData.values()).some(photo => photo.name === photoName);
}

  function addPreviewItem(currentPhotoId, photo) {
    const reader = new FileReader();
    reader.onload = function (event) {
      const imageSrc = event.target.result;
      const preview = $(`
            <div class="preview-image">
              <img alt="uploaded_image" src="${imageSrc}">
              <div class="remove-button" image-id="${currentPhotoId}">&times;</div>
            </div>
          `);
      $('#imagePreviews').append(preview);
    };
    reader.readAsDataURL(photo);
  }

  function togglePhotoTools(formData) {
    const formDataLength = Array.from(formData.entries()).length;
    $('#addImage').toggle(formDataLength < 5);
    $('#addImageText').toggle(formDataLength <= 0);
  }

  $('#fileInput').change(function() {
    const photos = this.files;


    Array.from(photos).forEach(photo => {
      if (!containsFile(formData, photo.name) &&
        (Array.from(formData.entries()).length) < 5) {

        const currentPhotoId = 'photo-' + imageNumbers;
        addPreviewItem(currentPhotoId, photo);
        formData.append(currentPhotoId, photo);
        imageNumbers++;
      }
    });
    togglePhotoTools(formData);
  });



  $(document).on('click', '.preview-image', function() {
    const imageId = $(this).find('.remove-button').attr('image-id');
    formData.delete(imageId);
    $(this).remove();
    togglePhotoTools(formData);
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
