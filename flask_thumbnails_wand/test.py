# -*- coding: utf-8 -*-

import os
import unittest

from shutil import rmtree
from tempfile import gettempdir
from uuid import uuid4
from flask import Flask
from flask.ext.thumbnails_wand import Thumbnail


class ThumbnailTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)

        self.tempdir = gettempdir()

        self.app.config['TESTING'] = True
        self.app.config['MEDIA_FOLDER'] = os.path.join(self.tempdir,
                                                       'thumbnails')
        self.app.config['MEDIA_URL'] = '/uploads/'

        self.thumbnail = Thumbnail(self.app)


    def test_make_path(self):
        """
            Test if make_path create all directories from the full filename
        """
        full_filename = os.path.join(self.tempdir,
                                     'make_path',
                                     str(uuid4()), 'image.png')

        self.thumbnail.make_path(full_filename)

        path = os.path.dirname(full_filename)

        self.assertTrue(os.path.exists(path))

    def test_get_name(self):
        """
            Test if the result of Thumbnail.get_name return a constant result
            for the given args.
        """
        values = ((('image.jpg', 'jpg', '200x200', 'fit', 100), 'image.jpg-200x200-fit-100.jpg'),
                   (('image.jpg', 'jpg', '200x200', 'fit', '100'), 'image.jpg-200x200-fit-100.jpg'),
                   (('image.jpg', 'jpg', '200x200'), 'image.jpg-200x200.jpg'),
                   (('image.png', 'jpg', '200x200'), 'image.png-200x200.jpg'),
                   (('image.pdf', 'png', '200x200'), 'image.pdf-200x200.png'),
                   (('image', 'png', '200x200'), 'image-200x200.png'),)

        for args, excepted in values:
            name = self.thumbnail.get_name(*args)
            self.assertEquals(name, excepted)

    def test_extension_is_allowed_restricted_extensions(self):
        """
           Test if the extensions are correctly restricted to the list of
           THUMBNAIL_ALLOWED_EXTENSIONS
        """
        self.app.config['THUMBNAIL_ALLOWED_EXTENSIONS'] = ('png', 'jpg',
                                                           'jpeg', 'gif')

        for extension in ('png', 'jpg', 'jpeg', 'gif'):
            self.assertTrue(self.thumbnail.extension_is_allowed(extension))

        for extension in ('.png', 'webp', 'svg'):
            self.assertFalse(self.thumbnail.extension_is_allowed(extension))

    def test_extension_is_allowed_force_extension(self):
        """
            Test if THUMBNAIL_FORCE_DEFAULT_EXTENSION correctly force the
            default extension when this one is True.
        """
        self.app.config['THUMBNAIL_DEFAULT_EXTENSION'] = 'png'
        self.app.config['THUMBNAIL_FORCE_DEFAULT_EXTENSION'] = True

        self.assertTrue(self.thumbnail.extension_is_allowed('png'))

        for extension in ('.png', 'webp', 'svg', 'jpg', 'gif'):
            self.assertFalse(self.thumbnail.extension_is_allowed(extension))

    def test_extension_is_allowed_all_extensions(self):
        """
            Test if THUMBNAIL_ALLOWED_EXTENSIONS allow all extensions when
            this one is True
        """
        self.app.config['THUMBNAIL_FORCE_DEFAULT_EXTENSION'] = False
        self.app.config['THUMBNAIL_ALLOWED_EXTENSIONS'] = True

        for extension in ('.png', 'webp', 'svg', 'jpg', 'gif', 'pdf'):
            self.assertTrue(self.thumbnail.extension_is_allowed(extension))

    def test_extension_is_allowed_force_extension_override_all_extensions(self):
        """
            Test if the THUMBNAIL_FORCE_DEFAULT_EXTENSION override
            THUMBNAIL_ALLOWED_EXTENSIONS when THUMBNAIL_FORCE_DEFAULT_EXTENSION
            and THUMBNAIL_ALLOWED_EXTENSIONS is True
        """
        self.app.config['THUMBNAIL_DEFAULT_EXTENSION'] = 'png'
        self.app.config['THUMBNAIL_FORCE_DEFAULT_EXTENSION'] = True
        self.app.config['THUMBNAIL_ALLOWED_EXTENSIONS'] = True

        self.assertTrue(self.thumbnail.extension_is_allowed('png'))

        for extension in ('.png', 'webp', 'svg', 'jpg', 'gif', 'pdf'):
            self.assertFalse(self.thumbnail.extension_is_allowed(extension))

    def test_extension_is_allowed_force_extension_override_restricted_extensions(self):
        """
            Test if the THUMBNAIL_FORCE_DEFAULT_EXTENSION override
            THUMBNAIL_ALLOWED_EXTENSIONS when THUMBNAIL_FORCE_DEFAULT_EXTENSION
            is True and THUMBNAIL_ALLOWED_EXTENSION list a list of extensions
        """
        self.app.config['THUMBNAIL_DEFAULT_EXTENSION'] = 'png'
        self.app.config['THUMBNAIL_FORCE_DEFAULT_EXTENSION'] = True
        self.app.config['THUMBNAIL_ALLOWED_EXTENSIONS'] = ('png', 'jpg')

        self.assertTrue(self.thumbnail.extension_is_allowed('png'))

        for extension in ('.png', 'webp', 'svg', 'jpg', 'gif', 'pdf'):
            self.assertFalse(self.thumbnail.extension_is_allowed(extension))

    def tearDown(self):
        rmtree(self.tempdir, ignore_errors=True)
