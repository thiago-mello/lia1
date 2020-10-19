from helpers.check_integer import check_integer


def parse_project(project_name):
    if 'thingiverse.com/thing:' in project_name:
        return project_name.split('thing:')[1]

    if check_integer(project_name):
        return project_name

    return False
