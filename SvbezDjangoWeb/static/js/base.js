$(document).ready(function($) {
    // PopUpHide();
    const header = $('.header')
    let prevScroll = $(window).scrollTop()
    let currentScroll
    let elems = document.getElementsByClassName('drop-down-data')
    $('.mobile-left-side-bar #id_brand').parent().show();
    $('.left-side-bar #id_brand').parent().show();
    for (let elem in elems){
        let this_element = $(elems[elem]).children('div')
        let element_id = this_element.attr('id')
        if($.cookie(element_id) != null && element_id != null){
            if($.cookie(element_id) === "show"){
                this_element.parent().show()
            }
        }
    }


    let categories = document.getElementsByClassName('category_block');
    for (let cat in categories){
        let cat_item = $(categories[cat])
        let cat_id = $(categories[cat]).attr('id');
        if(cat_id != null && $.cookie(cat_id) === "hint"){
            let hint_line = cat_item.siblings('hr')
            hint_line.show();
        }
    }

    $(window).on('scroll', function() {

        //ADD .TIGHT
        let expression = $(window).scrollTop() + $(window).height() > $('.wrapper').outerHeight() && $(window).width() > 990;
        if (expression) {
            $('body').addClass('tight');
        } else {
            $('body').removeClass('tight');
        }

        //HIDE HEADER
        currentScroll = $(window).scrollTop()
        let sub_header = $('.sub-header')
        const headerHidden = () => header.hasClass('header_hidden')
        let mlsb = document.getElementsByClassName('mobile-left-side-bar').length;
        
        if (mlsb){
            if (currentScroll > prevScroll && !headerHidden() && $('.mobile-left-side-bar').is(":hidden")) { // если прокручиваем страницу вниз и header не скрыт
                header.addClass('header_hidden')
                sub_header.addClass('sub-header_hidden')
            }
        }else{
            if (currentScroll > prevScroll && !headerHidden()) { // если прокручиваем страницу вниз и header не скрыт
                header.addClass('header_hidden')
                sub_header.addClass('sub-header_hidden')
            }
        }
        if (currentScroll < prevScroll && headerHidden() && !expression) { // если прокручиваем страницу вверх и header скрыт
            header.removeClass('header_hidden')
            sub_header.removeClass('sub-header_hidden')

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


function PopUpShow(preordered_value=null){
    if(preordered_value != null){
        let pattern = `Добрый день! Хотелось бы приобрести товар "${preordered_value}"`
        $(".pop-up textarea").val(pattern)
        $(".pop-up").css('display', 'flex');
    }
    else
        $(".pop-up").css('display', 'flex');
}

function PopUpHide(){
    $(".pop-up").hide();
}


$('.arrow').click(function(){
    $("html").animate({ scrollTop: $('html').prop("scrollHeight")}, 1200);
});

$('#id_sort_type').on('change', function() {
    document.forms["sort_form"].submit();
 });


$('.label').click(function(){
    let element = $(this).siblings('.drop-down-data')
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
    let element = $('.mobile-left-side-bar');
    let tint = $(".tint")
    if(element.is(":hidden")){
        tint.show();
        element.show();
        $(this).addClass('rotate_arrow')
    }else{
        tint.hide();
        element.removeAttr( 'style' );
        $(this).removeClass('rotate_arrow')

    }
});

function FiltersHide(){
    let element = $('.mobile-left-side-bar');
    let tint = $(".tint");
    tint.hide();
    element.removeAttr( 'style' );
    $('.filters').removeClass('rotate_arrow');
}

$('.selected').click(function(){
    let element = $(this).siblings('.sort_form')
    let arrow = $(this).children('span')
    if(element.is(":hidden")){
        element.show();
        arrow.addClass('rotate_arrow')
    }else{
        element.hide();
        arrow.removeClass('rotate_arrow')
    }
});

function clearMyCookie(){
    let cookies = $.cookie()
    for (let cookie in cookies){
        if($.cookie(cookie) === "show"){
            $.removeCookie(cookie);
        }
    }
}

$('.category_block').click(function(){
    clearMyCookie();
});

$('.mobile-left-side-bar #dismiss').click(clearMyCookie);
$('.left-side-bar #dismiss').click(clearMyCookie);


$('.extra img').click(function(){
    $('.product-image img').attr('src', $(this).attr('src'));
});

$('section.cards .card').click(function(e){
    if (!$(e.target).closest('.bottom-data').length) {
        let href = this.querySelector('.content .headline a');
        window.location.href = $(href).attr('href');
    } 
});

