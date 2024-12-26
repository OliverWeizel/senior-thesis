import re

sentence_enders = [".", '?', '!', ':', ';']

def english_indicator(text, options):
  for w in text:
    if w in options:
      return True
  return False

def english_processor(text, specific_processor=None):
  res = []
  sentences = text
  for e in sentence_enders:
    sentences = sentences.split(' '+e+' ')
  if specific_processor:
    res = specific_processor(sentences)
  else:
    res = [s for s in sentences if all(re.match('^[\w-]+$', w) for w in s)]
  return res
  #for s in sentences:
  #  if all(re.match('^[\w-]+$', w) for w in s):
  #    res.append(s)


def valid_sentences(textpath, processor, indicator):
  res = []
  with open(textpath, 'r') as f:
    for line in f:
      sentences = [s for s in processor(line) if indicator(s)]
      res = res + sentences
  return res

