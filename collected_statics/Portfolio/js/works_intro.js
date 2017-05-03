var castShadow = function(){
    $('div.thumbnail div.work').each(function(index, item){
        $(item).hover(function() {
            $(item).css('background-color', '#ffc');
        }, function() {
            $(item).css('background-color', 'transparent');
        });
    });
}
$(function() {
    castShadow();
});