from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from .models import Notifications
from core import settings

User = get_user_model()

@receiver(post_save, sender=Notifications)
def send_notification_email(sender, instance, created, **kwargs):
    if not created:
        return  # Só envia e-mail quando for um novo aviso

    subject = "🔔 Novo Aviso Publicado"

    # Se tiver destinatários específicos, pega eles
    recipient_list = list(instance.recipients.values_list('email', flat=True))

    # Se não tiver destinatários definidos, envia para todos os usuários ativos
    if not recipient_list:
        recipient_list = list(User.objects.filter(is_active=True).values_list('email', flat=True))

    # Renderiza o template HTML
    html_content = render_to_string('notifications/email_template.html', {
        'resume': instance.resume,
        'redator': instance.redator.username if instance.redator else 'Anônimo',
        'created_at': instance.created_at.strftime('%d/%m/%Y %H:%M'),
    })

    # Remove HTML para versão alternativa em texto puro
    text_content = strip_tags(html_content)

    # Configura e envia o e-mail
    email = EmailMultiAlternatives(subject, text_content, 'seu-email@gmail.com', recipient_list)
    email.attach_alternative(html_content, "text/html")
    email.send()
