from django import template
from django.urls import resolve
from Customizacao.models import Customizacao

register = template.Library()

class CustomizationNode(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):

        namespace = resolve(context.get("request").path_info).url_name

        try:
            customizacao = Customizacao.objects.get(pagina = namespace)

            with context.push():

                context["custom"] = {}

                context["custom"]["primary"] = customizacao.texto_1
                context["custom"]["secondary"] = customizacao.texto_2

                output = self.nodelist.render(context)

        except Customizacao.DoesNotExist:
            output = self.nodelist.render(context)

        return output


@register.tag("customization")
def customize(parser, token):
    nodelist = parser.parse(('endcustomization',))
    parser.delete_first_token()
    return CustomizationNode(nodelist)









#@register.simple_tag(takes_context = True)
#def customize(context):
#
#    path = context.get("request").path.strip("/")
#    customizacao = Customizacao.objects.get(pagina = path)
#
#    return customizacao
