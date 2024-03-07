$(document).ready(function() {
    const $popup = $('#photoPopup');
    const $prevPhotoBtn = $('#prevPhoto');
    const $nextPhotoBtn = $('#nextPhoto');
    const $popupImage = $('#popupImage');
    let photos = [];
    let currentIndex = 0;

    // Function to open the popup
    function openPopup(index, photo) {

        currentIndex = index;
        $popupImage.attr('src', photo);
        $('#overlay').addClass('active');
        $('.photo_popup').show();
    }

    function closePopup() {
        $('#overlay').removeClass('active');
        $('.photo_popup').hide();
    }

    $('.close').click(closePopup);
    $('.overlay').click(closePopup);

    // Close the popup when pressing the "Esc" key
    $(document).on('keydown', function(event) {
        if (event.keyCode === 27) closePopup();
        if (event.keyCode === 37) navigatePhotos('prev');
        if (event.keyCode === 39) navigatePhotos('next');
    });

    $nextPhotoBtn.on('click', function() {
        navigatePhotos('next');
    });

    $prevPhotoBtn.on('click', function() {
        navigatePhotos('prev');
    });


    function navigatePhotos(direction) {
        if (direction === 'prev') {
            if (currentIndex > 0) {
                currentIndex--;
                $popupImage.attr('src', photos[currentIndex]);
            }
        } else if (direction === 'next') {
            if (currentIndex < photos.length - 1) {
                currentIndex++;
                $popupImage.attr('src', photos[currentIndex]);
            }
        }
    }

    $('.photo_miniature').each(function() {
        $(this).on('click', function() {
            const clicked_photo_url = $(this).attr('src');
            const $siblings = $(this).parent().children();

            let i;
            photos.length = 0;
            $siblings.each(function(index) {
                photos.push($(this).attr('src'));
                if (clicked_photo_url === $(this).attr('src')) i = index;
            });

            openPopup(i, $(this).attr('src'));
        });
    });
});