# 811372A-3007 Software Development, Maintenance and Operations 2025 Projects

This repository contains example data and scripts showcasing data collection and processing
for projects of the Software Development, Maintenance and Operations.

The three projects are:

- Project 1: Developer de-duplication

## Contents

- `project1devs/`: Directory with data for Project 1
  - `devs.csv`: List of developers mined from eShopOnContainersProject
  - `devs_similarity.csv`: Similarity tests for each pair of developers
  - `devs_similarity_t=0.7.csv`: Similarity tests for each pair of developers with similarity threshold 0.7
- `project1developers.py`: Script demonstrating mining developer information and Bird heuristic to determine duplicate developers

## Running the scripts

The scripts were developed and tested on a Mac (UNIX) environment with Python 3.10.
There should be no compatibility issues with running the scripts on Windows.

The versions of imported libraries are provided in `requirements.txt`.

It is recommended to create a Python virtual environment and install the exact versions there.