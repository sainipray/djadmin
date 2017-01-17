from setuptools import find_packages,setup
from distutils.core import setup

setup(
    name='djadmin',
    version='1.1.0',
    packages=find_packages(),
    url='https://github.com/sainipray/djadmin',
    author='Neeraj Kumar',
    author_email='sainineeraj1234@gmail.com',
    description='Djadmin is a django admin theme',
    license='MIT',
    include_package_data=True,
    install_requires=[
        "geocoder","user_agents"
    ],
    platforms=['any'],
    zip_safe = False,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Framework :: Django :: 1.10',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: User Interfaces',
        'Topic :: System :: Systems Administration',
    ],
)
