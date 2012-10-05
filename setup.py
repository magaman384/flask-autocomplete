from setuptools import setup, find_packages

tests_require = ['Flask-Testing', 'Flask-WTF']

setup(
    name='flask-autocomplete',
    version='0.1',
    author='Marian Galik',
    packages=find_packages(),
    install_requires=['flask', 'wtforms'],
    tests_require=tests_require,
    extras_require={'test': tests_require}
)