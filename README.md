# macStats

<img src="resources/app_icon.png" alt="logo" width="100" height="100">

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/McMuellermilch/macStats/blob/master/LICENSE)

A simple macOS menu bar app, that displays all the relevant info about your Mac - built on top of [rumps](https://github.com/jaredks/rumps)

## Getting started

### Screenshots

<img src="resources/screenshot_online.png" alt="screenshot_online" height="350"> <img src="resources/screenshot_offline.png" alt="screenshot_offline" height="350">
<br/>

### Installing

macStats can be downloaded as a bundled .app file. [Here](https://github.com/McMuellermilch/macStats/releases) you can download the zipped file.

After downloading and unzipping, just copy macStats.app into your Applications folder.

To have macStats automatically start at startup, just head over to `Settings -> Users & Groups -> Login Terms`, click the `+` and select macStats.

### Development

#### Prerequisites

macStats only runs on `macOS`. Furthermore, you need an installation of `Python3` on your machine.

#### Dependencies

Packagemanagement for this project has been done with [pipenv](https://github.com/pypa/pipenv). With pipenv installed, you only have to run `pipenv install` to install all dependencies from the `Pipfile`. To start up the virtual environment, just run `pipenv shell`.

Without pipenv, install the dependencies as follows:

```python
pip install rumps py2app netifaces psutil
```

#### Building the app

At root level of the project directory, you can build the app with the following command:

```python
python3 setup.py py2app
```

This will create two new folders in the directory: `build` and `dist`. The bundled application can be found in `./dist/macStats.app`.

After building, you can start macStats by running:

```python
./dist/macStats.app/Contents/MacOS/macStats
```

## Usage

The idea behind macStats is to bundle all the necessary info about your Mac in one place and with that, replacing an abundance of terminal commands, settings pages and other apps. It's mainly for displaying information, so there's not much interactivity to it.

As an easy to see indicator for network connectivity, the logo in the app bar will change colors depending on the network connection status.

<img src="resources/logo_colorchange.gif" alt="screencast_colorchange">

The only button - `Copy stats to clipboard` - will copy a string to your clipboard, that contains the following data:

```
Model: -
Processor: -
macOS: -
MAC-address: -
RAM: -GB
Internet-connection: True/False

```

This button is meant to make aksing questions online about your Mac easier. When searching for a solution to a certain problem, it is of utmost importance to give all the relevant information and context for people to be able to solve your problem. Well, the info about your hardware is taken care of.
