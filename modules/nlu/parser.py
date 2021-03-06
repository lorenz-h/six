import os
import json
import typing
import random 
import logging

from ...utils import projpath
NLTK_DIR = projpath("modules/nlu/resources/nltk_data")
NLTK_DIR.mkdir(exist_ok=True, parents=True)
os.environ["NLTK_DATA"] = str(NLTK_DIR)

import numpy as np
import nltk
import torch
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import LocalOutlierFactor

from .InferSent.models import InferSent
from .intent import Intent


def create_new_parser(training_data=projpath("resources/intents.json")):
    return Parser(training_data)

def load_pretrained_parser(fpath):
    pass

class Parser:
    def __init__(self, training_data):
        self.logger = logging.getLogger("six_core.module.nlu.intent_parser")
        self.logger.setLevel(logging.INFO)
        self.logger.info("initializing...")

        with open(training_data, "r", encoding="utf-8") as fp:
            train_data = json.load(fp)

        self.sanitizer = str.maketrans('', '', r"""!"#$%&'()*+,-./:;<=>?@\^_`{|}~""")
        self.intents = {intent_spec["name"]: Intent(intent_spec, self.sanitize) for intent_spec in train_data["intents"]}
        self.intent_names = sorted([intent_name for intent_name in self.intents])
        self.encoder = None
        self.init_encoder()

        self.classifier, self.outlier_detector = self.build_classifier()

    def init_encoder(self):
        if not NLTK_DIR.is_dir():
            self.logger.info("Downloading nltk data...")
            nltk.download("punkt", NLTK_DIR)
        version = 1
        model_path = projpath(f'modules/nlu/InferSent/encoder/infersent{version}.pkl')
        params_model = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048, 'pool_type': 'max', 'dpout_model': 0.0, 'version': version}
        self.encoder = InferSent(params_model)
        self.logger.info("Loading model...")
        self.encoder.load_state_dict(torch.load(model_path))
        w2v_path = projpath(f'modules/nlu/resources/GloVe/glove.840B.300d.txt')
        self.encoder.set_w2v_path(w2v_path)
        self.logger.info("Building vocab...")
        self.build_encoder_vocab()

    def get_samples(self):
        samples: list = []
        for intent in self.intents.values():
            samples += intent.samples
        return samples

    def build_encoder_vocab(self):
        self.encoder.build_vocab_k_words(K=3000)
        #self.encoder.update_vocab(self.get_samples())

    def deterministic_parse(self, statement) -> typing.Optional[Intent]:
        for intent in self.intents.values():
            if intent.regex.match(statement):
                self.logger.info(f"Deterministic match with intent {intent.name}")
                return intent
        self.logger.info("Deterministic parsing did not match any intent.")
        return None

    def probabilistic_parse(self, statement) -> typing.Optional[Intent]:
        embedding = self.encode_statement(statement)
        outlier: bool = self.outlier_detector.predict(embedding)[0] == -1
        if outlier:
            self.logger.info("Probabalistic Parse Detected Outlier!")
            return None
        else:
            intents_proba = self.classifier.predict_proba(embedding)
            intent_name = self.intent_names[np.argmax(intents_proba)]
            self.logger.info(f"Probabalistic Parse found Intent {intent_name} with confidence {np.max(intents_proba)}")
            return self.intents[intent_name]
        
    def parse(self, statement):
        clean_statement = self.sanitize(statement)
        determ_intent = self.deterministic_parse(clean_statement)
        if determ_intent is None:
            return self.probabilistic_parse(clean_statement)
        else:
            return determ_intent

    def sanitize(self, statement):
        clean_statement = statement.translate(self.sanitizer)
        self.logger.debug(f"sanitized <{statement}> to <{clean_statement}>")
        return clean_statement

    def encode_statement(self, statement):
        return self.encoder.encode([statement])
    
    def build_classifier(self):
        n_neighbors = 3
        knn = KNeighborsClassifier(n_neighbors=n_neighbors)
        outlier_detector = LocalOutlierFactor(n_neighbors=n_neighbors, novelty=True)
        
        train_samples = []
        for intent in self.intents.values():
            for sample in intent.samples:
                sample_vector = self.encode_statement(sample)
                train_samples.append((sample_vector, intent.name))

        random.shuffle(train_samples)
        train_features, train_labels = zip(*train_samples)

        np_train_feat = np.stack(train_features, 0)
        np_train_feat = np_train_feat.reshape([np_train_feat.shape[0], np_train_feat.shape[2]])
        np_train_labels = np.array(train_labels)

        self.logger.info("fitting knn and outlier model")
        knn.fit(np_train_feat, np_train_labels)
        outlier_detector.fit(np_train_feat, np_train_labels)
        self.logger.info("finished fitting knn and outlier model")
        return knn, outlier_detector
