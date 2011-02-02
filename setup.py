from setuptools import setup

version = '0.11dev'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('TODO.txt').read(),
    open('CREDITS.txt').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'pkginfo',
    'Django',
    'django-staticfiles',
    'django-extensions',
    'lizard-map',
    'lizard-ui',
    'lizard-fewsunblobbed',
    'south',
    'django-nose',
    'django-treebeard',
    ],

tests_require = [
    ]

setup(name='lizard-krw',
      version=version,
      description="Kaderrichtlijn Water (KRW)",
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
      packages=['lizard_krw'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require = {'test': tests_require},
      entry_points={
          'console_scripts': [
            ],
          'lizard_map.adapter_class': [
            'adapter_krw = lizard_krw.layers:WorkspaceItemAdapterKrw',
            ],
          },
      )
