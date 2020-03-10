from flask import current_app
from fluent import event


def log(method_name, dict):
    event.Event(method_name, dict)
    current_app.logger.info(method_name + ' ' + str(dict))
