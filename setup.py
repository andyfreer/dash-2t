"""
dash-2t
--------------

Dash second tier websockets and zeromq server
"""
from setuptools import setup


setup(
    name='dash-2t',
    version='1.2',
    url='http://github.com/evan82/dash-2t',
    license='MIT',
    author='Evan Duffield',
    author_email='evan@dash.org',
    description='Dash second tier websockets and zeromq server',
    long_description=__doc__,
    packages=['dash-2t'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.9',
        'python-socketio>=0.6.1',
        'python-engineio>=0.7.2'
    ],
    tests_require=[
        'coverage'
    ],
    test_suite='test_dash2t',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
