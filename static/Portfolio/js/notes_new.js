var addSubtitle = function(index){
};
var addLetters = function(index){
    $(
        '<div class="paragraph">'+
            '<textarea name="">'+index+'</textarea>'+
            '<input class="hannom" type="button" value="소제목"/>'+
            '<input class="dushigi" type="button" value="글"/>'+
            '<input class="seoksam" type="button" value="사진"/>'+
            '<input class="neoguri" type="button" value="영상"/>'+
            '<input class="ojingeo" type="button" value="삭제"/>'+
        '</div>'
    ).appendTo('div.paragraph:eq('+index+')');
};
var addPicture = function(index){
};
var addClip = function(index){
};
var removeParagraph = function(index){
}
$(document).click(function() {
    $('input.hannom').each(function(index, item){
        $(item).click(function(){
            addSubTitle(index);
        });
    });
    $('input.dushigi').each(function(index, item){
        $(item).click(function(){
            addLetters(index);
            return false;
        });
    });
    $('input.seoksam').each(function(index, item){
        $(item).click(function(){
            addPictures(index);
        });
    });
    $('input.neoguri').each(function(index, item){
        $(item).click(function(){
            addClip(index);
        });
    });
    $('input.ojingeo').each(function(index, item){
        $(item).click(function(){
            removeParagraph(index);
        });
    });
    $(document).click(function(){
        return false;
    });
});