import rumps
import netifaces as ni
import subprocess
import json
import platform
import psutil
import socket

# Uncomment line below to have debugging print-statements while the app is running
# rumps.debug_mode(True)

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
MEMORY_TOTAL = rumps.MenuItem("Total:\t-")
MEMORY_USED = rumps.MenuItem("Used:\t-")
CPU_PERCENTAGE = rumps.MenuItem("CPU%:\t-")
BATTERY_CHARGE = rumps.MenuItem("Charge:\t-")
BATTERY_HEALTH = rumps.MenuItem("Health:\t-")
BATTERY_CYCLES = rumps.MenuItem("Cycles:\t-")


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


def round_space(disk_space):
    # round_disk_space converts a string to a number, rounds it
    # with a precision of two after the decimal point
    disk_space_num = float(disk_space)
    return str(round(disk_space_num, 2))


def get_battery_data():
    # collects all available data regarding the AppleSmartBattery, constructs
    # a json-object from it and returnes said object
    battery_info_obj = {}

    ioreg = subprocess.Popen(
        ['ioreg', '-c', 'AppleSmartBattery'], stdout=subprocess.PIPE)
    grep = subprocess.Popen(['grep', '-i', 'capacity'],
                            stdin=ioreg.stdout, stdout=subprocess.PIPE)
    end_of_pipe = grep.stdout

    for line in end_of_pipe:
        ln = line.strip().decode('utf8')
        key = ln[ln.find('\"')+1:ln.find('\" =')]
        val = ln[ln.find('\" = ') + 4:]
        battery_info_obj[key] = val

    json_obj = json.dumps(battery_info_obj)
    jsn = json.loads(json_obj)
    return jsn


def find_substr(start, end, s):
    # finds a substring between strings 'start' and 'end'
    tmp = s[s.find(start):]
    return tmp[len(start):tmp.find(end)]


def construct_battery_obj(json_data):
    # constructs and returns the following json-object from json_data:
    # {'MaxCapacity': 'x', 'CurrentCapacity': 'x', 'StateOfCharge': 'x', 'CycleCount': 'x'}
    data = {}
    battery_data = json_data['BatteryData']
    state_of_charge = find_substr("StateOfCharge\"=", ",", battery_data)
    cycle_count = find_substr("CycleCount\"=", ",", battery_data)

    data['MaxCapacity'] = json_data['MaxCapacity']
    data['CurrentCapacity'] = json_data['CurrentCapacity']
    data['StateOfCharge'] = state_of_charge
    data['CycleCount'] = cycle_count

    json_data = json.dumps(data)
    jsn = json.loads(json_data)
    return jsn


@rumps.timer(2)
def gather_data(sender):
    # gather_data updates all the fields of the app
    # rumps.timer open a new thread and triggers gather_data every two senconds
    battery_data = construct_battery_obj(get_battery_data())

    global MACOS_VERSION, CONNECTED, SSID, MAC_ADDR, IP_ADDR, DISK_TOTAL, DISK_FREE, MEMORY_TOTAL, MEMORY_USED, CPU_PERCENTAGE
    connection = is_connected()
    if connection:
        APP.icon = "../resources/app_icon_green.png"
        SSID.title = f"SSID:\t{cut_ssid_string(subprocess.check_output([MAC_AIRPORT_PATH, '-I']).decode('utf8').splitlines(True))}"
        IP_ADDR.title = f"IP:\t\t{ni.ifaddresses('en0')[ni.AF_INET][0]['addr']}"
    else:
        APP.icon = "../resources/app_icon_red.png"
        SSID.title = f"SSID:\t-"
        IP_ADDR.title = f"IP:\t\t-"
    DISK_TOTAL.title = f"Total:\t{round_space(psutil.disk_usage('/').total / (1000.0 ** 3))} GB"
    DISK_FREE.title = f"Free:\t{round_space(psutil.disk_usage('/').free / (1000.0 ** 3))} GB"
    MEMORY_TOTAL.title = f"Total:\t{round_space(psutil.virtual_memory()[0] / (1024.0 ** 3))} GB"
    MEMORY_USED.title = f"Used:\t{round_space(psutil.virtual_memory()[3] / (1024.0 ** 3))} GB"
    MACOS_VERSION.title = f"macOS:\t{platform.mac_ver()[0]}"
    MAC_ADDR.title = f"MAC:\t{ni.ifaddresses('en0')[ni.AF_LINK][0]['addr']}"
    CPU_PERCENTAGE.title = f"Load:\t{psutil.cpu_percent()} %"
    BATTERY_CHARGE.title = f"Charge:\t{battery_data['StateOfCharge']} %"
    BATTERY_HEALTH.title = f"Health:\t{round(float(battery_data['CurrentCapacity']) / (float(battery_data['MaxCapacity']) / 100), 2)} %"
    BATTERY_CYCLES.title = f"Cycles:\t{battery_data['CycleCount']}"


def main_func():
    # -- MAIN --
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
        None,
        "Memory",
        MEMORY_TOTAL,
        MEMORY_USED,
        None,
        "CPU",
        CPU_PERCENTAGE,
        None,
        "Battery",
        BATTERY_CHARGE,
        BATTERY_HEALTH,
        BATTERY_CYCLES,
        None
    ]
    APP.run()


if __name__ == "__main__":
    main_func()
