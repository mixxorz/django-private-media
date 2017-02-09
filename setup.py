import os
from setuptools import setup, find_packages

import private_media

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-private-media',
    version=private_media.__version__,
    packages=find_packages(),
    include_package_data=True,
    license=private_media.__license__,
    description=private_media.__doc__,
    long_description=README,
    keywords="private media xsendfile",
    url='https://github.com/RacingTadpole/django-private-media',
    author='Arthur Street',
    author_email='arthur@racingtadpole.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    zip_safe=False)
