# # -*- coding: utf-8 -*-
#
# from django.template import Library
# from django.contrib.staticfiles.storage import staticfiles_storage
# from django.core.files.storage import default_storage
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
#     Example: <img src="{% email_inline_static "django/email/header.png" %}" width="780" height="11" alt=""/>
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
#     Example: <img src="{% email_inline_file "django/email/header.png" %}" width="780" height="11" alt=""/>
#     """
#     email = context.get('email_object')
#     if isinstance(email, EmailMultiRelated):
#         return 'cid:' + email.attach_related_file(default_storage.path(path))
#     return default_storage.url(path)
#
# manager_mail = EmailMultiRelated(title, to=send_to)
# mail_data['email_object'] = manager_mail
# manager_mail.body = render_to_string('email/manager-temp-disabled.html', mail_data)
# manager_mail.content_subtype = 'html'
# manager_mail.send()