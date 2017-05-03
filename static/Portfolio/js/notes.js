var initDivs = function(){
    var category = $('div.category');
    var categoryMarginDouble = category.innerHeight() - category.height();
    category.css('min-height', window.innerHeight - $('div.footer').innerHeight() - categoryMarginDouble);
};

$(function() {
    initDivs();
    $('div.back a').click(function() {
        var oldUrl = $(location).attr('href')
        $(location).attr('href', oldUrl.replace(/\?contentId=[0-9]+#?/i, ''));
//        return false;
    });
})