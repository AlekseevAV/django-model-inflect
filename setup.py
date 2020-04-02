#!/usr/bin/env python
from distutils.core import setup

version = '0.1.0'


setup(
    name='django-model-inflect',
    version=version,
    description='Inflect Django models.',
    long_description=(
        'The model_inflect application can be used to inflect dynamic '
        'content of existing models.'),
    author='Aleksandr Alekseev',
    author_email='alekseevavx@gmail.com',
    url='https://github.com/AlekseevAV/django-model-inflect',
    packages=['model_inflect'],
    install_requires=['Django>=2.2', 'pymorphy2'],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License'],
    license='New BSD')
