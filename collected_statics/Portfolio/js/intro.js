var resizeMainParagraphs = function() {
    var paragraph = $('div.paragraph')
    paragraph.css('height', window.innerHeight);
};
var smoothSlide = function(obj){
    $('html, body').animate({
        scrollTop: $('[name="' + $.attr(this, 'href').substr(1) + '"]').offset().top
    }, 500);
    return false;
};
var eventClassifier = function() {
    $('a').click(function() {
        smoothSlide(this);
    });
    $('div.paragraph').each(function(index, item) {
        if(index == 0) {

        } else if index == $('div.paragraph:last').index() {

        } else {
        }
    });
};

$(window).resize(function() {
    resizeMainParagraphs();
});

$(function () {
alert('test');
    resizeMainParagraphs();
    eventClassifier();
});