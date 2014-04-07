from distutils.core import setup

setup(
    name='Flask-thumbnails-wand',
    version='0.1',
    url='https://github.com/dysosmus/flask-thumbnails-wand',
    license='MIT',
    author='Félix Mattrat, Dmitriy Sokolov',
    author_email='hello+flask-thumbnails-wand@dysosmus.net',
    description='A simple extension to create thumbnails for Flask, based on Wand',
    packages=['flask_thumbnails_wand'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask>=0.10',
        'Wand>=0.3',
    ],
)
