import logging
import os
import signal
import time

from ...utils import setup_console_output
from ..heartbeat import HeartBeat

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
