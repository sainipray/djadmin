#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User as OldUser

    get_user_model = lambda: OldUser

User = get_user_model()


class Test(TestCase):
    def setUp(self):
        self.c = Client()
        self.user = User.objects.create_user(username="tests", email="tests@tests.com", password="tests")
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()

    def test_entries_access(self):
        response = self.c.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)
