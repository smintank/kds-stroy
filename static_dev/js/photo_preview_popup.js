$(document).ready(function() {
    const $prevPhotoBtn = $('#prevPhoto');
    const $nextPhotoBtn = $('#nextPhoto');
    const $popupImage = $('#popupImage');
    let photos = [];
    let currentIndex = 0;

    function openPopup(index, photo) {
        currentIndex = index;
        toggleNavigationButtons();
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

    $(document).on('keydown', function(event) {
        if (event.keyCode === 27) closePopup();
        if (event.keyCode === 37) navigatePhotos(-1);
        if (event.keyCode === 39) navigatePhotos(1);
    });

    $nextPhotoBtn.on('click', function() {
        navigatePhotos(1);
    });

    $prevPhotoBtn.on('click', function() {
        navigatePhotos(-1);
    });


    function navigatePhotos(step) {
        const newIndex = currentIndex + step;
        if (newIndex >= 0 && newIndex < photos.length) {
            currentIndex = newIndex;
            $popupImage.attr('src', photos[currentIndex]);
            toggleNavigationButtons();
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

    function toggleNavigationButtons() {
        $prevPhotoBtn.toggle(currentIndex > 0);
        $nextPhotoBtn.toggle(currentIndex < photos.length - 1);
    }
});