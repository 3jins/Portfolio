var revealOrHideMenu = function(reveal){
    var menutable = $('div.menutable');
    if(reveal) {
        menutable.css('visibility', 'visible').css('animation-name', 'menuSlideDown').css('animation-duration', '0.5s');
        setTimeout(function() {$('div.menutable td').css('visibility', 'visible')}, 100)
        $('div.menubutton img.menubutton:eq(0)').css('display', 'none');
        $('div.menubutton img.menubutton:eq(1)').css('display', 'inline');
    }
    else {
        menutable.css('animation-name', 'menuSlideUp').css('animation-duration', '0.5s').delay(500).css('visibility', 'hidden');
        $('div.menutable td').css('visibility', 'hidden');
        $('div.menubutton img.menubutton:eq(0)').css('display', 'inline');
        $('div.menubutton img.menubutton:eq(1)').css('display', 'none');
    }
};
var revealSubmenu = function(index){
    if($('div.menutable a:eq('+index+')').text() == 'Notes') {
        hideSubmenu();
        return;
    }
    $('div.submenutable:not('+index+')').css('visibility', 'hidden');
    $('div.submenutable:eq('+index+')').css('visibility', 'visible');
}
var hideSubmenu = function(){
    $('div.submenutable').css('visibility', 'hidden');
};
var openSesame = function(idx, event){
    var key = new Array(115, 101, 115, 97, 109, 101);

    if(event.which == key[idx]) {
        if(++idx >= key.length) {
            var oldUrl = $(location).attr('href')
            var mainUrl = oldUrl.slice(0, oldUrl.indexOf('/', 7)+1);
            $(location).attr('href', mainUrl+'sesame');
        }
        return idx;
    }
    else {
        return 0;
    }
};
var closeSesame = function(idx, event){
    var key = new Array(101, 109, 97, 115, 101, 115);   // emases

    if(event.which == key[idx]) {
        if(++idx >= key.length) {
            alert('Demacia? Emases야!')
            var oldUrl = $(location).attr('href')
            var mainUrl = oldUrl.slice(0, oldUrl.indexOf('/', 7)+1);
            $(location).attr('href', mainUrl+'emases');
        }
        return idx;
    }
    else {
        return 0;
    }
}

$(function () {
    if(navigator.userAgent.match(/Android|Mobile|iP(hone|od|ad)|BlackBerry|IEMobile|Kindle|NetFront|Silk-Accelerated|(hpw|web)OS|Fennec|Minimo|Opera M(obi|ini)|Blazer|Dolfin|Dolphin|Skyfire|Zune/)){
        alert(
            'Design for mobile is under construction now. Please connect with PC. T_T\n'+
            '아직 스마트폰 해상도에서는 디자인이 개판입니다. PC로 접속해주세요ㅠㅠ\n\n'+
            'Do not forget to enter port number.\n'+
            '포트 번호까지 쳐야 정상적으로 접속됩니다.'
        );
    }

    sesameIndex = 0;
    emasesIndex = 0;

    $('div.menubutton img.menubutton:eq(0)').click(function() {
        revealOrHideMenu(true);
    });
    $('div.menubutton img.menubutton:eq(1)').click(function() {
        revealOrHideMenu(false);
    });
    $('div.menutable a').hover(function() {
        //revealOrHideSubmenu(true);
    });

    $('div.menutable a').each(function(index, item){
        $(item).hover(function() {
            revealSubmenu(index);
        }, function() {
        });
    });
    $('div.menu').hover(function() {
    }, function() {
           hideSubmenu();
    });

    $(document).keypress(function(e) {
        sesameIndex = openSesame(sesameIndex, e);
        emasesIndex = closeSesame(emasesIndex, e);
    });
});