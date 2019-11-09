import logging
import os
import signal
import subprocess
import time

from ..utils import setup_console_output

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
    terminate = False

    def __init__(self, name):
        self.name = name
        self.logger = logging.getLogger(f"six.modules.{name}")
    
    def loop(self):
        raise NotImplementedError("Module class is abstract")


class ExternalModule(Module):
    def __init__(self, name, cmd):
        logging.info(f"Creating ExternalModule {name}")
        super(ExternalModule, self).__init__(name)
        self.proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid) 

    def shutdown(self,signal_num, frame):
        self.terminate = True 
        self.proc.send_signal(signal.CTRL_BREAK_EVENT)
    
    def loop(self):
        while self.proc.poll is not None: 
            time.sleep(1)
            logging.info(f"module {self.name} is alive...")

    def __del__(self):
        try:
            os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
        except AttributeError:
            self.logger.warning("no process found under self.proc - most likely __init__ did not finish.")
        