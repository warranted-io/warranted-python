from setuptools import setup

setup(
    name='warranted-python',
    version='1.0.0',
    description='A Warranted helper library',
    url='https://github.com/warranted-io/warranted-python',
    author='API Team <api@warranted.io>',
    author_email='api@warranted.io',
    license='MIT',
    packages=['warranted'],
    install_requires=[
        "requests >= 2.0.0",
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    keywords='warranted api',
    long_description='''
A Warranted helper library
'''
)