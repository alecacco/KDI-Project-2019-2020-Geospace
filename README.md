# KDI-project-2019-2020
Project for the 2019/2020 Knowledge and Data Integration course @ UniTn

# Requirements

In order to reproduce every step of the process to create the final Knowledge graph in RDF format you must statisfy the following requirements:
* You must install the libpostal library and pypostal (the python wrapper for it), you can find instructions to install the library [here](https://github.com/openvenues/libpostal) and to install the python wrapper [here](https://github.com/openvenues/pypostal)
* You must have installed the python libraries in the requirements.txt file in the root of the repository


# Steps from data extraction to RDF generation

All the scripts are intended to be run with the root of the repo as Working Directory.

## Point Of Interest

### Province of Bolzano

* [Optional] if you want to see the original dataset run the ```./models/script/POI/BZ/original-datasets-download.py``` and you will find the dataset in the ```./data/datasets/POI/BZ/original-datasets``` folder
* [Optional] if you want to see the type analysis run the jupiter notebook ```./models/script/POI/BZ/types_analysis.ipynb```
* To download the datasets ready for Karma you only need to run the ```./models/script/POI/BZ/final-datasets-download.py``` and you will find the dataset in the ```./data/datasets/POI/BZ/final-datasets``` folder ready to be imported in Karma
* Then on Karma you must upload the ontology, the dataset and the corresponding model. They can be easily matched because the structure of the folders and the name of the files are easy to match under the two folder:

    1. `./data/datasets/POI/BZ` for the datasets (you always have to take the datasets under the final-datasets folder)
    2. `./models/r2ml/POI/BZ` for the models

### Province of Trento

* First you need to run the ```./models/script/POI/TN/original-download-and-merge.py``` that will create the file ```./data/datasets/POI/TN/original-dataset-comuni.csv```
* Then you need to run the ```./models/script/POI/TN/clean-dataset.py``` that will clean the dataset and create the file ```./data/datasets/POI/TN/cleaned-full-dataset-comuni.csv```
* Then run the ```./models/script/POI/TN/separate-datasets.py``` to create the datasets ready to be imported in Karma that can be found in ```./data/datasets/POI/TN/final-datasets```
* Then on Karma you must upload the ontology, the dataset and the corresponding model. They can be easily matched because the structure of the folders and the name of the files are easy to match under the two folder:

    1. `./data/datasets/POI/TN` for the datasets (you always have to take the datasets under the final-datasets folder)
    2. `./models/r2ml/POI/TN` for the models

## Merge all linked data

To merge all linked data you must first unzip all files inside the `./data/linked_data/` folder and then run the script ```./models/script/merge_RDFs.py``` that will merge all linked data in a big RDF that can be found at ```./data/linked_data/GeoSpace_RDF.ttl.zip```. The file is zipped in order to be uploaded on github. This GeoSpace_RDF.ttl file will represent all our knowledge graph.