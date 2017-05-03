import collections
from Portfolio.models import Menu

# Get menu/submenu data from database and combine it into an ordered dictionary
def menu(request):
    result_menu = Menu.objects.filter(submenu_title__isnull=True).order_by('menu_code')
    menu_list = collections.OrderedDict()
    temp_list = []
    for idx in range(0, len(result_menu)):
        result_submenu = Menu.objects.filter(menu_title=result_menu[idx].menu_title).filter(
            submenu_title__isnull=False).order_by('menu_code')
        for sub_idx in range(0, len(result_submenu)):
            temp_list += [result_submenu[sub_idx].submenu_title]
        menu_list[result_menu[idx].menu_title] = temp_list
        temp_list = []
    return {'menuList': menu_list, 'nullList':[],}