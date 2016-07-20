import os
import json
import gzip
import re
import collections

"""
"Classical" analysis script.
"""

data_directory = 'data'

def get_files(directory):
    filenames = os.listdir(directory)
    return sorted([os.path.join(directory,filename)
                   for filename in filenames if filename.endswith('.json.gz')])


def analyze_file(filename):
    word_frequencies = collections.defaultdict(lambda:0)
    with gzip.open(filename,'r') as input_file:
        for line in input_file:
            data = json.loads(line.decode('utf-8'))
            if data['type'] == 'PushEvent':
                for commit in data['payload']['commits']:
                    words = [word for word in re.compile('[^a-z\-\_]')\
                             .split(commit['message'].lower()) if word]
                    for word in words:
                        word_frequencies[word]+=1
    return word_frequencies

def reduce_results(results):
    word_frequencies = collections.defaultdict(lambda:0)
    for result in results:
        for word, frequency in result.items():
            word_frequencies[word]+=frequency
    return word_frequencies    

if __name__ == '__main__':
    files = get_files(data_directory)
    results = []
    for file in files:
        print("Analyzing {}".format(file))
        results.append(analyze_file(file))
    reduced_results = reduce_results(results)

    print("Top 100 words used in Github commits:")
    print("\n".join(["{:<40}:{}".format(word,frequency)
                     for word,frequency in 
                     sorted(reduced_results.items(),key=lambda x:-x[1])[:100]]))