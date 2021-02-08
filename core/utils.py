def convert_dict_breadcrums(data):

    breadcrums = []

    for item in data:
        status = ''
        if item[1] == "#":
            status = 'active'
        breadcrums.append({
            'name': item[0],
            'url': item[1],
            'status': status,
        })

    breadcrums[-1]['status'] = 'active'

    return breadcrums
