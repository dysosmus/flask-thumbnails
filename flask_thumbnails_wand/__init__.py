from flask_thumbnails_wand.image import Image

import os
import errno

class Thumbnail(object):

    def __init__(self, app=None):
        if app is not None:
            self.app = app
            self.init_app(self.app)
        else:
            self.app = None

    def init_app(self, app):
        self.app = app

        if not self.app.config.get('MEDIA_FOLDER', None):
            raise RuntimeError('You\'re using flask-thumbnail-wand '
                               'without having set the required MEDIA_FOLDER '
                               'setting.')

        if (self.app.config.get('MEDIA_THUMBNAIL_FOLDER', None) and
            not self.app.config.get('MEDIA_THUMBNAIL_URL', None)):
            raise RuntimeError('You\'re set MEDIA_THUMBNAIL_FOLDER setting, '
                               'need set and MEDIA_THUMBNAIL_URL setting.')

        app.config.setdefault('MEDIA_THUMBNAIL_FOLDER',
                               os.path.join(self.app.config['MEDIA_FOLDER'],
                                            ''))

        app.config.setdefault('MEDIA_URL', '/')
        app.config.setdefault('MEDIA_THUMBNAIL_URL',
                               os.path.join(self.app.config['MEDIA_URL'],
                                            ''))
        app.config.setdefault('THUMBNAIL_DEFAULT_EXTENSION', 'png')
        app.config.setdefault('THUMBNAIL_ALLOWED_EXTENSIONS', ('png', 'gif',
                                                               'jpg', 'jpeg',
                                                               'webp'))
        app.config.setdefault('THUMBNAIL_FORCE_DEFAULT_EXTENSION', False)

        app.jinja_env.filters['thumbnail'] = self.thumbnail

    def thumbnail(self, file_url, size, crop=None, quality=75, extension=None,
                  page=0):
        """
        :param file_url: url img - '/assets/media/summer.jpg'
        :param size: size return thumb - '100x100'
        :param crop: crop return thumb - 'fit', 'content-aware' or None
        :param page: page to use to generate the thumbnail of PDF file
        :param quality: JPEG quality 1-100
        :return: :thumb_url:
        """
        thumbnail_size = [int(x) for x in size.split('x')]

        url_path, basename = os.path.split(file_url)
        file_extension = os.path.splitext(basename)[1].strip('.')

        if not extension:
            extension = file_extension

        if not self.extension_is_allowed(extension):
            extension = self.app.config['THUMBNAIL_DEFAULT_EXTENSION']

        thumbnail_name = self.get_name(basename, extension, size, crop,
                                       quality, page)
        original_filename = os.path.join(self.app.config['MEDIA_FOLDER'],
                                         url_path, basename)
        thumbnail_filename = os.path.join(self.app.config['MEDIA_THUMBNAIL_FOLDER'],
                                          url_path, thumbnail_name)
        thumbnail_url = os.path.join(self.app.config['MEDIA_THUMBNAIL_URL'],
                                    url_path, thumbnail_name)

        if not os.path.exists(thumbnail_filename):
            self.make_path(thumbnail_filename)
            filename = '{filename}[{page!s}]'.format(filename=original_filename,
                                                     page=page)
            with Image(filename=filename) as img:
                img.compression_quality = quality

                if crop == 'fit':
                    img.fit(thumbnail_size)
                elif crop == 'content-aware':
                    img.liquid_rescale(thumbnail_size[0], thumbnail_size[1])
                else:
                    img.crop(right=thumbnail_size[0], bottom=thumbnail_size[1])

                img.save(filename=thumbnail_filename)

        return thumbnail_url

    def extension_is_allowed(self, extension):
        if self.app.config['THUMBNAIL_FORCE_DEFAULT_EXTENSION'] == True:
            return self.app.config['THUMBNAIL_DEFAULT_EXTENSION'] == extension

        if self.app.config['THUMBNAIL_ALLOWED_EXTENSIONS'] == True:
            return True

        return extension in self.app.config['THUMBNAIL_ALLOWED_EXTENSIONS']

    @staticmethod
    def make_path(full_path):
        directory = os.path.dirname(full_path)

        try:
            if not os.path.exists(full_path):
                os.makedirs(directory)
        except OSError as error:
            if error.errno != errno.EEXIST:
                raise

    @staticmethod
    def get_name(basename, extension, *args):
        args = [str(arg) for arg in args if arg]

        return '{name}-{unique}.{extension}'.format(name=basename,
                                                    unique='-'.join(args),
                                                    extension=extension)
