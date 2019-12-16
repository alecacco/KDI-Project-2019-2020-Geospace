# KDI-project-2019-2020
Project for the 2019/2020 Knowledge and Data Integration course @ UniTn

# Team Members

* Alessandro Cacco - Project Manager and Data Integration Coordinator
* Martina Battisti - Conceptual modeling coordinator 
* Bertiana Balliu - Conceptual modeling 
* Sara Callaioli - Data integration 
* Daniele Isoni - Data integration 
* Stefano Leonardi - Conceptual modeling 
* Michela Lorandi - Data integration

# Requirements

In order to reproduce every step of the process to create the final Knowledge graph in RDF format you must statisfy the following requirements:
* You must install the libpostal library and pypostal (the python wrapper for it), you can find instructions to install the library [here](https://github.com/openvenues/libpostal) and to install the python wrapper [here](https://github.com/openvenues/pypostal)
* You must have installed the python libraries in the requirements.txt file in the root of the repository


# Steps from data extraction to RDF generation

## Point Of Interest
All the scripts are intended to be run with the root of the repo as Working Directory.

### Province of Bolzano

* [Optional] if you want to see the original dataset run the `./models/script/POI/BZ/original-datasets-download.py` and you will find the dataset in the `./data/datasets/POI/BZ/original-datasets` folder
* [Optional] if you want to see the type analysis run the jupiter notebook `./models/script/POI/BZ/types_analysis.ipynb`
* To download the datasets ready for Karma you only need to run the `./models/script/POI/BZ/final-datasets-download.py` and you will find the dataset in the `./data/datasets/POI/BZ/final-datasets` folder ready to be imported in Karma
* Then on Karma you must upload the ontology, the dataset and the corresponding model. They can be easily matched because the structure of the folders and the name of the files are easy to match inside the two folder:

    1. `./data/datasets/POI/BZ` for the datasets (you always have to take the datasets under the final-datasets folder)
    2. `./models/r2ml/POI/BZ` for the models

### Province of Trento

* First you need to run the `./models/script/POI/TN/original-download-and-merge.py` that will create the file `./data/datasets/POI/TN/original-dataset-comuni.csv`
* Then you need to run the `./models/script/POI/TN/clean-dataset.py` that will clean the dataset and create the file `./data/datasets/POI/TN/cleaned-full-dataset-comuni.csv`
* Then run the `./models/script/POI/TN/separate-datasets.py` to create the datasets ready to be imported in Karma that can be found in `./data/datasets/POI/TN/final-datasets`
* Then on Karma you must upload the ontology, the dataset and the corresponding model. They can be easily matched because the structure of the folders and the name of the files are easy to match inside the two folder:

    1. `./data/datasets/POI/TN` for the datasets (you always have to take the datasets under the final-datasets folder)
    2. `./models/r2ml/POI/TN` for the models

## Accomodation

* [Optional] if you want to scrape the original dataset run the `./models/script/Accommodations/script_scraper.sh` and the dataset will be generated in the same folder
* [Optional] if you executed the first step, copy the generated dataset in your home and run the `./models/script/Accommodations/clean_json.py`
* If you do not want to scrape the dataset, copy the `./data/datasets/Accommodations/original-datasets/hotels.json` in your home directory
* To obtain the final dataset import in RapidMiner the process `./models/rapidminer/hotel_process.rmp`
* In RapidMiner, inside the Read XML block change the path to `./data/datasets/Accommodations/original-datasets/EserciziAlberghieri.xml`
* In RapidMiner, inside the Execute Python block change the path to `./models/script/Accommodations/cleanEncoding.py`
* In RapidMiner, inside the Write CSV block change the path to `./data/datasets/Accommodations/hotels_final.csv`
* Then on Karma you must upload the ontology, the dataset and the corresponding model:
    1. `./formal-model/SpaceDomain.owl` for the ontology
    2. `./data/datasets/Accommodations/hotels_final.csv` for the dataset
    3. `./models/r2ml/hotels_model.ttl` for the model

## Municipality
* First import the process `./models/rapidminer/Municipality/comuni_process.rpm` into RapidMiner
* Then change in the  `Read CSV` command the path of the csv file with your relative path. You can find the file in `./data/datasets/Municipality/original_dataset/Elenco-codici-statistici-e-denominazioni-al-30_06_2019.csv`
* Change in the  `Execute Python` command the path of the python script with your relative path. You can find the file in `./models/script/Municipality/comuni.py`
* You will find the final dataset on your desktop
* If you want to check the final output without running the RapidMiner process, you can find it in `./data/datasets/Municipality/final_dataset`
* [Optional] If you want to change the destination of the output, you need to modify the path in `Write File` command
* [Optional] The intermediate step `Write CSV` will save the file in your Desktop, and at the same location the python script will take the file just created. If you want to change the location, change the path in the commands and the python script

## Mountain datasets

### Mountain paths

The dataset of mountain paths are contained in `./data/datasets/Mountain/paths`, specifically:
* `topojson.json`, the json file containing the coordinates information about paths
* sentieri_coordinates.csv, the output of the parse_topojson.py script
* sentieri_coordinates_final.csv, the final output dataset of the rapidminer process

To correctly load the datasets:
* execute the python script `./models/script/Mountain/parse_topojson_sentieri.py` from the `.data/datasets/Mountain/paths` folder, in order to parse the topojson.json file into the `sentieri_coordinates.csv` file.
* execute the rapidminer process `./models/rapidminer/sentieri_rmprocess.rmp`, changing the path of the script to `./models/script/get_sentieri.py`, using as working directory the `./data/datasets/Mountain/paths` (to correctly load the `sentieri_coordinates.csv` file)

The output dataset of the RM process should correspond to the `sentieri_coordinates_final.csv` file. The corresponding Karma model is located in `./models/r2ml/sentieri_coordinates-model.tll`, which links the dataset to the ontology into `./data/linked_data/sentieri_karma_RDF.tll`.

### Mountain huts

The dataset folder `./data/datasets/Mountain/huts/rifugi.csv` can be obtained by executing the `./models/script/get_rifugi.py`, which scrapes all the data from the SAT APIs and website. This can be mapped with the `./models/r2ml/rifugi.csv-model.tll` model into the file `./data/linked_data/rifugi_karma_RDF.tll`

## Transportation
* First of all, trasform the data of Bolzano from VDV 452 standard to GTFS standard. You can find the original data in ```./data/datasets/Transportation/original_dataset/BZ/Original```. In order to do that follow the instruction of this public library [here](https://github.com/OneBusAway/onebusaway-vdv-modules). If you want to check the output you can find them in ```./data/datasets/Transportation/original_dataset/BZ/BZ_GTFS``` repository
* Import the process ```./models/rapidminer/Transportation/transportationProcess.rpm``` into RapidMiner
* Change the input files path with your relative path. You will find all the files in ```./data/datasets/Transportation/original_dataset```. Note that you need to put for each different name file ( ```agency.txt, calendar_dates.txt, calendar.txt, routes.txt, stop_times.txt, stops.txt, trips.txt```) the three files from different repositories (urbano_TTE, extraurbano_TTE and Bolzano) with the right order and with the right links to the union commands.
* Change in each ```Write CSV``` command the paths where you want to save the outputs with your relative paths.
* If you want to check the final output directly, you can find them in ```./data/datasets/Transportation/final_dataset```

## Merge all linked data

To merge all linked data you must first unzip all files inside the `./data/linked_data/` folder and then run the script `./models/script/merge_RDFs.py` that will merge all linked data in a big RDF that can be found at `./data/linked_data/GeoSpace_RDF.ttl.zip`. The file is zipped in order to be uploaded on github. This GeoSpace_RDF.ttl file will represent all our knowledge graph.

# Additional notes

The `./sparql_queries` folder contains all the queries we have produced. To check them load the final RDF `./data/linked_data/GeoSpace_RDF.ttl.zip` unzipped in GraphDB and run them.