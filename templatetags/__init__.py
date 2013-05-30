# # -*- coding: utf-8 -*-
#
# from django.template import Library
# from django.contrib.staticfiles.storage import staticfiles_storage
# from django.core.files.storage import default_storage
#
# from plate.tools import EmailMultiRelated
#
#
# register = Library()
#
#
# @register.simple_tag(takes_context=True)
# def email_inline_static(context, path):
#     """
#     use this tag with EmailMessageInline class,
#     tag attach inline image in email and return src attribute value
#     Example: <img src="{% email_inline_static "iplate/email/header.png" %}" width="780" height="11" alt=""/>
#     """
#     email = context.get('email_object')
#     if isinstance(email, EmailMultiRelated):
#         return 'cid:' + email.attach_related_file(staticfiles_storage.path(path))
#     return staticfiles_storage.url(path)
#
#
# @register.simple_tag(takes_context=True)
# def email_inline_file(context, path):
#     """
#     use this tag with EmailMessageInline class,
#     tag attach inline image in email and return src attribute value
#     Example: <img src="{% email_inline_file "iplate/email/header.png" %}" width="780" height="11" alt=""/>
#     """
#     email = context.get('email_object')
#     if isinstance(email, EmailMultiRelated):
#         return 'cid:' + email.attach_related_file(default_storage.path(path))
#     return default_storage.url(path)
