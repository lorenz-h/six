
from utils import projpath
import os
NLTK_DIR = projpath("modules/nlu/resources/nltk_data")
os.environ["NLTK_DATA"] = str(NLTK_DIR)


from modules.nlu.InferSent.models import InferSent
import torch
import nltk

import time
from spine.module_skeletons import InternalModule

class NLUModule(InternalModule):

    name = "nlu"
    
    def __init__(self):
        #super(NLUModule, self).__init__()
        self.infersent = None
        self.init_infersent()

    def init_infersent(self):
        if not NLTK_DIR.is_dir():
            self.logger.info("Downloading nltk data...")
            nltk.download("punkt", NLTK_DIR)
        version = 1
        model_path = projpath(f'modules/nlu/InferSent/encoder/infersent{version}.pkl')
        params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048, 'pool_type': 'max', 'dpout_model': 0.0, 'version': version}
        self.infersent = InferSent(params_model)
        self.logger.info("Loading model...")
        self.infersent.load_state_dict(torch.load(model_path))
        w2v_path = projpath(f'modules/nlu/resources/GloVe/glove.840B.300d.txt')
        self.infersent.set_w2v_path(w2v_path)
        self.logger.info("Building vocab...")
        self.infersent.build_vocab_k_words(K=10000)
    
    def parse(self, statement):
        embedding = self.infersent.encode(statement, tokenize=True)
        self.logger.info(f"Parsing {statement}")

    def on_msg(self, topic: str, message: str):
        if topic.endswith("/nlu/parse"):
            self.parse(msg.decode("utf-8"))
