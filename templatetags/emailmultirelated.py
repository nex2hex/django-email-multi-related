# # -*- coding: utf-8 -*-

from django.template import Library
from django.contrib.staticfiles.storage import staticfiles_storage
from django.core.files.storage import default_storage

from ..mail import EmailMultiRelated


register = Library()


@register.simple_tag(takes_context=True)
def email_embedded_static(context, path):
    """
    use this tag with EmailMultiRelated class,
    tag attach inline image in email and return src attribute value
    Example: <img src="{% email_inline_static "django/email/header.png" %}" width="780" height="11" alt=""/>
    """
    email = context.get('emailmultirelated_object')

    if isinstance(email, EmailMultiRelated):
        return 'cid:' + email.attach_related_file(staticfiles_storage.path(path))
    return staticfiles_storage.url(path)


@register.simple_tag(takes_context=True)
def email_embedded_media(context, path):
    """
    use this tag with EmailMultiRelated class,
    tag attach inline image in email and return src attribute value
    Example: <img src="{% email_inline_file "django/email/header.png" %}" width="780" height="11" alt=""/>
    """
    email = context.get('emailmultirelated_object')

    if isinstance(email, EmailMultiRelated):
        return 'cid:' + email.attach_related_file(default_storage.path(path))
    return default_storage.url(path)