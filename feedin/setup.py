from distutils.core import setup
import sys

sys.path.append('feedin')


setup(name='feedin',
      version='0.1',
      author='Keven Li',
      author_email='kevenli@users.noreply.github.com',
      url='https://github.com/kevenli/FeedIn',
      download_url='https://github.com/kevenli/FeedIn',
      description='Web data fetching engine.',
      long_description='A web data fetching engine which can be used in \
          easy configuration and has multiple build-in modules.',
      packages=['feedin'],
      provides=['feedin'],
      required=['lxml'],
      keywords='web data python fetching',
      license='Apache License, Version 2.0',
      classifiers=['Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Natural Language :: English',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
                   'License :: OSI Approved :: GNU Affero General Public License v3',
                   'Topic :: Internet',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                  ],
     )