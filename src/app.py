import rumps
import netifaces as ni
import subprocess
import json
import platform
import psutil
import socket
import time
import datetime

# Variables to be displayed in the menu bar app
MAC_AIRPORT_PATH = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"
MACOS_VERSION = rumps.MenuItem("macOS:\t-")
CONNECTED = rumps.MenuItem("Connected:\t-")
SSID = rumps.MenuItem("SSID:\t-")
MAC_ADDR = rumps.MenuItem("MAC:\t-")
IP_ADDR = rumps.MenuItem("IP:\t-")
DISK_TOTAL = rumps.MenuItem("Total:\t-")
DISK_FREE = rumps.MenuItem("Free:\t-")

def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

@rumps.timer(2)
def gather_data(sender):
    global MACOS_VERSION, CONNECTED, SSID, MAC_ADDR, IP_ADDR, DISK_TOTAL, DISK_FREE, TIME
    connection = is_connected()
    if connection:
        CONNECTED.title = f"Connected: {True}"
        SSID.title = f"SSID:\t{cut_ssid_string(subprocess.check_output([MAC_AIRPORT_PATH, '-I']).decode('utf8').splitlines(True))}"
        IP_ADDR.title = f"IP:\t\t{ni.ifaddresses('en0')[ni.AF_INET][0]['addr']}"
    else:
        CONNECTED.title = f"Connected: {False}"
        SSID.title = f"SSID:\t-"
        IP_ADDR.title = f"IP:\t\t-"
    DISK_TOTAL.title = f"Total:\t{psutil.disk_usage('/').total / (1000.0 ** 3)}"
    DISK_FREE.title = f"Free:\t{psutil.disk_usage('/').free / (1000.0 ** 3)}"
    MACOS_VERSION.title = f"macOS:\t{platform.mac_ver()[0]}"
    MAC_ADDR.title = f"MAC:\t{ni.ifaddresses('en0')[ni.AF_LINK][0]['addr']}"


    
# cut_ssid_string takes a string of data, finds the 'SSID: ' section and cuts out the ssid as a string
def cut_ssid_string(data):
    ssid_string = ""
    for d in data:
        if ' SSID:' in d:
            s = d
            s_tmp = s[s.find('SSID'):s.find('\n')]
            ssid_string = s_tmp[s_tmp.find(' ') +1 : ]
    return ssid_string
        
if __name__ == "__main__":
    app = rumps.App("macStats")
    app.icon = "../resources/AppLogo.png"
    app.menu = [
        "System",
        MACOS_VERSION,
        None,
        "Wifi",
        CONNECTED,
        IP_ADDR,
        SSID, 
        MAC_ADDR,
        None,
        "Disk",
        DISK_TOTAL,
        DISK_FREE,
        None
    ]
    app.run()