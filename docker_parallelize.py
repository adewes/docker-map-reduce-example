import docker
import os
import math
import json
import collections

CONTAINER_NAME = 'analysis_test'
DATA_DIRECTORY = os.path.abspath('data')
OUTPUT_DIRECTORY = os.path.abspath('out')
N = 6

"""
Supervisor script to launch Docker containers and reduce the results produced by them.
"""

client = docker.Client()

def get_files(directory):
    filenames = os.listdir(directory)
    return sorted([filename for filename in filenames if filename.endswith('.json.gz')])

def reduce_output_files():
    filenames = [filename for filename in os.listdir(OUTPUT_DIRECTORY) if filename.endswith('.json')]
    results = []
    for filename in filenames:
        with open(os.path.join(OUTPUT_DIRECTORY,filename),'r') as input_file:
            results.append(json.loads(input_file.read()))
    return reduce_results(results)

def reduce_results(results):
    word_frequencies = collections.defaultdict(lambda:0)
    for result in results:
        for word, frequency in result.items():
            word_frequencies[word]+=frequency
    return word_frequencies    

def analyze_files_in_container(files):
    print("Launching container for files {}".format(", ".join(files)))

    host_config = client.create_host_config(
        binds={
            DATA_DIRECTORY : {
                'bind' : '/data',
                'mode' : 'ro'
            },
            OUTPUT_DIRECTORY : {
                'bind' : '/out',
                'mode' : 'rw'
            }
        },
        )

    environment = {
            'INPUT_FILENAMES' : ';'.join(files)
        }

    container = client.create_container(
        image='analysis_test',
        host_config=host_config,
        environment=environment)   

    client.start(container)

    return container

if __name__ == '__main__':

    files = get_files(DATA_DIRECTORY)
    chunk_size = int(math.ceil(len(files)/float(N)))
    containers = []

    for i in range(0,len(files),chunk_size):
        files_chunk = files[i:i+chunk_size]
        containers.append(analyze_files_in_container(files_chunk))

    print("Waiting for containers to finish...")

    for container in containers:
        exit_code = client.wait(container)
        print("Container exited with code {}".format(exit_code))

    reduced_results = reduce_output_files()

    print("Top 100 words used in Github commits:")
    print("\n".join(["{:<40}:{}".format(word,frequency)
                     for word,frequency in 
                     sorted(reduced_results.items(),key=lambda x:-x[1])[:100]]))