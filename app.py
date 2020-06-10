import rumps

class MacStatsApp(rumps.App):
    def __init__(self):
        super(MacStatsApp, self).__init__("macStats")
        self.menu = ["Wifi", None, "System", None]
        self.icon = "AppLogo2.png"

if __name__ == "__main__":
    MacStatsApp().run()