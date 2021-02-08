def edit_button(permiso=False, url='#', data_placement='top', title=''):

    if permiso:

        html = """
        <div class="text-center">
            <a href="{0}" class="" data-toggle="tooltip" data-placement="{1}" title="{2}">
                <i class="fas fa-edit fa-lg text-success"></i>
            </a>
        </div>
        """.format(url, data_placement, title)

    else:

        html = """
        <div class="text-center">
            <i class="fas fa-edit fa-lg"></i>
        </div>
        """

    return html


def edit_button_no_div(permiso=False, url='#', data_placement='top', title=''):

    if permiso:

        html = """
        <a href="{0}" class="" data-toggle="tooltip" data-placement="{1}" title="{2}">
            <i class="fas fa-edit fa-lg text-success"></i>
        </a>
        """.format(url, data_placement, title)

    else:

        html = """
        <i class="fas fa-edit fa-lg"></i>
        """

    return html


def delete_button(permiso=False, url='#', data_placement='top', title=''):

    if permiso:

        html = """
        <div class="text-center">
            <a href="{0}" class="" data-toggle="tooltip" data-placement="{1}" title="{2}">
                <i class="fas fa-trash-alt fa-lg text-danger"></i>
            </a>
        </div>
        """.format(url, data_placement, title)

    else:

        html = """
        <div class="text-center">
            <i class="fas fa-trash-alt fa-lg"></i>
        </div>
        """

    return html


def delete_button_no_div(permiso=False, url='#', data_placement='top', title=''):

    if permiso:

        html = """
        <a href="{0}" class="" data-toggle="tooltip" data-placement="{1}" title="{2}">
            <i class="fas fa-trash-alt fa-lg text-danger"></i>
        </a>
        """.format(url, data_placement, title)

    else:

        html = """
        <i class="fas fa-trash-alt fa-lg"></i>
        """

    return html
