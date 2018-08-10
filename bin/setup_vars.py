import os
import os.path
import ConfigParser
import datetime
import unittest


def get_variables(defaults_file, project_name=None):
    user_variables_file = os.path.expanduser('~/.robot_variables')

    config = ConfigParser.ConfigParser()
    try:
        config.readfp(open(defaults_file))
        if 'ROBOT_VARIABLES_FILE' in os.environ:
            config.read([os.environ['ROBOT_VARIABLES_FILE']])
        elif os.path.exists(user_variables_file):
            config.read(user_variables_file)
    except IOError:
        raise RuntimeError('Could not open variable defaults file (%s)' %
                defaults_file)

    variables = dict(config.items('Variables'))
    if project_name is not None:
        variables.update(config.items(project_name))
    for k in variables.keys():
        variables[k] = variables[k].lstrip('"').rstrip('"')
        if variables[k].startswith('EVAL:'):
            variables[k] = eval(variables[k][5:])

    return variables
