from setuptools import find_packages,setup
import djadmin
setup(
    name=djadmin.__name__,
    version=djadmin.__version__,
    packages=find_packages(),
    url='https://github.com/sainipray/djadmin',
    author=djadmin.__author__,
    author_email=djadmin.__author_email__,
    description=djadmin.__description__,
    license='MIT',
    include_package_data=True,
    install_requires=[
        "geocoder","user_agents"
    ],
    platforms=['any'],
    zip_safe = False,
    classifiers=[
        'Development Status :: 4 - Beta',
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
