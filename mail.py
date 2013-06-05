# -*- coding: utf-8 -*-

import os
import hashlib
from BeautifulSoup import BeautifulSoup
from email.mime.base import MIMEBase
from django.core.mail import EmailMultiAlternatives, SafeMIMEMultipart


class EmailMultiRelatedCore(EmailMultiAlternatives):
    """
    A version of EmailMessage that makes it easy to send multipart/related
    messages. For example, including text and HTML versions with inline images.
    """
    related_subtype = 'related'

    def __init__(self, *args, **kwargs):
        self.related_attachments = []
        self.related_attachments_filename_content_id = []
        super(EmailMultiRelatedCore, self).__init__(*args, **kwargs)

    def attach_related(self, filename=None, content=None, mimetype=None, filename_content_id=None):
        """
        Attaches a file with the given filename and content. The filename can
        be omitted and the mimetype is guessed, if not provided.

        If the first parameter is a MIMEBase subclass it is inserted directly
        into the resulting message attachments.
        """
        if filename_content_id is None:
            m = hashlib.md5()
            m.update(filename)
            filename_content_id = m.hexdigest()
        if filename_content_id not in self.related_attachments_filename_content_id:
            if isinstance(filename, MIMEBase):
                assert content == mimetype == None
                self.related_attachments.append(filename)
            else:
                assert content is not None
                self.related_attachments.append((filename, content, mimetype, filename_content_id))
            self.related_attachments_filename_content_id.append(filename_content_id)
        return filename_content_id

    def attach_related_file(self, path, mimetype=None):
        """Attaches a file from the filesystem."""
        filename = os.path.basename(path)
        content = open(path, 'rb').read()
        return self.attach_related(filename, content, mimetype)

    def _create_message(self, msg):
        return self._create_attachments(self._create_related_attachments(self._create_alternatives(msg)))

    def _create_related_attachments(self, msg):
        encoding = self.encoding or 'utf-8'
        if self.related_attachments:
            body_msg = msg
            msg = SafeMIMEMultipart(_subtype=self.related_subtype, encoding=encoding)
            if self.body:
                msg.attach(body_msg)
            for related in self.related_attachments:
                msg.attach(self._create_related_attachment(*related))
        return msg

    def _create_related_attachment(self, filename, content, mimetype=None, filename_content_id=None):
        """
        Convert the filename, content, mimetype triple into a MIME attachment
        object. Adjust headers to use Content-ID where applicable.
        Taken from http://code.djangoproject.com/ticket/4771
        """
        attachment = super(EmailMultiRelated, self)._create_attachment(filename, content, mimetype)
        if filename:
            mimetype = attachment['Content-Type']
            del(attachment['Content-Type'])
            del(attachment['Content-Disposition'])
            attachment.add_header('Content-Disposition', 'inline', filename=filename)
            attachment.add_header('Content-Type', mimetype, name=filename)
            attachment.add_header('Content-ID', '<%s>' % filename_content_id)
        return attachment


class EmailMultiRelated(EmailMultiRelatedCore):
    def make_body(self, text):
        self.body = ''.join(BeautifulSoup(text).findAll(text=True)).strip()
        self.attach_alternative(text, 'text/html')

    def set_body_template(self, template_name, dictionary=None):
        """
        Render template using django template
        """

        # need to create new environment with self object
        from django.template.loader import get_template
        from django.template.context import Context

        t = get_template(template_name)
        dictionary = dictionary if dictionary is not None else {}
        dictionary['emailmultirelated_object'] = self
        self.make_body(t.render(Context(dictionary)))

    def set_body_template_jinja2(self, template_name, dictionary=None):
        """
        Render template using jinja
        required coffin
        """

        # need to create new environment with self object
        from coffin.common import CoffinEnvironment
        from django.conf import settings
        from jinja import email_embedded_media

        kwargs = {
            'autoescape': True
        }
        kwargs.update(getattr(settings, 'JINJA2_ENVIRONMENT_OPTIONS', {}))
        kwargs['extensions'].append(email_embedded_media)

        env = CoffinEnvironment(**kwargs)
        env.email_object_instance = self
        if settings.USE_I18N:
            from django.utils import translation
            env.install_gettext_translations(translation)

        template = env.get_template(template_name)
        self.make_body(template.render(dictionary))


