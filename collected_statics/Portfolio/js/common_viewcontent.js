$(function() {
    $('div.back a').click(function() {
        var oldUrl = $(location).attr('href')
        $(location).attr('href', oldUrl.replace(/\?id=[0-9]+#?/i, ''));
//        return false;
    });
});
