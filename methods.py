import re
import benepar
import pandas as pd
import nltk
import nltk.draw
from nltk.tree import Tree
from nltk.draw.tree import TreeView
from nltk.stem import WordNetLemmatizer as wln
import os
from IPython.display import display
# import spacy
from  icecream import ic
from scipy.stats import chisquare

nltk.download('wordnet')

sentence_enders = [".", '?', '!', ':', ';']

# takes in an array of english words and returns true if one of a 
# set of words is present
def english_indicator(text, options=['but']):
  for w in text:
    if w in options:
      return True
  return True

# takes in a line of english text, splits the line into paragraphs
# returns a line splinto sentences as an array of array of strings
# if containing all alphanumeric characters, or if a specified
# other condition is met
def english_processor(text, specific_processor=None):
  res = []

  #https://stackoverflow.com/questions/25735644/python-regex-for-splitting-text-into-sentences-sentence-tokenizing
  sentences = re.split(r'(?<!\w\.\w.)(?<!\b[A-Z][a-z]\.)(?<![A-Z]\.)(?<=\.|\?)\s|\\n', text)

  sentences = [s.split(' ') for s in sentences]


  sentences = [[w.lower() for w in s if w not in { '\n', '<p>', '', ',', '.', '\"', '\'', '?', '!', ':', ';'}] for s in sentences]

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
    if '-' in joined:
      continue
    res.append(s)
  return res

def new_processor(text, specific_processor=None):
  res = nltk.sent_tokenize(text)
  ic(res)
  return res


# takens in the path to a .txt file, a function that takes in a 
# line containing multiple sentences and returns array of array
# of words in sentences, and a function that return true iff a 
# sentence is valid
def valid_sentences(textpath, processor, indicator):
  res = []
  i = 0
  with open(textpath, 'r') as f:
    for line in f:
      #print(line)
      sentences = [s for s in processor(line) if indicator(s)]
      res = res + sentences
  return res

def pp(t):
  return str(t.flatten()).replace('\n', ' ').replace('   ', ' ')

def text(t):
  return ' '.join(t.leaves())

def conjoin(a, b, left):
  if left:
    return Tree.fromstring(b.label() + ' (' + text(a) + ' ' + text(b) + ')')
  else:
    return Tree.fromstring(a.label() + ' (' + text(a) + ' ' + text(b) + ')')
  
def lowest_pos(t):
  return [s for s in t.subtrees(lambda t: t.height() == 2)]

def lowest_leaves(t):
  return [t[s] for s in t.subtrees(lambda t: t.height() == 2)]

#returns if corrective, anchored (verb negated)
def find_s(t, pos0):
  sentential_tags = {'S', 'SBAR', 'SINV', 'SBARQ', 'SQ'}
  negators = {'not', 'n\'t'}
  verb_tags = {'VBD', 'VBG', 'VBN', 'VBP', 'VBZ'}
  tensed = {'have', 'do', 'will', 'would', 'can', 'could', 'may', 'might', 'should', 'ought', 'must', 'shall', 'be'}

  try:
    while t[pos].label() not in sentential_tags:
      pos = pos[:-1]
  except:
    return (False, False)
  poses = lowest_pos(t)
  i = None
  for k in range(poses.index(pos0)):
    if text(t[poses[k]]) in negators:
      i = k
      break
  if i == None:
    return (False, False)
  try:
    if t[poses[i-1]].label() in verb_tags and wln().lemmatize(text(t[poses[i-1]]),pos='v') in tensed:
      return (True, True)
    return (True, False)
  except:
    return (False, False)

def test():
  parser = benepar.Parser("benepar_en3")
  ans = valid_sentences('demo.txt', english_processor, english_indicator)
  ic(ans)
  df = pd.DataFrame({"sentence":ans})
  print("OK")
  tree_gen = parser.parse_sents([benepar.InputSentence(s) for s in ans])
  trees = []
  for t in tree_gen:
   trees.append(t)
  #ic(trees)
  # df['tree'] = trees

  # df = pd.DataFrame("tree":[], "conjunction":[], 'left':[], 'right':[])

  parent_tree = []
  parent_text = []
  parent_type = []
  left_tree = []
  left_text = []
  left_type = []
  cc_tree = []
  cc_text = []
  right_tree = []
  right_text = []
  right_type = []
  

  for t in trees:
    ic('full: '+ pp(t))
    for tp in t.treepositions():
      if isinstance(t[tp], str):
        continue
      if t[tp].label() == 'CC':
        parent = t[tp[:-1]]
        relative_tp = tp[-1]
        # ic(relative_tp)
        # ic(parent.treepositions())
        if relative_tp + 1 >= len(parent.treepositions()):
          print("bad conjunction!")
          continue
        ic('parent: ' + pp(parent))
        left = parent[0]
        ic('left: ' + pp(left))
        conj = parent[relative_tp]
        ic('conj: ' + pp(conj))
        ic('conjunction: ' + ' '.join(conj.leaves()))
        right = parent[relative_tp + 1]
        ic('right: ' + pp(right))
        parent_tree.append(parent)
        parent_text.append(text(parent))
        parent_type.append(parent.label())
        left_tree.append(left)
        left_text.append(text(left))
        left_type.append(left.label())
        right_tree.append(right)
        right_text.append(text(right))
        right_type.append(right.label())
        cc_tree.append(conj)
        cc_text.append(text(conj))

  df = pd.DataFrame({'parent_tree':parent_tree, 'parent_text':parent_text, 'parent_type':parent_type, 'left_tree':left_tree, 'left_text':left_text, 'left_type':left_type, 'right_tree':right_tree, 'right_text':right_text, 'right_type':right_type, 'cc_tree':cc_tree, 'cc_text':cc_text})
  df['same_type'] = df.apply(lambda row: row['left_type'] == row['right_type'], axis=1)
  print(df['cc_text'].value_counts())
  res = chisquare(df['cc_text'].value_counts())
  print(res)
  print(df.head())

  # #df.head()
  # # ic(ans[0])
  # # ic(trees[0])
  # # for t in trees:
  # #   with open('trees/'+'test', 'w') as f:
  # #     for tp in t.treepositions():
  # #       if isinstance(t[tp], str):
  # #         continue
  # #       ic(t[tp])
  # #       if t[tp].label() == 'CC':
  # #         parent = t[tp[:-1]]
  # #         f.write(pp(t[tp[:-1]]))
  # #         for stp in parent.treepositions():
  # #           f.write(str(parent[stp]))
  # #           f.write('\n')
  # #         f.write('\n')
  # # #display(trees[0])
  # #trees[0].pretty_print(unicodelines=True, nodedist=4)
  # #TreeView(trees[0])._cframe.print_to_file('output.ps')
  # #os.system('convert output.ps output.png')
  # #ic(df['tree'][0])

if __name__ == '__main__':
  test()