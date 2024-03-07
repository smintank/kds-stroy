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
        $('.overlay').addClass('active');
        $('.photo_popup').show();
    }

    $(document).on('keydown', function(event) {
        if (event.keyCode === 27) {
            $('#overlay').removeClass('active');
            $('.photo_popup').hide();
        }
        if (event.keyCode === 37) navigatePhotos(-1);
        if (event.keyCode === 39) navigatePhotos(1);
    });

    $nextPhotoBtn.click(() => navigatePhotos(1));
    $prevPhotoBtn.click(() => navigatePhotos(-1));


    function navigatePhotos(step) {
        const newIndex = currentIndex + step;
        if (newIndex >= 0 && newIndex < photos.length) {
            currentIndex = newIndex;
            $popupImage.attr('src', photos[currentIndex]);
            toggleNavigationButtons();
        }
    }

    function toggleNavigationButtons() {
        $prevPhotoBtn.toggle(currentIndex > 0);
        $nextPhotoBtn.toggle(currentIndex < photos.length - 1);
    }

    $('.photo_miniature').click(function() {
        const clickedPhotoUrl = $(this).attr('src');
        const $siblings = $(this).parent().children();
        const i = $siblings.index($(this));

        photos = $siblings.map(function() {
            return $(this).attr('src');
        }).get();
        openPopup(i, clickedPhotoUrl);
    });
});