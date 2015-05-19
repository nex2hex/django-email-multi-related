django-email-multi-related
==========================

Send HTML emails with embedded images in Django from templates. Required [Django](https://github.com/django/django) >= 1.4 and [BeautifulSoup4](http://www.crummy.com/software/BeautifulSoup/) with `lxml` http://www.crummy.com/software/BeautifulSoup/bs4/doc/#parser-installation parser for automatically generat text version of email.

Send emails using django templates
-----
Add `emailmultirelated` to settings.INSTALLED_APPS

    from emailmultirelated.mail import EmailMultiRelated
    email = EmailMultiRelated('email title', to=['nex2hex@gmail.com'])
    email.set_body_template('email_template.html', {})
    email.send()

Example of email_template.html

	{% load emailmultirelated %}

    <html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>
      <body>
        <img src="{% email_embedded_media "path_to_image_in_media_root_dir.png" %}" alt="" />
        <img src="{% email_embedded_static "path_to_image_in_static_root_dir.png" %}" alt="" />
      </body>
    </html>

Send emails using Jinja2 templates
-----
Required [Jinja2](https://github.com/mitsuhiko/jinja2)

    from emailmultirelated.mail import EmailMultiRelated
    email = EmailMultiRelated('email title', to=['nex2hex@gmail.com'])
    email.set_body_template('email_template.html', {}, using='jinja')
    email.send()
    
Example of email_template.html

    <html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8"></head>
      <body>
        <img src="{% email_embedded_media "path_to_image_in_media_root_dir.png" %}" alt="" />
        <img src="{% email_embedded_static "path_to_image_in_static_root_dir.png" %}" alt="" />
      </body>
    </html>

How write HTML Emails
-----

  - http://24ways.org/2009/rock-solid-html-emails/
  - http://habrahabr.ru/company/badoo/blog/180579/
  - http://habrahabr.ru/post/17531/
