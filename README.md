## Map-Reduce With Docker

This is a very simple example of realizing a map-reduce style workflow with Docker and Python.

The example uses data from Github. To fetch the data, simply run `fetch_data.sh`.

To analyze the data normally:

    python analyze.py

To build the Docker image required for the docker-based analyis, run

    docker build --tag analysis_test .

Then simply run

    python docker_parallelize.py

This will launch a number of Docker containers, each of which will analyze a portion of the
data using the `docker_analyze.py` script.

To run the Docker container manually (e.g. for testing), use

    docker run -it -u `id -u $USER`:`id -u $USER` -P -e "INPUT_FILENAMES=2015-01-01-0.json.gz" -v [absolute-path-to-data-directory]:/data -v [absolute-path-to-output-directory]:/out analysis_test
