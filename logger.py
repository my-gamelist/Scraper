import os
from datetime import date 

pwd = os.getcwd()

class Logger:
    def __init__(self):
        today = date.today()
        
        self.log_file = open(pwd + '/logs/log_%s.txt' %today,'a+')
        self.failed_file = open('failed_games.txt', 'w')

    # save any failed appids to a file
    def save_failed(self, content):
        self.failed_file.write(content + '\n')

    # save any new appids to a file
    def save_logs(self, appid):
        self.log_file.write(appid + '\n')
    
    def close_files(self):
        self.log_file.close()
        self.failed_file.close()
    