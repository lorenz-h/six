import logging
import signal
import time
import multiprocessing as mp

from .module import start_module

class Spine:
    terminate = False
    
    def __init__(self):
        signal.signal(signal.SIGINT, self._shutdown_signal_handler)
        signal.signal(signal.SIGTERM, self._shutdown_signal_handler)

        self.logger = logging.getLogger("six.spine")

        self.mp_ctx = mp.get_context('spawn')
        self.modules = []
    
    def _shutdown_signal_handler(self, signum, frame):
        self.terminate = True
        self.logger.info("exit signal intercepted. spine will exit gracefully...")
    
    def _shutdown(self):
        self.logger.info("terminating children...")
        for module in self.modules:
            self.logger.info(f"sent SIGTERM to {module.name}")
            module.terminate()

    def loop(self):
        try:
            while not self.terminate:
                time.sleep(5)
                self.logger.info("still alive...")
        finally:
            self._shutdown()
    
    def add_module(self, module):
        mod_proc = self.mp_ctx.Process(target=start_module, args=(module, ))
        mod_proc.start()
        self.modules.append(mod_proc)
