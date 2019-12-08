from modules.nlu.intent import Parser

if __name__ == "__main__":
    ps = Parser()
    intent = ps.probabilistic_parse("turn the lights off")