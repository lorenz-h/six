import logging
import os
import signal
import time
import subprocess

from .module import Module

class ExternalModule(Module):

    name = "anonymous_ext_module"

    def __init__(self, cmd):
        super(ExternalModule, self).__init__()
        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 

    def shutdown(self,signal_num, frame):
        self.terminate = True 
        self.proc.send_signal(signal.CTRL_BREAK_EVENT)
    
    def loop(self):
        while self.proc.poll is not None: 
            time.sleep(3)
            self.hb.ping()

    def __del__(self):
        try:
            os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        except AttributeError:
            self.logger.warning("no process found under self.proc - most likely __init__ did not finish.")
        