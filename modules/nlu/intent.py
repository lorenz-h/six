from utils import projpath
import os
import json
import re
import typing
NLTK_DIR = projpath("modules/nlu/resources/nltk_data")
os.environ["NLTK_DATA"] = str(NLTK_DIR)

import torch

from modules.nlu.InferSent.models import InferSent


class Slot:
    def __init__(self, spec):
        self.name: str = spec["name"]
        self.parser: str = spec["parser"]
        self.required: bool = spec["required"]


class Intent:
    def __init__(self, spec: dict):
        self.test(spec)
        self.name = spec["name"]
        self.slots = [Slot(slot_spec) for slot_spec in spec["slots"]]
        self.templates = spec["templates"]

        self.regex = self.gen_regex()

    def gen_regex(self) -> re.Pattern:
        regex_strs = []
        for template in self.templates:
            for slot in self.slots:
                template_regex_str = template.replace(f"[{slot.name}]", "(.+)")
                regex_strs.append(template_regex_str)
        
        regex_str = '|'.join(regex_strs)
        return re.compile(regex_str, re.I)

    @staticmethod
    def test(spec):
        for key in ["name", "templates", "slots"]:
            try: 
                val = spec[key]
            except KeyError:
                raise KeyError(f"Intent Spec missing key <{key}>")
        assert isinstance(spec["templates"], list) and len(spec["templates"]) > 0, f"Intent {spec['name']} has no templates"


class Parser:
    def __init__(self):
        with open(projpath("resources/intents.json"), "r") as fp:
            train_data = json.load(fp)
        self.intents = [Intent(intent_spec) for intent_spec in train_data["intents"]]

        self.encoder = None
        self.init_encoder()
    
    def init_encoder(self):
        if not NLTK_DIR.is_dir():
            print.info("Downloading nltk data...")
            nltk.download("punkt", NLTK_DIR)
        version = 1
        model_path = projpath(f'modules/nlu/InferSent/encoder/infersent{version}.pkl')
        params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048, 'pool_type': 'max', 'dpout_model': 0.0, 'version': version}
        self.encoder = InferSent(params_model)
        print("Loading model...")
        self.encoder.load_state_dict(torch.load(model_path))
        w2v_path = projpath(f'modules/nlu/InferSent/GloVe/glove.840B.300d.txt')
        self.encoder.set_w2v_path(w2v_path)
        print("Building vocab...")
        self.encoder.build_vocab_k_words(K=10000)
    
    def deterministic_parse(self, sentence) -> typing.Optional[Intent]:
        for it in self.intents:
            if it.regex.match(sentence):
                print(f"Matched intent {it.name}")
                return it
        return None

    def probabilistic_parse(self, statement) -> typing.Optional[Intent]:
        embedding = self.encoder.encode(statement, tokenize=True)
        print(f"Parsing <{statement}>")
        
