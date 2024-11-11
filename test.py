import numpy as np
from nltk.corpus import wordnet as wn
import benepar
import spacy
import warnings
import os
import logging
import sys
# test

LOGGER = logging.getLogger(__name__)
HANDLER = logging.StreamHandler(sys.stdout)
HANDLER.setFormatter(logging.Formatter("%(asctime)-s.%(msecs)03d %(levelname)-6.6s %(filename)-18.18s line:%(lineno)-4.4d %(funcName)-18s %(message)s"))
LOGGER.addHandler(HANDLER)

LOGGER.error("Here we go!")
#os.environ['TRANSFORMERS_NO_ADVISORY_WARNINGS'] = 'true'
#warnings.filterwarnings("ignore", category=DeprecationWarning) 
#warnings.filterwarnings("ignore", category=UserWarning)
#warnings.simplefilter("ignore")
def _label(span):
    return span._.labels or (span[0].tag_,)
nlp = spacy.load('en_core_web_md')
if spacy.__version__.startswith('2'):
  nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
else:
  nlp.add_pipe("benepar", config={"model": "benepar_en3"})
doc = nlp("The time for action is now. It's never too late to do something.")
sent = list(doc.sents)[0]
print(sent._.parse_string)
doc = nlp("I am bored. Who am I? I am tired!")
sent = list(doc.sents)[0]
print(sent._.parse_string)
