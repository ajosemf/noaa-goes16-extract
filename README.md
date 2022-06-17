# NOAA GOES16 data extraction
A minimal implementation to extract GOES16 satellite data on AWS using python

### Requirements
[Conda](https://docs.conda.io/projects/conda/en/latest/commands/install.html) >= 4.11.0

### Install
Create and activate conda environment
```
conda env create -f environment.yml
conda activate goes16-extract
```

### Running
Type:
```
python -m src.etl
```
