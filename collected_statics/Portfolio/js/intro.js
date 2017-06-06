var resizeMainParagraphs = function() {
    var paragraph = $('div.paragraph')
    paragraph.css('height', window.innerHeight);
};
var smoothSlideByObj = function(obj){
    $('html, body').animate({
        scrollTop: $('[name="' + $.attr(obj, 'href').substr(1) + '"]').offset().top
    }, 500);
    return false;
};
var smoothSlideByIdx = function(idx){
    var obj = $('div.paragraph:eq('+idx+')').children("a");
    $('html, body').animate({
        scrollTop: obj.offset().top
    }, 500);
    return false;
};
var eventClassifier = function() {
    $('a').click(function() {
        smoothSlideByObj(this);
    });
//    $(window).scrollUp(function() {
//        alert();
//        $('div.paragraph').each(function(index, item) {
//            if(index > 0 && $(window).scrollTop() < $('div.paragraph:eq('+(index+1)+')').offset().top) {
//                smoothSlideByIdx(index);
//                return false;
//            }
//        });
//    });
//    $(window).scrollDown(function() {
//        $('div.paragraph').each(function(index, item) {
//            if(index < $('div.paragraph:last').index() && $(window).scrollTop() >= $('div.paragraph:eq('+index+')')) {
//                smoothSlideByIdx(index+1);
//                return false;
//            }
//        });
//    });
};

$(window).resize(function() {
    resizeMainParagraphs();
});

$(function () {
    resizeMainParagraphs();
    eventClassifier();
});