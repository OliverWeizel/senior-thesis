import re
import benepar
import pandas as pd
import nltk
import nltk.draw
from nltk.tree import Tree
from nltk.draw.tree import TreeView
import os
from IPython.display import display
# import spacy
from  icecream import ic
from scipy.stats import chisquare

sentence_enders = ["."] #, '?', '!', ':', ';']
# nlp = spacy.load('en_core_web_md')
# if spacy.__version__.startswith('2'):
#   nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
# else:
#   nlp.add_pipe("benepar", config={"model": "benepar_en3"})

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
  sentences = [[w for w in s if w not in { '\n', '<p>', '', ',' } and w != ''] for s in sentences]
  sentences = [s for s in sentences if '@' not in s]
  sentences = [s.lower() for s in sentences]

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

def pp(t):
  return str(t.flatten()).replace('\n', ' ').replace('   ', ' ')

def text(t):
  return ' '.join(t.leaves())

def test():
  parser = benepar.Parser("benepar_en3")
  ans = valid_sentences('COCA/text_academic_rpe/w_acad_1990.txt', english_processor, english_indicator) #[:5]
  #df = pd.DataFrame({"sentence":ans})
  tree_gen = parser.parse_sents([benepar.InputSentence(s) for s in ans])
  trees = []
  for t in tree_gen:
    trees.append(t)
  #ic(trees)
  #df['tree'] = trees

  #df = pd.DataFrame("tree":[], "conjunction":[], 'left':[], 'right':[])

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

  #df.head()
  # ic(ans[0])
  # ic(trees[0])
  # for t in trees:
  #   with open('trees/'+'test', 'w') as f:
  #     for tp in t.treepositions():
  #       if isinstance(t[tp], str):
  #         continue
  #       ic(t[tp])
  #       if t[tp].label() == 'CC':
  #         parent = t[tp[:-1]]
  #         f.write(pp(t[tp[:-1]]))
  #         for stp in parent.treepositions():
  #           f.write(str(parent[stp]))
  #           f.write('\n')
  #         f.write('\n')
  # #display(trees[0])
  #trees[0].pretty_print(unicodelines=True, nodedist=4)
  #TreeView(trees[0])._cframe.print_to_file('output.ps')
  #os.system('convert output.ps output.png')
  #ic(df['tree'][0])

if __name__ == '__main__':
  test()