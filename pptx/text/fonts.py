# encoding: utf-8

"""
Objects related to system font file lookup.
"""

from __future__ import absolute_import, print_function

import os
import sys


class FontFiles(object):
    """
    A class-based singleton serving as a lazy cache for system font details.
    """

    _font_files = None

    @classmethod
    def find(cls, family_name, is_bold, is_italic):
        """
        Return the absolute path to the installed OpenType font having
        *family_name* and the styles *is_bold* and *is_italic*.
        """
        if cls._font_files is None:
            cls._font_files = cls._installed_fonts()
        return cls._font_files[(family_name, is_bold, is_italic)]

    @classmethod
    def _installed_fonts(cls):
        """
        Return a dict mapping a font descriptor to its font file path,
        containing all the font files resident on the current machine. The
        font descriptor is a (family_name, is_bold, is_italic) 3-tuple.
        """
        fonts = {}
        for d in cls._font_directories():
            for key, path in cls._iter_font_files_in(d):
                fonts[key] = path
        return fonts

    @classmethod
    def _font_directories(cls):
        """
        Return a sequence of directory paths likely to contain fonts on the
        current platform.
        """
        if sys.platform.startswith('darwin'):
            return cls._os_x_font_directories()
        if sys.platform.startswith('win32'):
            return cls._windows_font_directories()
        raise OSError('unsupported operating system')

    @classmethod
    def _iter_font_files_in(cls, directory):
        """
        Generate the OpenType font files found in and under *directory*. Each
        item is a key/value pair. The key is a (family_name, is_bold,
        is_italic) 3-tuple, like ('Arial', True, False), and the value is the
        absolute path to the font file.
        """
        for root, dirs, files in os.walk(directory):
            for filename in files:
                file_ext = os.path.splitext(filename)[1]
                if file_ext.lower() not in ('.otf', '.ttf'):
                    continue
                path = os.path.abspath(os.path.join(root, filename))
                with _Font.open(path) as f:
                    yield ((f.family_name, f.is_bold, f.is_italic), path)

    @classmethod
    def _os_x_font_directories(cls):
        """
        Return a sequence of directory paths on a Mac in which fonts are
        likely to be located.
        """
        os_x_font_dirs = [
            '/Library/Fonts',
            '/Network/Library/Fonts',
            '/System/Library/Fonts',
        ]
        home = os.environ.get('HOME')
        if home is not None:
            os_x_font_dirs.extend([
                os.path.join(home, 'Library', 'Fonts'),
                os.path.join(home, '.fonts')
            ])
        return os_x_font_dirs

    @classmethod
    def _windows_font_directories(cls):
        """
        Return a sequence of directory paths on Windows in which fonts are
        likely to be located.
        """
        raise NotImplementedError


class _Font(object):
    """
    A wrapper around an OTF/TTF font file stream that knows how to parse it
    for its name and style characteristics, e.g. bold and italic.
    """

    @classmethod
    def open(cls, font_file_path):
        """
        Return a |_Font| instance loaded from *font_file_path*.
        """
        raise NotImplementedError