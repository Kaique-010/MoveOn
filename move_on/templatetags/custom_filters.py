from django import template

register = template.Library()

@register.filter
def get_color(value):
    """
    Retorna a cor de fundo com base na prioridade do ticket.
    """
    if value == 'low':
        return 'green'
    elif value == 'medium':
        return 'yellow'
    elif value == 'high':
        return 'orange'
    elif value == 'critical':
        return 'red'
    return 'gray'  # Valor padrão, caso não tenha correspondência
