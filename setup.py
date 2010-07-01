import os, sys
from setuptools import setup, find_packages

def read_file(filename):
    path = os.path.abspath(os.path.dirname(__file__))
    filepath = os.path.join(path, filename)
    try:
        return open(filepath).read()
    except:
        return ''

setup(
    name = "django-pag-extras",
    version = __import__('django_pag_extras').get_version().replace(' ', '-'),
    url = '',
    author = 'Corey Oordt',
    author_email = 'coreyoordt@gmail.com',
    description = 'Extra pagination options for use with django-autopaginate',
    long_description = read_file('README'),
    packages = find_packages(),
    install_requires=read_file('requirements.txt'),
    include_package_data = True,
    classifiers = [
    ],
)
