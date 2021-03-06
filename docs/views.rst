.. _views:
.. module:: registration.views

Base view classes
=================

In order to allow the utmost flexibility in customizing and supporting
different workflows, ``django-registration`` makes use of Django's
support for `class-based views
<https://docs.djangoproject.com/en/1.8/topics/class-based-views/>`_. Included
in ``django-registration`` are two base classes which can be
subclassed to implement whatever workflow is required.

.. class:: RegistrationView

   A subclass of Django's `FormView
   <https://docs.djangoproject.com/en/1.8/ref/class-based-views/generic-editing/#formview>`_,
   which provides the infrastructure for supporting user registration.

   Since it's a subclass of ``FormView``, ``RegistrationView`` has all
   the usual attributes and methods you can override.

   When writing your own subclass, one method is required:

   .. method:: register(**cleaned_data)

      Implement your registration logic here. ``cleaned_data`` will be
      the dictionary of data supplied by the user during the
      registration process (i.e., the ``cleaned_data`` from a valid
      instance of :class:`registration.forms.RegistrationForm` or a
      subclass of it).

      This method should return the newly-registered user instance,
      and should send the signal
      :data:`registration.signals.user_registered`.

   Useful optional places to override or customize on a
   ``RegistrationView`` subclass are:

   .. attribute:: disallowed_url

      The URL to redirect to when registration is disallowed. Should
      be a `string name of a URL pattern
      <https://docs.djangoproject.com/en/1.8/topics/http/urls/#naming-url-patterns>`_.
      Default value is ``"registration_disallowed"``.

   .. attribute:: form_class

      The form class to use for user registration. Can be overridden
      on a per-request basis (see below). Should be the actual class
      object; by default, this class is
      :class:`registration.forms.RegistrationForm`.

   .. attribute:: success_url

      The URL to redirect to after successful registration. Should be
      a string name of a URL pattern, or a 3-tuple of arguments
      suitable for passing to Django's `redirect shortcut
      <https://docs.djangoproject.com/en/1.8/topics/http/shortcuts/#redirect>`_. Can
      be overridden on a per-request basis (see below). Default value
      is ``None``, so that per-request customization is used instead.

   .. attribute:: template_name

      The template to use for user registration. Should be a
      string. Default value is
      ``registration/registration_form.html``.

   .. method:: get_form_class()

      Select a form class to use on a per-request basis. If not
      overridden, will use :attr:`~form_class`. Should be the actual
      class object.

   .. method:: get_success_url(user)

      Return a URL to redirect to after successful registration, on a
      per-request or per-user basis. If not overridden, will use
      :attr:`~success_url`. Should be a string name of a URL pattern,
      or a 3-tuple of arguments suitable for passing to Django's
      ``redirect`` shortcut.

   .. method:: registration_allowed()

      Should return a boolean indicating whether user registration is
      allowed, either in general or for this specific request.

   .. method:: get_user_kwargs(**cleaned_data)

      Given the cleaned_data from the registration form, return from
      them a dictionary of keyword arguments to be used in
      user-account creation. By default, this is a dictionary with
      values for the ``USERNAME_FIELD`` of the user model, along with
      email and password, to match the signature of Django's default
      ``User.objects.create_user()`` implementation, and assumes the
      field names of the default
      :class:`~registration.forms.RegistrationForm` class.


.. class:: ActivationView

   A subclass of Django's `TemplateView
   <https://docs.djangoproject.com/en/1.8/ref/class-based-views/base/#templateview>`_
   which provides support for a separate account-activation step, in
   workflows which require that.

   One method is required:

   .. method:: activate(*args, **kwargs)

      Implement your activation logic here. You are free to configure
      your URL patterns to pass any set of positional or keyword
      arguments to ``ActivationView``, and they will in turn be passed
      to this method.

      This method should return the newly-activated user instance (if
      activation was successful), or boolean ``False`` if activation
      was not successful.

   Useful places to override or customize on an ``ActivationView``
   subclass are:

   .. attribute:: template_name

      The template to use for user activation. Should be a
      string. Default value is ``registration/activate.html``.

   .. method:: get_success_url(user)

      Return a URL to redirect to after successful registration, on a
      per-request or per-user basis. If not overridden, will use
      :attr:`~success_url`. Should be a string name of a URL
      pattern, or a 3-tuple of arguments suitable for passing to
      Django's ``redirect`` shortcut.
