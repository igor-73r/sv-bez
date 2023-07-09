$(document).ready(function($) {
    PopUpHide();
    const header = $('.header')
    let prevScroll = $(window).scrollTop()
    let currentScroll
    let elems = document.getElementsByClassName('drop-down-data')
    $(document.getElementById('id_brand')).parent().show()
    for (let elem in elems){
        let this_element = $(elems[elem]).children('div')
        let element_id = this_element.attr('id')
        if($.cookie(element_id) != null && element_id != null){
            if($.cookie(element_id) === "show"){
                this_element.parent().show()
            }
        }

    }
    $(window).on('scroll', function() {

        //ADD .TIGHT
        let expression = $(window).scrollTop() + $(window).height() > $('.wrapper').outerHeight() && $(window).width() > 990
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


function PopUpShow(){
    $(".pop-up").show();
}
//Функция скрытия PopUp
function PopUpHide(){
    $(".pop-up").hide();
}


$('.arrow').click(function(){
    $("html").animate({ scrollTop: $('html').prop("scrollHeight")}, 1200);
});


$('.label').click(function(){
    let element = $(this).parent().children('.drop-down-data')
    if(element.is(":hidden")){
        element.show();
        $.cookie(element.children('div').attr('id'), 'show')
    }else{
        element.hide();
        if ($.cookie(element.children('div').attr('id'))){
            $.removeCookie(element.children('div').attr('id'));
        }
    }
});

$('.filters').click(function(){
    let element = $(this).siblings('.left-side-bar')
    if(element.is(":hidden")){
        element.show();
    }else{
        element.removeAttr( 'style' );
    }
});

function clearMyCookie(){
    let cookies = $.cookie()
    for (let cookie in cookies){
        if($.cookie(cookie) === "show"){
            $.removeCookie(cookie)
        }
    }
}

$('#dismiss').click(clearMyCookie);

$('.category_block').click(clearMyCookie);


