
/*
1. Set the height of representative divs as that of the screen.
2. Set the position of representative images into the center.
*/
var initImgs = function () {
    // 1
	$('div.representative div.fix').css('height', window.innerHeight);
	// 2
	$('div.representative div.fix div.wrapper').css(
	    'padding-top',
	    (window.innerHeight/2-125)+'px'
	);
//	$('div.representative div div.wrapper').css(
//	    'line-height',
//	    (window.innerHeight+($('div.representative div div.wrapper img').height())/2)+'px'
//	);
//	$('div.representative div div.wrapper div').css('line-height', 1);
};

/*
In this template, almost all divs are defined as 'absolute' or 'fixed'.
So footer doesn't stick at bottom.
This function makes footer stay in the bottom.
*/
//var initFooter = function() {
//    $('div.footer').css('width', parseFloat($('div.footer').width())*3/4);
//    $('div.footer').offset({
//        top:
//            $('div.content').height(),
//        left:
//            window.innerWidth/4     // This is mystery : The position of span changes as if the width of footer is same with the width of representative div.
//    });
//};

var fixedOn = function(index) {
    $('div.representative div.fix:not('+index+')').attr('class', 'fix nonfixed');
    $('div.representative div.fix:eq('+index+')').attr('class', 'fix fixed');
    $('div.representative div.fix:eq('+index+')').css('top', 0);
    $('div.representative div.fix:eq('+index+')').css('z-index', 10);
};

var fixedOff = function(index) {
    // current bottom div
    $('div.representative div.fix:eq('+index+')').attr('class', 'fix nonfixed');
    $('div.representative div.fix:not('+index+')').css('z-index', 0);   // 'here'
    $('div.representative div.fix:eq('+index+')').css('z-index', 1);
    $('div.representative div.fix:eq('+index+')').offset({
        top:
            parseFloat($('div.content div.thumbnail:eq('+index+')').offset().top) +
            parseFloat($('div.content div.thumbnail:eq('+index+')').height()) -
            parseFloat($('div.representative div.fix:eq('+index+')').height()) +
            parseFloat($('div.content div.thumbnail:eq('+index+')').innerHeight() - $('div.content div.thumbnail:eq('+index+')').height())		// padding
	});
	// next top div
	if(index < $('div.representative div.fix').length - 1 ) {
        index++;
        $('div.representative div.fix:eq('+index+')').attr('class', 'fix nonfixed');
        $('div.representative div.fix:eq('+index+')').css('z-index', 1);    // I don't make others' 0 cause it's already changed in comment 'here'.
        $('div.representative div.fix:eq('+index+')').offset({
            top:
                $('div.content div.thumbnail:eq('+index+')').offset().top //+
                //($('div.content div:eq('+index+')').innerHeight() - $('div.content div:eq('+index+')').height())		// padding
        });
    }
};

var fixedOnOff = function() {
    var fixOffFlag = false;
    // Check if fixOff should be called
    $('div.representative div.fix').each(function(index, item) {
        if(index < $('div.representative div.fix').length - 1) {
            if(
                $(window).scrollTop() >= parseFloat($('div.content div.thumbnail:eq('+(index+1)+')').offset().top) - parseFloat($(item).height()) &&
                $(window).scrollTop() < parseFloat($('div.content div.thumbnail:eq('+(index+1)+')').offset().top)
            ) {
                fixedOff(index);
                fixOffFlag = true;
            }
        }
    });
    // Check if fixOn should be called
    if(!fixOffFlag) {
        $('div.representative div.fix').each(function(index, item) {
            if(index < $('div.representative div.fix').length - 1) {
                if(
                    $(window).scrollTop() < parseFloat($('div.content div.thumbnail:eq('+(index+1)+')').offset().top) - parseFloat($(item).height()) &&
                    $(window).scrollTop() >= parseFloat($('div.content div.thumbnail:eq('+index+')').offset().top)
                ){
                    fixedOn(index);
                }
            } else {
                if($(window).scrollTop() >= parseFloat($('div.content div.thumbnail:eq('+index+')').offset().top)) {
                    fixedOn(index);
                }
            }
        });
    }
};

$(function() {
	initImgs();
});
$(window).resize(function() {
	initImgs();
});
$(window).on("keydown", function(e) {
	if(e.which == 36) {
	    fixedOn(0);
	}
});

$(window).scroll(function(event){
    fixedOnOff();
});