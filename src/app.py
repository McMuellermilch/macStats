import rumps
import netifaces as ni
import subprocess
import json
import platform
import psutil
import socket

# Global variables
MAC_AIRPORT_PATH = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
APP = rumps.App("macStats")
MACOS_VERSION = rumps.MenuItem("macOS:\t-")
WIFI = rumps.MenuItem("Wifi:")
SSID = rumps.MenuItem("SSID:\t-")
MAC_ADDR = rumps.MenuItem("MAC:\t-")
IP_ADDR = rumps.MenuItem("IP:\t-")
DISK_TOTAL = rumps.MenuItem("Total:\t-")
DISK_FREE = rumps.MenuItem("Free:\t-")


def is_connected():
    # is_connected tests the internet connection and returns true if connected
    try:
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False


def cut_ssid_string(data):
    # cut_ssid_string takes a string of data, finds the 'SSID: ' section and cuts out the ssid as a string
    ssid_string = ""
    for d in data:
        if ' SSID:' in d:
            s = d
            s_tmp = s[s.find('SSID'):s.find('\n')]
            ssid_string = s_tmp[s_tmp.find(' ') + 1:]
    return ssid_string


def round_disk_space(disk_space):
    # round_disk_space converts a string to a number, rounds it
    # with a precision of two after the decimal point
    disk_space_num = float(disk_space)
    return str(round(disk_space_num, 2))


@rumps.timer(2)
def gather_data(sender):
    # gather_data updates all the fields of the app
    # rumps.timer open a new thread and triggers gather_data every two senconds
    global MACOS_VERSION, CONNECTED, SSID, MAC_ADDR, IP_ADDR, DISK_TOTAL, DISK_FREE, TIME
    connection = is_connected()
    if connection:
        APP.icon = "../resources/app_icon_green.png"
        SSID.title = f"SSID:\t{cut_ssid_string(subprocess.check_output([MAC_AIRPORT_PATH, '-I']).decode('utf8').splitlines(True))}"
        IP_ADDR.title = f"IP:\t\t{ni.ifaddresses('en0')[ni.AF_INET][0]['addr']}"
    else:
        APP.icon = "../resources/app_icon_red.png"
        SSID.title = f"SSID:\t-"
        IP_ADDR.title = f"IP:\t\t-"
    DISK_TOTAL.title = f"Total:\t{round_disk_space(psutil.disk_usage('/').total / (1000.0 ** 3))} GB"
    DISK_FREE.title = f"Free:\t{round_disk_space(psutil.disk_usage('/').free / (1000.0 ** 3))} GB"
    MACOS_VERSION.title = f"macOS:\t{platform.mac_ver()[0]}"
    MAC_ADDR.title = f"MAC:\t{ni.ifaddresses('en0')[ni.AF_LINK][0]['addr']}"


if __name__ == "__main__":
    #print(psutil.virtual_memory()[0] / (1000.0 ** 3))
    APP.icon = "../resources/app_icon_white.png"
    APP.menu = [
        "System",
        MACOS_VERSION,
        MAC_ADDR,
        None,
        WIFI,
        IP_ADDR,
        SSID,
        None,
        "Disk",
        DISK_TOTAL,
        DISK_FREE,
        None
    ]
    APP.run()
