import logging
import signal
import time
import multiprocessing as mp

from .module_skeletons import start_module
from .heartbeat import HeartBeat
from ..utils import setup_console_output, check_platform_compatibility

class Spine:
    terminate = False
    
    def __init__(self, strict = True):
        signal.signal(signal.SIGINT, self._shutdown_signal_handler)
        signal.signal(signal.SIGTERM, self._shutdown_signal_handler)

        check_platform_compatibility()
        setup_console_output()

        self.strict: bool = strict

        self.hb = HeartBeat("spine")
        self.logger = logging.getLogger("six.spine")

        self.mp_ctx = mp.get_context('spawn')
        self.modules: list = []
    
    def _shutdown_signal_handler(self, signum, frame):
        self.terminate = True
        self.logger.info("exit signal intercepted. spine will exit gracefully...")
    
    def _shutdown(self):
        logging.info("terminating children...")
        for module in self.modules:
            logging.info(f"sent SIGTERM to {module.name}")
            module.terminate()

    def poll_modules(self):
        if not all([module.is_alive() for module in self.modules]):
            self.logger.critical("Found dead children. Spine will exit...")
            self.terminate = True
        else:
            self.logger.info("all children are alive.")

    def loop(self):
        try:
            i = 0
            while not self.terminate:
                time.sleep(0.5)
                i += 1
                if i > 20:
                    i = 0
                    if self.strict:
                        self.poll_modules()
                    self.hb.ping()
        finally:
            self._shutdown()
    
    def add_module(self, module):
        mod_proc = self.mp_ctx.Process(target=start_module, args=(module, ), name=f"{module.name}_proc")
        mod_proc.start()
        self.modules.append(mod_proc)
