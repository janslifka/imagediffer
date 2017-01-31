import os
from setuptools import setup, find_packages


install_requires = ['numpy', 'Pillow', 'pyssim', 'requests', 'scipy']

if os.environ.get('TRAVIS') is None and os.environ.get('READTHEDOCS') is None:
    install_requires.append('PyQt5')

setup_requires = ['pytest-runner']
tests_requires = ['pytest']

setup(
    name='imagediffer',
    version='0.1.4',
    description='Tool for image diffs.',
    author='Jan Slifka',
    author_email='slifkjan@fit.cvut.cz',
    url='https://github.com/janslifka/imagediffer',
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_requires=tests_requires
)
