var current = 0;
var imagenes = new Array();

$(document).ready(function () {
    var numImages = 8;
    if (numImages <= 4) {
        $('.right-arrow').css('display', 'none');
        $('.left-arrow').css('display', 'none');
    }

    $('.left-arrow').on('click', function () {
        if (current > 0) {
            current = current - 1;
        } else {
            current = numImages - 4;
        }

        $(".carrusel").animate({ "left": -($('#product_' + current).position().left) }, 900);

        return false;
    });

    $('.left-arrow').on('hover', function () {
        $(this).css('opacity', '0.5');
    }, function () {
        $(this).css('opacity', '1');
    });

    $('.right-arrow').on('hover', function () {
        $(this).css('opacity', '0.5');
    }, function () {
        $(this).css('opacity', '1');
    });

    $('.right-arrow').on('click', function () {
        if (numImages > current + 4) {
            current = current + 1;
        } else {
            current = 0;
        }

        $(".carrusel").animate({ "left": -($('#product_' + current).position().left) }, 900);

        return false;
    });
});


