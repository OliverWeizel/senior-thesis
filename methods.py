import re
from  icecream import ic

sentence_enders = ["."] #, '?', '!', ':', ';']

# takes in an array of english words and returns true if one of a 
# set of words is present
def english_indicator(text, options=['but']):
  for w in text:
    if w in options:
      return True
  return False

# takes in a line of english text, splits the line into paragraphs
# returns a line splinto sentences as an array of array of strings
# if containing all alphanumeric characters, or if a specified
# other condition is met
def english_processor(text, specific_processor=None):
  #print("HEllllllLLO")
  res = []
  #sentences = re.split(' ' + ' | '.join(sentence_enders) + ' ', text)
  sentences = text.split(' . ')
  sentences = [s.split(' ') for s in sentences]
  sentences = [[w for w in s if w not in { '\n', '<p>', '' } and w != ''] for s in sentences]
  sentences = [s for s in sentences if '@' not in s]
  sentences = [s for s in sentences]

  for s in sentences:
    if not s:
      continue
    if '@' in s:
      continue
    joined = ''.join(s)
    if '#' in joined:
      continue
    if ':' in joined:
      continue
    if ';' in joined:
      continue

    res.append(s)
  #print([r[:3] for r in res])
  # for e in sentence_enders:
  #   print(e)
  #   sentences = [s.split(' '+e+' ') for s in sentences]
  # if specific_processor:
  #   res = specific_processor(sentences)
  #else:
  #  res = [s for s in sentences if all(re.match(r'^[\w-]+$', w) for w in s.split(' '))]
  return res

# takens in the path to a .txt file, a function that takes in a 
# line containing multiple sentences and returns array of array
# of words in sentences, and a function that return true iff a 
# sentence is valid
def valid_sentences(textpath, processor, indicator):
  print("NEW8")
  res = []
  i = 0
  with open(textpath, 'r') as f:
    for line in f:
      #print(line)
      sentences = [s for s in processor(line) if indicator(s)]
      res = res + sentences
  return res

def test():
  ans = valid_sentences('COCA/text_academic_rpe/w_acad_1990.txt', english_processor, english_indicator)
  ic(ans)

if __name__ == '__main__':
  test()