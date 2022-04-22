import sys
import os
from pathlib import Path
import time

import urllib3

from phion import Package
from phion import Wallpaper
from phion.utils import *
from phion.enums

import argparse
from importlib.metadata import version
import sqlite3
from alive_progress import alive_bar 
from loguru import logger

from PIL import Image

from time import sleep
# logger = logging.getLogger('alive_progress')
HOME_DIR = Path.home()
DB_DIR = f"{HOME_DIR}/.config/phion/phion.db"

def __add_wallpaper(package):
    while True:
        clearConsole()
        print("--------------------------------")
        print("Add Wallpaper\n")
        wallpaper_name = input("Wallpaper Name: ")
        file_path = input("Wallpaper Full Path (or link): ")



        if "http" in file_path:
            logger.debug("File Location set as a URL")
            urllib3.request.urlretrieve(file_path,wallpaper_name.replace(" ", "")+'.'+file_path.split(".")[-1])
            try:
                logger.info(f"Downloading Image to" + wallpaper_name.replace(" ", "")+'.'+file_path.split('.')[-1])
                urllib3.request.urlretrieve(file_path,wallpaper_name.replace(" ", "")+'.'+file_path.split(".")[-1])
            except:
                logger.error("Could not retrieve wallpaper")
            else:
                logger.info("Successfully retrieved wallpaper") 
                file_path = wallpaper_name.replace(" ", "")+'.'+file_path.split(".")[-1]
                new_wallpaper = Wallpaper(name=wallpaper_name, location=file_path)
                package.wallpapers.append(new_wallpaper)
                logger.success("Wallpaper added successfully")
                break
        
        else:
            logger.debug("File Location as local file")
            if os.path.exists(file_path):
                logger.debug("File Exists as local file")
                try:
                    logger.debug("Checking file type")
                    __im=Image.open(file_path)
                except IOError:
                    logger.error("Not a valid image file")
                else:
                    logger.info("File is an Image")
                    new_wallpaper = Wallpaper(name=wallpaper_name, location=file_path)
                    logger.debug("Created new wallpaper object")
                    package.wallpapers.append(new_wallpaper)
                    logger.info("Wallpaper added to package")
                    break
            else:
                logger.error("File Not Found")

        time.sleep(2)



def __remove_wallpaper(package, wallpaper_index):
    removed_wallpaper = package.wallpapers.pop(wallpaper_index)
    logger.info(f"Removed wallpaper '{removed_wallpaper.name}' from package")


def _edit_wallpapers(package):
    clearConsole()

    while True:
        print("--------------------------------\n")


        menu = {
            'A': 'Add Wallpapers',
            'B': 'Go Back'
        }


        logger.info(f"Found {len(package.wallpapers)} wallpaper in this package.\n")
        if len(package.wallpapers) != 0:
            for wallpaper in package.wallpapers:
                print(f"[{package.wallpapers.index(wallpaper)}] {wallpaper.name} -> {wallpaper.location}")
            print("\n")
            menu[f'0-{len(package.wallpapers)-1}'] = 'Select Wallpaper to remove'

        else:
            pass

        for key, option in menu.items():
            print(f"[{key}] - {option}")

        _choice = input("\n: ")

        if _choice.upper() in menu.keys():
            try:
                if _choice.upper() == 'A':
                    __add_wallpaper(package)
                elif _choice.upper() == 'B':
                    break
            except:
                pass
 
        else:
            try:
                logger.debug(f"Wallpapers in package: { len(package.wallpapers)}")
                logger.debug(f"Choice in selection:{int(_choice) in list(range(0,len(package.wallpapers)+1))}")

                if len(package.wallpapers) > 0 and int(_choice) in list(range(0,len(package.wallpapers)+1)):
                    __remove_wallpaper(package, int(_choice))
            except:
                pass
        

def _edit_colorschemes(package):
    pass

def _configure_wm(package):
    pass

def _configure_programs(package):
    pass

def _save_package(package):
    pass

def _quit(_=None):
    sys.exit()

def package_wizard():
    while True:
        clearConsole()
        print("""PHION PACKAGE CREATION WIZARD\n""")
        time.sleep(0.4)


        package_name = dinput("Package Name: ")

        if package_name != None and package_name.isspace() == False and package_name!="":
            break
        else:
            logger.error("Package Name cannot be empty")
            time.sleep(0.7)
            continue

    package_author = dinput("Package Author", os.getlogin())
    package_description = dinput("Package Description (default=None): ")

    current_package = Package(name=package_name, author=package_author, description=package_description)

    menu = {
        'Edit Wallpapers': _edit_wallpapers,
        'Edit Color Schemes': _edit_colorschemes,
        'Configure Window Managers': _configure_wm,
        'Configure Programs': _configure_programs,
        'Save Package': _save_package,
        'Quit': _quit,
    }

    while True:
        clearConsole()
        print("----------------------------------------------------------------")
        print(f"Editing Package: {package_name} \n\n")
        for option in list(menu.keys()):
            print(f"[{list(menu.keys()).index(option)}] {option}")

        try:
            choice = int(input("\n: "))
        except ValueError:
            choice = -1
        

        if choice in list(range(0,len(menu.keys()))):
            list(menu.values())[choice](current_package)



def read_database():
    conn = sqlite3.connect(DB_DIR)
    c = conn.cursor()
    try:
        c.execute("SELECT * FROM packages")
        packages = c.fetchall()
    except sqlite3.DatabaseError:
        logger.error("Error Reading Database file. It may be corrupt, please try reinstalling phion")
    else:
        logger.info("Database is valid!")
        return packages


def list_packages():
    with alive_bar(2) as bar:
        bar.title = 'Checking Installation'
        if os.path.exists(DB_DIR):
            logger.info("Database file found")
            bar()
            packages = read_database()
            bar()
            for package in packages:
                print(f"Name: {package[0]}  Author: {package[1]}")

        else:
            logger.error("Database file not found.")


def main():

    parser = argparse.ArgumentParser(description='PHION Rice Package Manager Core Module')
    parser.add_argument('-v','--version', help='Version of PHION Core', action='store_true')
    parser.add_argument('-l', '--list', help='List all PHION Packages Loaded (.phkg', action='store_true')
    parser.add_argument('-w', '--packagewizard', help="Create a new Package Using PHION Package Wizard", action='store_true')
    args = vars(parser.parse_args())

    if args['version']:
        print(f"Phion Rice Package Manager CLI \n\nVersion: {version('phion')}\nhttps://github.com/phion-pm/core")
    if args['list']:
        list_packages()
    if args['packagewizard']:
        package_wizard()
    


if __name__ == "__main__":
    main()
    # conn = sqlite3.connect(DB_DIR)

    # c = conn.cursor()


    # c.execute("INSERT INTO packages VALUES ('myPackage1', 'Sortedcord')")

    # conn.commit()