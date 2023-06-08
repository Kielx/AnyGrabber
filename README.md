# <img src="./assets/AnyGrabberLogo.png" alt="Logo" width="60">  AnyGrabber

[![Tests](https://github.com/Kielx/AnyGrabber/actions/workflows/tests.yml/badge.svg)](https://github.com/Kielx/AnyGrabber/actions/workflows/tests.yml)

AnyGrabber simplifies the process of searching for AnyDesk logs, extracting relevant data concerning IP addresses used
for logging
in, along with corresponding dates. It also generates .txt and
.csv reports based on the data retrieved. The user-friendly interface and localization features make it easy for anyone
to use, regardless of technical proficiency. It's portable and can be used on any Windows machine without the need for
installation.

![App screenshot](./assets/README/screenshot1.png)

## Key Features:

- Search for logs in default and custom locations
- Extraction of login date and IP address/es
- Generation of checksums for retrieved files
- Creation of .txt and .csv reports based on found data
- Support for English and Polish languages
- User-friendly interface
- Portable

## Motivation

Extracting information from AnyDesk logs can be difficult and time-consuming, especially for people who aren't familiar
with where the logs are stored. It usually involves a lot of searching through irrelevant details to find important
information, such as dates and IP addresses. This can be so complicated that some people give up or spend a long time
trying to find what they need.

AnyGrabber is designed to make searching and finding AnyDesk logs easier for everyone. The app has an easy-to-use
interface that simplifies the process, making it accessible to both beginners and advanced users. It also offers
localization features, so people can use it in their native language.

## Tech used

- Python - https://www.python.org/
- Customtkinter -  https://github.com/TomSchimansky/CustomTkinter
- Pytest - https://docs.pytest.org/en/7.3.x/
- Auto-py-to-exe - https://pypi.org/project/auto-py-to-exe/

## Building

Easiest way to build portable version of app is to use [auto-py-to-exe](https://pypi.org/project/auto-py-to-exe/)  and
following the steps:

1. Run `auto-py-to-exe` from your command line
1. Choose `main.py` as script location
2. Change Console Window option to Window Based (hide the console)
3. Pick the icon that is located in `assets` folder
4. Pick and add additional files and directories from project root:
    - Assets folder
    - Locale folder
    - Customtkinter folder (`/venv/Lib/site-packages/customtkinter`)
    - Dateutil folder (`/venv/Lib/site-packages/dateutil`)
    - PIL folder (`/venv/Lib/site-packages/PIL`)
    - `config.json` file

Use the screenshot below for reference:

![py-to-exe](./assets/README/Auto-py-to-exe.png)

If you prefer to use pyinstaller command you need to swap locations of file to match your system.

**IMPORTANT**- If you are using PyCharm be sure to un-check the following options

![py-to-exe](./assets/README/Auto-py-to-exe2.png)
[Big thanks to this stackoverflow post](https://stackoverflow.com/questions/36618749/module-imports-work-in-pycharm-dont-work-in-python-idle/36618847#36618847):

**--- OR ---**

install dependencies globally via PIP

## Acknowledgments

- http://greenfishsoftware.org/gfie.php - Greenfish Icon Editor Pro was a great asset at creating icon for app
- https://figma.com - Figma for free design tools that I used for my logo
- https://photopea.com - Photopea being a great free image editor I used for my assets and images
- https://poedit.net/ - Poedit for making language translations a breeze


