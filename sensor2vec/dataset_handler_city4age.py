# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 14:07:36 2016

@author: aitor
"""
from collections import Counter
import csv
import json

from gensim.models import Word2Vec
import numpy

#base directory
BASE_DIR = './user_67/'

# city4age dataset
DATASET_67 = BASE_DIR + 'user_67_actions_final.csv'
# List of unique actions in the dataset
UNIQUE_ACTIONS = BASE_DIR + 'unique_actions.json'
# Word2vec model generated with gensim
ACTIONS_MODEL = BASE_DIR + 'actions.model'
# Vector values for each action
ACTIONS_VECTORS = BASE_DIR + 'actions_vectors.json'
ACTION_TEXT = BASE_DIR + "actions.txt"
ACTION_TEXT_CSV = BASE_DIR + "actions.csv"


# When there is no activity
NONE = 'None'
# Separator for the text file
SEP = ' '
# Maximun number of actions in an activity
ACTIVITY_MAX_LENGHT = 32
# word2vec dimensions for an action
ACTION_MAX_LENGHT = 50

# period duration
PERIOD_DURATION = 30

DATASET = DATASET_67

DELIMITER = ','

# Generates the text file from the csv
def process_csv():
    actions = ''    
    actions_csv = ''    
    actions_set = set()
    with open(DATASET, 'rb') as csvfile: 
        print 'Processing:', DATASET
        reader = csv.reader(csvfile, delimiter=DELIMITER)  
        for row in reader:
            for element in row:
                print element
                action = element.replace('_', '')
                actions_csv += action + "\n"
                actions += action + SEP  
                actions_set.add(action)
    with open(ACTION_TEXT, 'w') as textfile: 
        textfile.write(actions)     
    with open(ACTION_TEXT_CSV, 'w') as textfile:
        textfile.write(actions_csv)
    json.dump(list(actions_set), open(UNIQUE_ACTIONS, 'w'))
    print 'Text file saved'


if __name__ == '__main__':
    print 'Start...'
    process_csv()


    print 'Fin'



            


