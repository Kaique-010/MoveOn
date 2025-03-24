from django import template

register = template.Library()

@register.filter
def get_color(value):
    """
    Retorna a cor de fundo com base na prioridade do ticket.
    """
    if value == 'low':
        return '#00c16c'
    elif value == 'medium':
        return '#ffc52c'
    elif value == 'high':
        return '#ff9915'
    elif value == 'critical':
        return '#CC3733'
    return 'gray'  # Valor padrão, caso não tenha correspondência
