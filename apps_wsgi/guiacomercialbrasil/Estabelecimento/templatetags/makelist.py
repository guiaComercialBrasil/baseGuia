from django import template

register = template.Library()

@register.filter
def makelist(value, sep):
    ''' Make Readable List From QuerySet '''

    if str(sep) not in [";", ",", ".", "-", "_", "/", "\\", "|"]:
        raise Exception("Invalid Separator. Valid Separators are ; , . - _ / \\ |")
    return "{} ".format(sep).join([str(name) for name in value[:5]])
