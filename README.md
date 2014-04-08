Flask-thumbnails-wand
===============

[![Build Status](https://travis-ci.org/dysosmus/flask-thumbnails-wand.svg?branch=master)](https://travis-ci.org/dysosmus/flask-thumbnails-wand)

Flask extension to create thumbnails, based on Wand (ImageMagick).<br />
This is a fork of [Flask-thumbnails](https://github.com/SilentSokolov/flask-thumbnails).

Support
=======

* Python 2.6, 2.7 and 3.4
* All files suported by ImageMagick (jpg, png, gif, pdf...)

Installation
===============

Install with ``pip``:

Run ``pip install git+https://github.com/dysosmus/flask-thumbnails-wand.git``

Add ``Thumbnail`` to your extension file:

    from flask.ext.thumbnails_wand import Thumbnail

    app = Flask(__name__)

    thumb = Thumbnail(app)

Add ``MEDIA_FOLDER`` and ``MEDIA_URL`` in your settings:

    app.config['MEDIA_FOLDER'] = '/home/www/media'
    app.config['MEDIA_URL'] = '/media/'

### Notes
If you want to use the content aware crop method, you need to install ImageMagick with the Liquid Rescale support.

Usage
===============

Use in Jinja2 template:

    <img src="{{ 'image.jpg'|thumbnail('200x200') }}" alt="" />
    <img src="{{ 'image.jpg'|thumbnail('200x200', crop='fit', quality=100) }}" alt="" />
    <img src="{{ 'image.jpg'|thumbnail('200x200', extension='png') }}" alt="" />
    <img src="{{ 'image.jpg'|thumbnail('200x200', crop='content-aware') }}" alt="" />

### Options

``crop``

* ``fit`` returns a sized and cropped version of the image, cropped to the requested aspect ratio and size, this method respect the implemention of  [PIL.ImageOps.fit](http://pillow.readthedocs.org/en/latest/reference/ImageOps.html#PIL.ImageOps.fit).
* ``content-aware``.

``quality`` changes the quality of the output JPEG thumbnail, default ``75``.

``extension`` save the thumbnail in the specified format, default ``None``.

``page`` page number of PDF file to use for generate the thumbnail, default ``0``.


Optional settings
===============

### ``MEDIA_FOLDER``

If you want to store the thumbnail in a folder other than the ``MEDIA_FOLDER``, you need to set it manually:

    app.config['MEDIA_THUMBNAIL_FOLDER'] = '/home/www/media/cache'
    app.config['MEDIA_THUMBNAIL_URL'] = '/media/cache/'

### ``THUMBNAIL_ALLOWED_EXTENSIONS``

The default configuration allow only ``png``, ``gif``, ``jpg``, ``jpeg`` or ``webp`` as output formats for thumbnail:

	app.config['THUMBNAIL_ALLOWED_EXTENSIONS'] = ('png', 'webp') # allow only png and webp

	app.config['THUMBNAIL_ALLOWED_EXTENSIONS'] = True # don't check the output format


### ``THUMBNAIL_DEFAULT_EXTENSION``

The default extenstion to use as output format when the file passed isn't a image (eg. PDF file) or is not in ``THUMBNAIL_ALLOWED_EXTENSIONS``, default ``png``:

	app.config['THUMBNAIL_DEFAULT_EXTENSION'] = 'jpg'

### ``THUMBNAIL_FORCE_DEFAULT_EXTENSION``

Force the default extension if extension is not explicitly passed to the ``thumbnail`` method, default ``False``:

	app.config['THUMBNAIL_FORCE_DEFAULT_EXTENSION'] = True


Develop and Production
===============

### Production

In production, you need to add media directory in your web server.


### Development
To service the uploaded files need a helper function, where ``/media/`` your settings ``app.config['MEDIA_URL']``:

    from flask import send_from_directory

    @app.route('/media/<regex("([\w\d_/-]+)?.(?:jpe?g|gif|png)"):filename>')
    def media_file(filename):
        return send_from_directory(app.config['MEDIA_THUMBNAIL_FOLDER'], filename)

