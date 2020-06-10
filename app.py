import rumps


class MacStatsApp(object):
    def __init__(self):
        self.config = {
            "app_name": "macStats",
            "wifi": "wifiStats",
            "disk": "diskStats",
            "system": "systemStats"
        }
        self.app = rumps.App(self.config["app_name"])
        self.wifi = rumps.MenuItem(title=self.config["wifi"])
        self.app.menu = [self.wifi]

    def run(self):
        self.app.run()


if __name__ == '__main__':
    app = MacStatsApp()
    app.run()
