from django import template


register = template.Library()

@register.simple_tag(takes_context=True)
def page_replace(context, **kwargs):
    context_request = context['request'].GET.copy()
    for key, value in kwargs.items():
        context_request[key] = value
    for key in [k for k, v in context_request.items() if not v]:
        del context_request[key]
    return context_request.urlencode()
