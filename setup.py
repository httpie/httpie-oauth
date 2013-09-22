from setuptools import setup
try:
    import multiprocessing
except ImportError:
    pass

import httpie_oauth


setup(
    name='httpie-oauth',
    description=httpie_oauth.__doc__.strip(),
    long_description=open('README.rst').read().strip(),
    version=httpie_oauth.__version__,
    author=httpie_oauth.__author__,
    author_email='jakub@roztocil.name',
    license=httpie_oauth.__licence__,
    url='https://github.com/jkbr/httpie-oauth',
    download_url='https://github.com/jkbr/httpie-oauth',
    py_modules=['httpie_oauth'],
    zip_safe=False,
    entry_points={
        'httpie.plugins.auth.v1': [
            'httpie_oauth1 = httpie_oauth:OAuth1Plugin'
        ]
    },
    install_requires=[
        'httpie>=0.7.0',
        'requests-oauthlib>=0.3.2'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Environment :: Plugins',
        'License :: OSI Approved :: BSD License',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities'
    ],
)
