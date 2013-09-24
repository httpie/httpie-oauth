from setuptools import setup
try:
    import multiprocessing
except ImportError:
    pass


setup(
    name='httpie-oauth',
    description='OAuth plugin for HTTPie.',
    long_description=open('README.rst').read().strip(),
    version='1.0.2',
    author='Jakub Roztocil',
    author_email='jakub@roztocil.name',
    license='BSD',
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
