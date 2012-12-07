import sys
from setuptools import find_packages, setup

try:
    import multiprocessing
except ImportError:
    pass


install_requires = [
    'eventlet',
    'kazoo',
]

tests_require = [
    'mock',
    'nose',
]

setup_requires = []
if 'nosetests' in sys.argv[1:]:
    setup_requires.append('nose')

setup(
    name='kazoo-eventlet-handler',
    version='0.1.0',
    author='ted kaemming, disqus',
    author_email='ted@disqus.com',
    url='http://github.com/disqus/kazoo-eventlet-handler',
    license='Apache License 2.0',
    packages=find_packages(exclude=('tests',)),
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    test_suite='nose.collector',
)
