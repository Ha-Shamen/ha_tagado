import os
import threading, time, signal
from datetime import timedelta
from data_collector import get_data
from mongo_service import MongoService


WAIT_TIME_SECONDS = os.environ.get("WAIT_TIME_SECONDS") or 60

class ProgramKilled(Exception):
    pass

    
def signal_handler(signum, frame):
    raise ProgramKilled
    
class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs
        self.mongo_service = MongoService()
        self.get_users = True
        
    def stop(self):
            self.stopped.set()
            self.join()
    def run(self):
            while not self.stopped.wait(self.interval.total_seconds()):
                self.execute(self.get_users, *self.args, **self.kwargs)
                self.get_users = False
            
if __name__ == "__main__":
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    job = Job(interval=timedelta(seconds=WAIT_TIME_SECONDS), execute=get_data)
    job.start()
    
    while True:
          try:
              time.sleep(1)
          except ProgramKilled:
              print ("Program killed: running cleanup code")
              job.stop()
              break