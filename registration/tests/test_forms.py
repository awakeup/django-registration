"""
Exercise django-registration's built-in form classes.

"""

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils.six import text_type

from .. import forms


class RegistrationFormTests(TestCase):
    valid_data = {
        'username': 'testuser',
        'email': 'test@example.com',
        'password1': 'swordfish',
        'password2': 'swordfish',
    }

    def test_username_format(self):
        """
        Invalid usernames are rejected.

        """
        bad_usernames = [
            'user!example', 'valid?',
        ]
        for username in bad_usernames:
            data = self.valid_data.copy()
            data.update(username=username)
            form = forms.RegistrationForm(data=data)
            self.assertFalse(form.is_valid())
            self.assertEqual(
                form.errors['username'],
                [text_type(forms.BAD_USERNAME)]
            )

    def test_user_uniqueness(self):
        """
        Existing usernames cannot be re-used.

        """
        User.objects.create(
            username='testuser',
            email='test@example.com',
            password='swordfish'
        )

        form = forms.RegistrationForm(data=self.valid_data.copy())
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['username'],
            [text_type(forms.DUPLICATE_USER)]
        )

    def test_password_match(self):
        """
        Both submitted passwords must match.

        """
        data = self.valid_data.copy()
        data.update(password2='swordfishes')
        form = forms.RegistrationForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['__all__'],
            [text_type(forms.PASSWORD_MISMATCH)]
        )

    def test_tos_field(self):
        """
        The terms-of-service field on RegistrationFormTermsOfService
        is required.

        """
        form = forms.RegistrationFormTermsOfService(
            data=self.valid_data.copy()
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['tos'],
            [text_type(forms.TOS_REQUIRED)]
        )

    def test_email_uniqueness(self):
        """
        Email uniqueness is enforced by RegistrationFormUniqueEmail.

        """
        User.objects.create(
            username='testuser2',
            email='test@example.com',
            password='swordfish'
        )

        form = forms.RegistrationFormUniqueEmail(
            data=self.valid_data.copy()
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['email'],
            [text_type(forms.DUPLICATE_EMAIL)]
        )

        data = self.valid_data.copy()
        data.update(email='test2@example.com')
        form = forms.RegistrationFormUniqueEmail(
            data=data
        )
        self.assertTrue(form.is_valid())

    def test_no_free_email(self):
        """
        Free email domains are disallowed by
        RegistrationFormNoFreeEmail.

        """
        for domain in forms.RegistrationFormNoFreeEmail.bad_domains:
            data = self.valid_data.copy()
            data.update(
                email='testuser@%s' % domain
            )
            form = forms.RegistrationFormNoFreeEmail(
                data=data
            )
            self.assertFalse(form.is_valid())
            self.assertEqual(
                form.errors['email'],
                [text_type(forms.FREE_EMAIL)]
            )

        form = forms.RegistrationFormNoFreeEmail(
            data=self.valid_data.copy()
        )
        self.assertTrue(form.is_valid())
