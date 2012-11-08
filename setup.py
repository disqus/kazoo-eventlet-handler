import sys
from setuptools import setup

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
    version='0.0.0',
    install_requires=install_requires,
    setup_requires=setup_requires,
    tests_require=tests_require,
    test_suite='nose.collector',
)
