from setuptools import setup, find_packages


setup(
    name='Interstat',
    description='HTML formatter for IRC log files',
    version='0.1',
    author='Kevin Xiwei Zheng',
    author_email='blankplacement+interstat@gmail.com',
    url='https://github.com/kxz/interstat',

    install_requires=['Django'],
    tests_require=['nose'],
    test_suite='nose.collector',

    packages=find_packages(),
    package_data={'interstat': ['templates/*.css',
                                'templates/*.html',
                                'templates/message/*.html']},
    entry_points={'console_scripts': ['interstat=interstat.cli:main']})
