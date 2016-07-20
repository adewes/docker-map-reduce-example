import os
import json
import gzip
import re
import collections

"""
Analysis script to run inside the Docker container.
"""

DATA_DIRECTORY = '/data'
OUTPUT_DIRECTORY = '/out'

def analyze_file(filename):
    word_frequencies = collections.defaultdict(lambda:0)
    with gzip.open(os.path.join(DATA_DIRECTORY,filename),'r') as input_file:
        for line in input_file:
            data = json.loads(line.decode('utf-8'))
            if data['type'] == 'PushEvent':
                for commit in data['payload']['commits']:
                    words = [word for word in re.compile('[^a-z\-\_]')\
                             .split(commit['message'].lower()) if word]
                    for word in words:
                        word_frequencies[word]+=1
    return word_frequencies

if __name__ == '__main__':
    print("Working directory: {}".format(os.getcwd()))
    input_filenames=os.environ['INPUT_FILENAMES'].split(';')
    for input_filename in input_filenames:
        print("Analyzing file: {}".format(input_filename))
        output_filename = input_filename[:-3]#we cut away the .gz
        print("Writing result to: {}".format(output_filename))
        result=analyze_file(input_filename)
        with open(os.path.join(OUTPUT_DIRECTORY,output_filename),'w') as output_file:
            output_file.write(json.dumps(result))
