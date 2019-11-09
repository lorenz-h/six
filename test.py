from modules.nlu import NLUModule

from utils import setup_console_output

if __name__ == "__main__":
    setup_console_output()
    nlu = NLUModule()
    nlu.loop()