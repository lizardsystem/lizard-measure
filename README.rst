lizard-krw
==========================================

Introduction
------------

Store and visualize measures.


Features
--------

Measures in areas are stored and their status is tracked.

Measures can be imported from 'KRW portaal', using::

    $ bin/django import_krw_portaal

Models can be synchronized from the Aquo domain tables using::

    $ bin/django sync_aquo
    
- Waterbodies are not imported, but linked to areas via owmxxx.xml files.

Data is accessible using the REST API.


Usage
-----

*TO BE UPDATED*

- Add lizard_krw to setup.py

- Add PIL, matplotlib (more?) in buildout.cfg:sysegg

- Optionally pin lizard_krw in buildout.cfg

- Add lizard_krw in the django settings.py

- Mount lizard_krw on '^krw/' in urls.py. DO NOT MOUNT ON OTHER URL OR
  THE JS WILL NOT WORK.

    (r'^krw/', include('lizard_krw.urls')),

- Override lizard_ui/lizardbase.html template and add css and js:

    {% extends "lizard_ui/realbase.html" %}

    {% block sitetitle %}
      - Lizard Volg- en Stuursysteem
    {% endblock sitetitle %}

    {% block css %}
    {{ block.super }}
    <link type="text/css"
          href="{{ STATIC_URL }}lizard_krw/lizard_krw.css"
          rel="stylesheet" />
    {% endblock css %}

    {% block javascript %}
    {{ block.super }}
    <script type="text/javascript"
            src="{{ STATIC_URL }}lizard_krw/lizard_krw.js"></script>
    {% endblock javascript %}

    {% block portal-tabs %}
    <ul>
      <li><a href="/">Overzicht</a></li>
      <li class="selected last"><a href="/analysis">Analyse</a></li>
    </ul>
    {% endblock portal-tabs %}

- Fill waterbodies and make workspace no 1. Put them in a fixture.


Development installation
------------------------

The first time, you'll have to run the "bootstrap" script to set up setuptools
and buildout::

    $> python bootstrap.py

And then run buildout to set everything up::

    $> bin/buildout

(On windows it is called ``bin\buildout.exe``).

You'll have to re-run buildout when you or someone else made a change in
``setup.py`` or ``buildout.cfg``.

The current package is installed as a "development package", so
changes in .py files are automatically available (just like with ``python
setup.py develop``).

If you want to use trunk checkouts of other packages (instead of released
versions), add them as an "svn external" in the ``local_checkouts/`` directory
and add them to the ``develop =`` list in buildout.cfg.

Tests can always be run with ``bin/test`` or ``bin\test.exe``.

Note that since version 1.5 a lot has changed. Therefore, migrations 4 and
5 throw all tables away from previous migrations and versions and build
the entire new table set. All data present migrating to 1.5 will be lost.
