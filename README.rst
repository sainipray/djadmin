===============
Djadmin
===============

Djadmin is a django admin theme

.. image:: https://img.shields.io/pypi/v/djadmin.svg
    :target: https://pypi.python.org/pypi/djadmin

.. image:: https://api.travis-ci.org/sainipray/djadmin.svg
    :target: https://travis-ci.org/sainipray/djadmin/

.. image:: https://img.shields.io/pypi/pyversions/djadmin.svg
    :target: https://travis-ci.org/sainipray/djadmin/

Overview
========
  **"NEW UPDATES"**

- Added Django 2.x.x support.

- Fixed Bugs

- Added Dashboard Tiles and Icon.

- Added edit button on listing.

- Added inlined form action buttons 

- Icon on dashboard per models.

Documentation
=============

- Installation -
   * Run ::

      pip install djadmin

   * Add 'djadmin' to your INSTALLED_APPS just before 'django.contrib.admin' ::

      'djadmin',

   * Add middleware in MIDDLEWARE_CLASSES list ::

     'djadmin.middleware.DJMiddleware',

   * Please make sure you already have 'django.template.context_processors.request' in context_processors of settings. If you don't have, please add it

   * Add in urls.py ::

      path('admin/', include('djadmin.urls')),

   * Run 'python manage.py migrate' for make visitor model ::

      python manage.py migrate

   * Run 'python manage.py collectstatic' ::

      python manage.py collectstatic

   * Now you have successfully install djadmin in your project

- Customization -
   * Add 'DJADMIN_DYNAMIC_FIELD_DISPLAY' for Enable Django admin dynamic options for models, After enable this option it's need to "migrate" model. default: False ::

       DJADMIN_DYNAMIC_FIELD_DISPLAY = True

   * Inherit DjadminMixin in your admin class of model, No need of inherit 'admin.ModelAdmin'::

      from djadmin.mixins import DjadminMixin
      from main.models import Book
      @admin.register(Book)
      class BookAdmin(DjadminMixin):
          pass

   * Another way for register DjadminMixin to Model ::

      from djadmin.mixins import DjadminMixin
      from main.models import Book
      admin.site.register(Book, DjadminMixin)

   After that you will see DjadminMixin Inherit model name in "DjadmiModelSetting" of admin like below snapshot
   then change field values with given field.You will get field to show

   Note: If any field already define in your admin class of model then that field value in DjadmiModelSetting will not work for field.

   * Add 'DJADMIN_FIELD_DEPTH' for define field depth.When any model has ForeignKey relation with another model and next model also has Foreignkey relation with another that define relation depth.default = 1 ::

        DJADMIN_FIELD_DEPTH = 2

        Ex:
        class Publisher(models.Model):
            name = models.CharField(max_length=30)

        class Book(models.Model):
            pub = models.ForeignKey(Publisher)

        class Author(models.Model):
            book = models.ForeignKey(Book)

   So, If we have Author model then depth 2 will create field in Author model:   "**book__pub__name**" for access Publisher name from Author model instance.

   * Add 'ALLOW_FORGET_PASSWORD_ADMIN' for Enable Forget password option in login page, default: Disable ::

        ALLOW_FORGET_PASSWORD_ADMIN = True
        EMAIL_USE_TLS = True
        DEFAULT_FROM_EMAIL = '<Email ID>'
        SERVER_EMAIL = '<Email ID>'
        EMAIL_HOST = '<smtp.example.com>'  #Ex: Gmail : smtp.gmail.com
        EMAIL_PORT = <Port Number>    #Ex: Gmail : 587
        EMAIL_HOST_USER = '<Email ID>'
        EMAIL_HOST_PASSWORD = '<Password>'
        EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

   * Add 'ADMIN_COLOR_THEME'  for change admin color. you can write directly name of color. default: cyan ::

        ADMIN_COLOR_THEME = 'red'

   * Add 'ADMIN_HEADER_TITLE' for change admin header title ::

        ADMIN_HEADER_TITLE  = 'Djadmin Administrator'

   * Add 'DASHBOARD_ICONS' for models icons.

   		DASHBOARD_ICONS = {
		  "MODEL_NAME1": "mdi-car",
		  "MODEL_NAME2": "mdi-coin",
		  ......
		}
   * Add Dashboard models that need to show on dashboard.
    `ALLOW_DASHBOARD_MODEL = ['Model1', 'Model2', ..]`


Screenshot
==========
.. image:: .dashboard.png
   :width: 400px

.. image:: .screen2.png
   :width: 400px

.. image:: .form_button.png
   :width: 400px

.. image:: .screen4.png
   :width: 400px

.. image:: .listing.png
   :width: 400px

License
=======

Djadmin is an Open Source project licensed under the terms of the `MIT license <https://github.com/sainipray/djadmin/blob/master/LICENSE>`_
