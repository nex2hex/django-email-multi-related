# -*- coding: utf-8 -*-

import os
import hashlib
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
    def make_body(self, content):
        try:
            from bs4 import BeautifulSoup, FeatureNotFound
            from bs4.element import Comment

            try:
                html = BeautifulSoup(content, 'lxml')
                # remove comments from text
                for c in html.find_all(text=lambda t: isinstance(t, Comment)):
                    c.extract()

                # set links from a tag to text
                for tag in html.find_all(True):
                    if tag.name == 'a':
                        href = tag.attrs.get('href', '')
                        if href and not href.startswith('#'):
                            contents = reduce(lambda x, y: unicode(x) + unicode(y), tag.contents) if tag.contents else ''
                            if href.find(contents) != -1:
                                tag.replace_with(' %s ' % href)
                            elif href != contents:
                                tag.replace_with('%s %s ' % (contents, href))
                # trim each line in plaintext
                text = []
                for line in html.get_text().strip().split('\n'):
                    text.append(line.strip(' \t\n\r'))
                text = '\r\n'.join(text)

                # plaintext version comes first to set better preheaders
                self.body = text
                self.attach_alternative(content, 'text/html')
            except FeatureNotFound:
                pass
        except ImportError:
            pass

    def set_body_template(self, template_name, context=None):
        """
        Render template using django template
        """

        # need to create new environment with self object
        from django.template.loader import get_template
        from django.template.context import Context

        t = get_template(template_name)
        dictionary = context if context is not None else {}
        dictionary['emailmultirelated_object'] = self
        self.make_body(t.render(Context(dictionary)))

    def set_body_template_jinja2(self, template_name=None, context=None, template=None):
        """
        Render template using jinja
        required coffin
        """

        # need to create new environment with self object
        from coffin.common import get_env
        from jinja import email_embedded_media

        env = get_env()
        env.add_extension(email_embedded_media)
        env.email_object_instance = self
        template_code = env.from_string(template) if template else env.get_template(template_name)
        self.make_body(template_code.render(context))


