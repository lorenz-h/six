import re
import random
import copy
import logging
import json


class Slot:
    def __init__(self, spec):
        self.name: str = spec["name"]
        self.parser_type: str = spec["parser_type"]
        self.required: bool = spec["required"]

    def get_random_value(self):
        if self.parser_type == "Room":
            return random.choice(["kitchen", "bedroom", "bathroom", "living room"])
        elif self.parser_type == "Temperature":
            raw_val = (random.random()*40)+5.0
            return round(raw_val, 1)
        else:
            raise ValueError(f"Invalid parser type {self.parser_type}")
    
    def __iter__(self):
        yield "name", self.name
        yield "parser_type", self.parser_type
    

class Intent:
    def __init__(self, spec: dict, sanitize_fn):
        self.logger = logging.getLogger("six_core.module.nlu.intent")
        self.test(spec)
        self.name = spec["name"]
        self.slots = [Slot(slot_spec) for slot_spec in spec["slots"]]
        self.templates = [sanitize_fn(template) for template in spec["templates"]]
        self.samples = self.gen_samples()
        self.regex = self.gen_regex()

    def gen_regex(self) -> re.Pattern:
        regex_strs = []
        for template in self.templates:
            for slot in self.slots:
                template_regex_str = template.replace(f"[{slot.name}]", "(.+)")
                regex_strs.append(template_regex_str)
        
        regex_str = '|'.join(regex_strs)
        return re.compile(regex_str, re.I)

    def __str__(self):
        return json.dumps({"name":self.name, "slots":[dict(slot) for slot in self.slots]})

    def gen_samples(self) -> list:
        samples = []
        for template in self.templates:
            for i in range(2):
                sample = copy.copy(template)
                for slot in self.slots:
                    sample = sample.replace(f"[{slot.name}]", str(slot.get_random_value()))

                self.logger.debug(f"created sample <{sample}>")
                samples.append(sample)
        return samples

    @staticmethod
    def test(spec):
        for key in ["name", "templates", "slots"]:
            try: 
                val = spec[key]
            except KeyError:
                raise KeyError(f"Intent Spec missing key <{key}>")
        assert isinstance(spec["templates"], list) and len(spec["templates"]) > 0, f"Intent {spec['name']} has no templates"

