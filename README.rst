===============
Djadmin
===============

Djadmin is django admin theme

Overview
========

- Visior - Add visitor model for administrator location on each login and show graph of login device

- Forget Password Option - Admin can enable or disable forget password option on admin login

- Theme Color - Change theme color of admin

- Admin Header Title - Change django admin header title

- Admin Language - Change django admin language using language short code

Documentation
=============

- Installation -
   * Run ::

      pip install djadmin

   * Add 'djadmin' in INSTALLED_APPS list at Top position ::

      'djadmin',

   * Add middleware in MIDDLEWARE_CLASSES list ::

     'djadmin.middleware.DJMiddleware',

   * Add in urls.py ::

      url(r'^admin/', include('djadmin.urls')),

   * Run 'python manage.py migrate' for make visitor model ::

      python manage.py migrate

   * Run 'python manage.py collectstatic' ::

      python manage.py collectstatic

   * Now you have successfully install djadmin in your project

- Customization -
   * Add 'ALLOW_FORGET_PASSWORD_ADMIN' for Enable Forget password option in login page, default: Disable ::

        ALLOW_FORGET_PASSWORD_ADMIN = True

   * Add 'ADMIN_COLOR_THEME'  for change admin color. you can write directly name of color. default: cyan ::

        ADMIN_COLOR_THEME = 'red'

   * Add 'ADMIN_LANGUAGE' for particular language.Use language short code.check language code at `Language code list in django <https://github.com/django/django/blob/master/django/conf/locale/__init__.py>`_ . default: 'en'::

        ADMIN_LANGUAGE = 'fr'
   * Add 'ADMIN_HEADER_TITLE' for change admin header title ::

        ADMIN_HEADER_TITLE  = 'Djadmin Administrator'

License
=======

Djadmin is an Open Source project licensed under the terms of the `MIT license <https://github.com/sainipray/djadmin/blob/master/LICENSE>`_

