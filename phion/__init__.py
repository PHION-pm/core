from datetime import date, datetime
import os
from pathlib import Path
import re
from PIL import Image
import urllib.request
import pickle
import shutil


HOME_DIR = Path.home()
DB_DIR = f"{HOME_DIR}/.config/phion/phion.db"

class File():
    def __init__(self, name, location, parent=None):
        self.name = name
        self.location = location
        self.parent = parent


class WM():
    def __init__(self, name, files=[]):
        self.name = name
        self.files = files


class Program():
    def __init__(self, name,files=[]):
        self.name = name
        self.files = files


class ColorScheme():
    def __init__(self, name, colors={}):
        self.name = name
        self.colors = colors

        _colors = {}
        if type(self.colors) == list:
            for i in colors:
                if colors.index(i) <= 16:
                    _colors[f'color{colors.index(i)}'] = i
                elif colors.index(i) == 17:
                    _colors['background'] = i
                elif colors.index(i) == 18:
                    _colors['foreground'] = i


class Wallpaper():
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.ext = location.split('.')[-1]

        # get image
        img = Image.open(location)
        
        # get width and height
        self.width = img.width
        self.height = img.height


class Package():
    def __init__(self, name, author, description="", date_created=datetime.now(), version='0.0.1', wallpapers=[], color_schemes=[], WMs=[], programs=[]):
        self.name = name
        self.author = author
        self.date_created = date_created
        self.description = description
        self.version = version
        
        self.wallpapers = wallpapers
        self.color_schemes = color_schemes
        self.WMs = WMs
        self.programs = programs

        self.formatted_name = re.sub('[^A-Za-z0-9]+', '', self.name)

    
    def __dump_phn():
        pass

    def __move_wallpapers(self, package_dir):
        os.makedir(f"{package_dir}/wallpapers")
        for wallpaper in self.wallpapers:

            if 'http' in wallpaper.location:
                urllib.request.urlretrieve(wallpaper.location, f"{package_dir}/wallpapers/{wallpaper.name}.{wallpaper.ext}")
            else:
                shutil.copyfile(wallpaper.location, f"{package_dir}/wallpapers/{wallpaper.name}.{wallpaper.ext}")


    def save(self, location=f"{HOME_DIR}/.config/phion/packages/"):

        package_dir = f"{location}/{self.formatted_name}"
        os.makedir(package_dir)

        self.__move_wallpapers(package_dir)






