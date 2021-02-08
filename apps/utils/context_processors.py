from django.conf import settings
from django.apps import apps
from django.urls import reverse, resolve
from django.urls.exceptions import Resolver404


def settings_context(_request):
    return {"settings": settings}


def get_apps_data(request):

    items = [
        {
            'index_name': 'Inicio',
            'icon': 'home',
            'url': reverse('index'),
            'menu': [],
            'status': 'active' if reverse('index') == request.path else ''
        }
    ]

    for app in apps.get_app_configs():
        if hasattr(app, 'index_name'):
            if hasattr(app, 'disable'):
                pass
            else:
                if request.user.has_perms(app.permisos) or app.permisos == {}:
                    menu = app.menu[:]
                    status_app = ''

                    for item in menu:
                        if len(item['submenu']) > 0:
                            status_item = ''
                            for submenu in item['submenu']:
                                if request.user.has_perm(submenu['permiso']) or submenu['permiso'] == {}:
                                    if request.path == submenu['url']:
                                        submenu['status'] = 'active'
                                        status_item = 'active'
                                        status_app = 'active'
                                    else:
                                        submenu['status'] = ''

                                    submenu['class'] = ''
                                else:
                                    submenu['class'] = 'd-none'

                                if len(submenu['other_urls']) > 0:
                                    try:
                                        url_match = resolve(request.path)
                                    except Resolver404:
                                        pass
                                    else:
                                        name_url = '{0}:{1}'.format(url_match.app_name, url_match.url_name)
                                        if name_url in submenu['other_urls']:
                                            submenu['status'] = 'active'
                                            status_item = 'active'
                                            status_app = 'active'

                            item['status'] = status_item

                        else:

                            if request.user.has_perm(item['permiso']) or item['permiso'] == '':

                                if request.path == item['url']:
                                    item['status'] = 'active'
                                    status_app = 'active'
                                else:
                                    item['status'] = ''

                                item['class'] = ''
                            else:
                                item['class'] = 'd-none'

                        if len(item['other_urls']) > 0:
                            try:
                                url_match = resolve(request.path)
                            except Resolver404:
                                pass
                            else:
                                name_url = '{0}:{1}'.format(url_match.app_name, url_match.url_name)
                                if name_url in item['other_urls']:
                                    item['status'] = 'active'
                                    status_app = 'active'

                    items.append({
                        'index_name': app.index_name,
                        'icon': app.icon,
                        'url': app.url,
                        'menu': menu,
                        'status': 'active' if app.url == request.path else status_app
                    })

    return items


def sidebar(request):
    return {'apps_permissions': get_apps_data(request)}
