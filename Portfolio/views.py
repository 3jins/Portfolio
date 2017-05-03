import collections
import datetime
import json
import math
import hashlib

from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.db.models import F

from Portfolio.forms import CommentForm, AdminLoginForm
from Portfolio.models import Menu, Comment, Content, Context, AdminInfo
from Portfolio.oauth import refresh_credential


def intro(request):
    # Literally a dictionary for test
    for_test = {
        'test':[reverse('intro')]
    }

    # A dictionary for passing to intro.html as a context
    context = {
        #'menuList': menu_list,
        'forTest': for_test
    }
    return render(request, 'Portfolio/intro.html', context)


def works(request):
    content_id = request.GET.get('id')

    if content_id:
        # get content from DB
        contents_queryset = Context.objects.filter(content_id=content_id).order_by('seq')
        contents = []
        for content in contents_queryset:
            if content.type >= 3:
                context = content.context.split("??width=")
                if len(context) > 1:
                    contents += [{'type': content.type, 'context': context[0], 'width': context[1]}]
                else:
                    contents += [{'type': content.type, 'context': content.context}]
            else:
                contents += [{'type': content.type, 'context': content.context}]

        # Get infos from comment
        meta, account, comments = get_from_comment(request, content_id)

        # Update comments on DB.
        if update_comment(request, content_id) in ['1', '2', '3', '4']:
            return redirect('/works/?id='+content_id)

        # Make an unbound form.
        form = CommentForm(initial={
            'commentor_email': account['email'],
            'commentor_name': account['name'],
            'commentor_picture': account['picture'],
            'content_id': content_id,
        })

        # Get comments from DB
        # meta, comments = get_comments(content_id, meta)

        # Complete context.
        context = {'meta': meta, 'comments': comments, 'account': account, 'form': form, 'contents': contents, 'id': content_id}

        return render(request, 'Portfolio/works.html', context)
    else:
        # get thumbnail info from DB
        thumbnails_queryset = Content.objects.filter(menu__menu_title='Works').prefetch_related('menu').order_by('date')
        thumbnails_prg = []
        thumbnails_sec = []
        thumbnails_etc = []
        for thumbnail in thumbnails_queryset:
            if thumbnail.menu.submenu_title == 'Programming':
                thumbnails_prg += [{
                    'id': thumbnail.id,
                    'title': thumbnail.title,
                    'pic': thumbnail.thumbnail_pic,
                    'text': thumbnail.thumbnail_text,
                    'date': datetime.datetime.strftime(thumbnail.date, '%Y-%m-%d'),
                }]
            elif thumbnail.menu.submenu_title == 'Security':
                thumbnails_sec += [{
                    'id': thumbnail.id,
                    'title': thumbnail.title,
                    'pic': thumbnail.thumbnail_pic,
                    'text': thumbnail.thumbnail_text,
                    'date': thumbnail.date,
                }]
            elif thumbnail.menu.submenu_title == 'ETC':
                thumbnails_etc += [{
                    'id': thumbnail.id,
                    'title': thumbnail.title,
                    'pic': thumbnail.thumbnail_pic,
                    'text': thumbnail.thumbnail_text,
                    'date': thumbnail.date,
                }]
        thumbnails = collections.OrderedDict()
        thumbnails['programming'] = thumbnails_prg
        thumbnails['security'] = thumbnails_sec
        thumbnails['etc'] = thumbnails_etc
        return render(request, 'Portfolio/works_intro.html', {'thumbnails': thumbnails, })


def interests(request):
    return render(request, 'Portfolio/works_intro.html')


def notes(request):
    meta = {}
    context = {}
    menu_queryset = Menu.objects.filter(menu_title='Notes').order_by('menu_code')
    categories = []
    for menu in menu_queryset:
        if int(menu.menu_code)%100 is 0:
            continue
        categories += [{'code':menu.menu_code, 'title':menu.submenu_title}]
    content_id = request.GET.get('contentId')

    if request.method == 'GET':
        if request.GET.get('flag') is '1':
            print('T_T')
            return write_note(request, categories)

    # view content
    if content_id:
        # Get infos from comment
        meta, account, comments = get_from_comment(request, content_id)

        # Update comments on DB.
        if update_comment(request, content_id) in ['1', '2', '3', '4']:
            return redirect('/notes/?contentId=' + content_id)

        # Make an unbound form.
        form = CommentForm(initial={
            'commentor_email': account['email'],
            'commentor_name': account['name'],
            'commentor_picture': account['picture'],
            'content_id': content_id,
        })

        meta['isSelected'] = True
        contents_queryset = Context.objects.filter(content_id=content_id).order_by('seq')
        contents = []
        for content in contents_queryset:
            if content.type >= 3:
                context = content.context.split("??width=")
                if len(context) > 1:
                    contents += [{'type': content.type, 'context': context[0], 'width': context[1]}]
                else:
                    contents += [{'type': content.type, 'context': content.context}]
            else:
                contents += [{'type': content.type, 'context': content.context}]
        title = str(Content.objects.values_list('title').filter(id=content_id).first()[0])
        print(title)

        # Set context
        context = {
            'meta': meta,
            'categories': categories,
            'contents': contents,
            'title': title,
            'account': account,
            'comments': comments,
            'form': form,
        }

    # list contents
    else:
        meta = {'isSelected': False}
        this_category = request.GET.get('category')
        current_page = request.GET.get('currentPage')
        if current_page is None:
            current_page = 1
        else:
            current_page = int(current_page)
        page_size = 10

        # Calculate the sequence where has to start
        list_size = 8
        seq_start = (current_page-1)*list_size

        # Get contents from DB
        query = request.POST.get('query')
        if query:
            print(query)
            if this_category is not None:
                meta['thisCategory'] = int(this_category)
                num_of_contents = Content.objects.filter(menu__menu_title='Notes', menu=this_category, title__contains=query).count()
                thumbnails_queryset = Content.objects.filter(menu__menu_title='Notes', menu=this_category, title__contains=query).order_by('-date')[seq_start:seq_start+list_size]
            else:
                meta['thisCategory'] = 0
                num_of_contents = Content.objects.filter(menu__menu_title='Notes', title__contains=query).count()
                thumbnails_queryset = Content.objects.filter(menu__menu_title='Notes', title__contains=query).order_by('-date')[seq_start:seq_start+list_size]
        else:
            if this_category is not None:
                meta['thisCategory'] = int(this_category)
                num_of_contents = Content.objects.filter(menu__menu_title='Notes', menu=this_category).count()
                thumbnails_queryset = Content.objects.filter(menu__menu_title='Notes', menu=this_category).order_by('-date')[seq_start:seq_start+list_size]
            else:
                meta['thisCategory'] = 0
                num_of_contents = Content.objects.filter(menu__menu_title='Notes').count()
                thumbnails_queryset = Content.objects.filter(menu__menu_title='Notes').order_by('-date')[seq_start:seq_start+list_size]
        last_page = math.floor((num_of_contents - 1) / list_size) + 1
        thumbnails = []
        for thumbnail in thumbnails_queryset:
            thumbnails += [{
                'id': thumbnail.id,
                'title': thumbnail.title,
                'pic': thumbnail.thumbnail_pic,
                # 'text': query.thumbnail_text,
                'date': datetime.datetime.strftime(thumbnail.date, '%Y-%m-%d'),
            }]

        # Calculate infos about page
        current_pages = []
        page_start = math.floor(current_page / page_size) * page_size + 1
        current_last_page = min([last_page, page_start + page_size - 1])
        for value in range(page_start, current_last_page + 1):
            current_pages += [value]
        meta['currentPage'] = current_page
        meta['currentPages'] = current_pages
        if current_pages != []:
            if min(current_pages) > 1:
                meta['isTherePrevPages'] = True
                meta['firstPrevPage'] = page_start - page_size
            else:
                meta['isTherePrevPages'] = False
            if max(current_pages) < last_page:
                meta['isThereNextPages'] = True
                meta['firstNextPage'] = page_start + page_size
            else:
                meta['isThereNextPages'] = False

        # Set context
        context = {
            'meta': meta,
            'categories': categories,
            'thumbnails': thumbnails,
            'lastPage': last_page
        }

    return render(request, 'Portfolio/notes.html', context)


def guestbook(request):
    # Get id of guestbook from DB.
    content_id = str(Content.objects.values_list('id').filter(title='guestbook').first()[0])

    # Get infos from comment
    meta, account, comments = get_from_comment(request, content_id)

    # Update comments on DB.
    if update_comment(request, content_id) in ['1', '2', '3', '4']:
        return redirect('/guestbook/')

    # Make an unbound form.
    form = CommentForm(initial={
        'commentor_email': account['email'],
        'commentor_name': account['name'],
        'commentor_picture': account['picture'],
        'content_id': content_id,
    })

    # Get comments from DB
    # meta, comments = get_comments(content_id, meta)

    # Complete context.
    context = {'meta': meta, 'comments': comments, 'account':account, 'form':form,}

    # Render.
    return render(request, 'Portfolio/guestbook.html', context)


def login(request):

    form = AdminLoginForm()

    if request.method == 'POST':
        admin_id = request.POST.get('admin_id')
        admin_pw = request.POST.get('admin_pw')
        try:
            admin_info = AdminInfo.objects.filter(admin_id=admin_id)[0]
            if admin_info.fail_time.replace(tzinfo=None) < datetime.datetime.now().replace(tzinfo=None) - datetime.timedelta(minutes=1):
                AdminInfo.objects.filter(admin_id=admin_id).update(fails=0)
            if admin_info.fails >= 5:
                return render(request, 'Portfolio/admin_login.html', {'form':form, 'error':'No bruteforce! ㅗㅗㅗ'})
            else:
                # id ok pw ok
                if admin_info.admin_pw == hashlib.md5(admin_pw.encode('utf-8')).hexdigest():
                    AdminInfo.objects.filter(admin_id=admin_id).update(fails=0)
                    # 세션작업
                    request.session['admin_id'] = admin_id
                    return intro(request)
                # id ok pw no
                else:
                    AdminInfo.objects.filter(admin_id = admin_id).update(fails=F('fails')+1)
                    AdminInfo.objects.filter(admin_id=admin_id).update(fail_time=datetime.datetime.now())
                    return render(request, 'Portfolio/admin_login.html', {'form': form, 'error':'땡ㅋㅋㅋㅋ'})
        except IndexError:
            # id no
            return render(request, 'Portfolio/admin_login.html', {'form': form, 'error': '땡ㅋㅋㅋㅋ'})

    return render(request, 'Portfolio/admin_login.html', {'form':form, 'error':'none'})


def get_from_comment(request, content_id):
    comments_queryset = Comment.objects.filter(content_id=content_id).order_by('-date')
    num_of_comments = len(comments_queryset)
    meta = {'num': num_of_comments}

    if 'email' in request.session:
        # Get oauth account information from session and credential json file.
        try:
            credential_json = json.load(open('static/Portfolio/json/' + request.session['email'] + '.json'))
            refresh_credential(request, credential_json)
            account = {
                'email': request.session['email'],
                'name': credential_json['id_token']['name'],
                'picture': credential_json['id_token']['picture']
            }
            meta['login'] = 1
        except OSError:  # For FileNotFoundError. It occurs in case that json file is disappeared but session still remains.
            account = {'email': '', 'name': '', 'picture': ''}
            meta['login'] = 0

        # Get comments
        comments = []
        for comment in comments_queryset:
            picture = comment.commentor.picture
            print(picture[picture.find('/')+1:])
            comments += [{
                'id': comment.id,
                'commentorEmail': comment.commentor.email,
                'name': comment.commentor.name,
                'picture': picture[picture.find('/')+1:],
                'comment': comment.comment,
                'date': comment.date,
                'editDate': comment.edit_date,
            }]
    else:
        account = {'email': '', 'name': '', 'picture': ''}
        meta['login'] = 0
        comments = {}

    return meta, account, comments


def logout(request):
    request.session.pop('admin_id')
    return intro(request)


def update_comment(request, content_id):
    if request.method == 'POST':
        commentor_email = request.POST.get('commentor_email')   # it is used when flag is not 1
        flag = request.POST.get('flag')
        if flag is '1':
            form = CommentForm(request.POST)  # form is bound to POST data
            if form.is_valid() and 'email' in request.session:
                comment = form.save(commit=False)
                comment.content_id = content_id
                comment.date = datetime.datetime.now()
                comment.edit_date = None
                comment.commentor_id = request.session['email'] # 씨발
                comment.save()
            else:
                # session 끊겼다고 예외처리
                print("whatthefuck")
            return flag
        elif 'email' in request.session and commentor_email == request.session['email']:
            print("fufufufuck")
            # elif flag is '2':
            #     aim = request.POST.get('aim')
            if flag is '3':
                aim = request.POST.get('aim')
                edit_text = request.POST.get('editText')
                Comment.objects.filter(id=aim).update(comment=edit_text, edit_date=datetime.datetime.now())
                return flag
            elif flag is '4':
                aim = request.POST.get('aim')
                Comment.objects.filter(id=aim).delete()
                return flag
        else:
            return 0


def write_note(request, categories):
    #폼을 짜서 던진다...가 안돼 컨텍스트 DB 구조 존나 특이해서.
    #필요한거: 카테고리선택박스, 제목, 컨텍스트 추가버튼 4종
    # 카테고리/제목 외에 기본적으로 맨 위에 컨텍스트 추가버튼 4종이 있음.
    # 하나 누르면 컨텍스트 에디터가 생김.
    # 컨텍스트 에디터는 편집창이랑 삭제 버튼이랑 컨텍스트추가버튼4종 을 가지고 있음.
    # 컨텍스트 교환 기능도 만들고 싶지만 이 기능은 관리자 혼자 쓰는거인데다 그거 서버로직은 쉬운데 js가 복잡해서 안할거임.
    # content_queryset = Content.objects.filter(menu_code__gte=400).filter(menu_code__lt=500)

    context = {
        # 'meta': meta,
        'categories': categories,
    }
    print('TT')
    return render(request, 'Portfolio/notes_new.html', context)



# def handler404(request):
#     return render(request, 'test/test.html', {'who':'you'})