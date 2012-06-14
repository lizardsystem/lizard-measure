from setuptools import setup

version = '1.78'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('TODO.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'pkginfo',
    'Django',
    'django-staticfiles',
    'django-extensions',
    'lizard-area',
    'lizard-esf',
    'lizard-history >= 0.2.3',
    'lizard-graph',
    'lizard-geo',
    'lizard-map >= 1.71',
    'lizard-ui',
    'lizard-security',
    'lizard-layers >= 0.4.2',
    'iso8601',
    'lxml',
    'south',
    'suds',
    'django-nose',
    'django-treebeard',
    ],

tests_require = [
    ]

setup(name='lizard-measure',
      version=version,
      description="Maatregelen",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=[],
      author='Jack Ha',
      author_email='jack.ha@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['lizard_measure'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require = {'test': tests_require},
      entry_points={
          'console_scripts': [
            ],
          },
      )
