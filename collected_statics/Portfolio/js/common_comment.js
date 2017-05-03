//var modifyForReply = function(additionalButtons, index){
//    additionalButtons.remove();
//    $('<tr>'+
//        '<td>↳</td>'+
//        '<td><textarea name="replyText" cols="40" rows="10"></textarea></td>'+
//        '<td><input type="button" value="upload" onclick="submitForReply('+index+')"/>'+
//      '</tr>').appendTo('div.comment_list div:nth-child('+(index+1)+')>table>tbody');
//}
//var submitForReply = function(index){
//    $('input#flag').val(2);
//    $('input#aim').val($('input.commentId:eq('+index+')').val());
//    $('form').submit();
//}
var modifyForEdit = function(additionalButtons, index){
    additionalButtons.remove();
    var editArea = $('div.comment_list div:nth-child('+(index+1)+') table td:nth-child(2) p');
    $('div.comment_list div:nth-child('+(index+1)+') table table td:nth-child(1) span').text('editting');
    var editAreaText = editArea.text();
    editArea.remove();
    $('<textarea name="editText" cols="40" rows="10">'+editAreaText+'</textarea>').appendTo('div.comment_list div:nth-child('+(index+1)+')>table>tbody>tr>td:nth-child(2)');
    $('<input type="button" value="update" onclick="submitForEdit('+index+')"/>').appendTo('div.comment_list div:nth-child('+(index+1)+')>table>tbody>tr>td:nth-child(2)');
}
var submitForEdit = function(index){
    $('input#flag').val(3);
    $('input#aim').val($('input.commentId:eq('+index+')').val());
    $('input#aimEmail').val($('input.commentorEmail:eq('+index+')').val());
    $('form').submit();
}
var submitForDelete = function(index){
    $('input#flag').val(4);
    $('input#aim').val($('input.commentId:eq('+index+')').val());
    $('input#aimEmail').val($('input.commentorEmail:eq('+index+')').val());
    $('form').submit();
}

$(function(){
    var additionalButtons = $('div.comment_list div table td:nth-child(2) img');
//    $('.img_reply').each(function(index, item) {
//        $(item).click(function() {
//            modifyForReply(additionalButtons, index);
//        });
//    });
    $('.img_edit').each(function(index, item) {
        $(item).click(function() {
            modifyForEdit(additionalButtons, index);
        });
    });
    $('.img_delete').each(function(index, item){
        $(item).click(function() {
            if(confirm("Are you sure you want to delete?") == true) {
                submitForDelete(index);
            }
        });
    });
});