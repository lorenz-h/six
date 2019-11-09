import logging
import os
import signal
import subprocess
import time

from utils import setup_console_output
from .heartbeat import HeartBeat

def start_module(mod_constructor):
    setup_console_output()
    try:
        module = mod_constructor()
    except Exception:
        logging.critical(f"Exeption occurred while creating module {mod_constructor}")
        raise
    try:
        module.loop()
    except Exception:
        logging.critical(f"Expeption occurred in {module.name} module")
        raise

class Module:

    name = "anonymous_module"
    terminate = False

    def __init__(self):
        self.logger = logging.getLogger(f"six.modules.{self.name}")
        self.hb = HeartBeat(self.name)
    
    def loop(self):
        raise NotImplementedError("Module class is abstract")


class ExternalModule(Module):

    name = "anonymous_ext_module"

    def __init__(self, cmd):
        logging.info(f"Creating ExternalModule {self.name}")
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
        