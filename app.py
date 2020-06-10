import rumps
import netifaces as ni
import subprocess
import json

MAC_AIRPORT_PATH = "/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport"

# cut_ssid_string takes a string of data, finds the 'SSID: ' section and cuts out the ssid as a string
def cut_ssid_string(data):
    ssid_string = ""
    for d in data:
        if ' SSID:' in d:
            s = d
            s_tmp = s[s.find('SSID'):s.find('\n')]
            ssid_string = s_tmp[s_tmp.find(' ') +1 : ]
    return ssid_string

# Variables to be displayed in the menu bar app
SSID = cut_ssid_string(subprocess.check_output([MAC_AIRPORT_PATH, '-I']).decode('utf8').splitlines(True))
MAC_ADDR = ni.ifaddresses('en0')[ni.AF_LINK][0]['addr']
IP_ADDR = ni.ifaddresses('en0')[ni.AF_INET][0]['addr']

class MacStatsApp(rumps.App):
    def __init__(self):
        super(MacStatsApp, self).__init__("macStats")
        self.icon = "AppLogo.png"
        self.menu = [
            rumps.MenuItem(f"IP:\t\t{IP_ADDR}"),
            rumps.MenuItem(f"MAC:\t{MAC_ADDR}"),
            rumps.MenuItem(f"SSID:\t{SSID}"), 
            None
        ]
        

if __name__ == "__main__":
    MacStatsApp().run()