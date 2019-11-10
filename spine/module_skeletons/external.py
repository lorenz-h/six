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
        i = 0
        time.sleep(6)
        while self.proc.poll() is not None: 
            time.sleep(0.5)
            i += 1
            if i > 20:
                i = 0
                self.hb.ping()
        outs, errs = self.proc.communicate()
        self.logger.critical(f"External module {self.name} is exiting because its subprocess is dead with:\n stdout {outs.decode('utf-8')} \n stderr {errs.decode('utf-8')}...")

    def __del__(self):
        
        try:
            os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        except AttributeError:
            self.logger.warning("no process found under self.proc - most likely __init__ did not finish.")
        