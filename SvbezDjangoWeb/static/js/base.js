$(document).ready(function($) {
    const header = $('.header')
    let prevScroll = $(window).scrollTop()
    let currentScroll
    $(window).on('scroll', function() {

        //ADD .TIGHT
        let expression = $(window).scrollTop() + $(window).height() > $('.wrapper').outerHeight()
        if (expression) {
            $('body').addClass('tight');
            $('.arrow').hide();
        } else {
            $('body').removeClass('tight');
            $('.arrow').show();
        }

        //HIDE HEADER
        currentScroll = $(window).scrollTop()
        const headerHidden = () => header.hasClass('header_hidden')
        if (currentScroll > prevScroll && !headerHidden()) { // если прокручиваем страницу вниз и header не скрыт
            header.addClass('header_hidden')
        }
        if (currentScroll < prevScroll && headerHidden() && !expression) { // если прокручиваем страницу вверх и header скрыт
            header.removeClass('header_hidden')
        }
        prevScroll = currentScroll
    });

    //BACK TO PRESENTATION MODE
    $("html").on("click", "body.tight .wrapper", function() {
        $('html, body').animate({
            scrollTop: $('.wrapper').outerHeight() - $(window).height()
        }, 500);
    });

});

$('.arrow').click(function(){
    $("html").animate({ scrollTop: $('html').prop("scrollHeight")}, 1200);
});
