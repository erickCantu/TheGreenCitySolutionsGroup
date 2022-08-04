# The Energy of Tomorrow: Forecasting building energy demand 

### **The Green City Solutions Group**

Rafael Arndt, Erick Cantu, Leon Pichotka, Su Leen Wong


This repo contains files and jupyter notebooks related to the above project. This project focuses on predicting the hourly building energy demand of 9 buildings in total from the CityLearn Challenge, based on the past 4 years of hourly energy consumption data. 




## Introduction
Since energy prices are continuing to rise and the future of the energy 
situation is rather uncertain, cities may want to investigate the energy 
consumption of different building sectors to predict future energy demand and
identify areas where energy can be saved.

Energy demand forecasting is fundamental for an energy utility’s decision making on:

- Grid stability

- Planning power supply activities

- Reducing energy wastage

Our stakeholder is a city municipality aiming to reduce its energy consumption and . Our stakeholder aims to identify the types of buildings 

## About the dataset
- Synthetic data of 4 years, 9 buildings from the CityLearn Challenge* (southern  US suburb)
- Hourly data of energy demand and solar generation
- Hourly weather data (temperature, humidity, solar radiation) 

Building types:
- Building 1: Office building
- Building 2: Fast food restaurant
- Building 3: Standalone retail
- Building 4: Strip mall retail
- Buildings 5-9: Multi-family buildings

## Problem statement
Our goal is to model the net energy demand of a collection of 9 buildings which are part of the [2021 CityLearn Challenge](https://sites.google.com/view/citylearnchallenge).



## Results
We found that the time series consisted of a trend, a yearly seasonality, a weekly seasonality and a daily seasonality.

## Conclusion
The tree-based machine learning models (Random forest and XGBoost) produced forecasts with the lowest root mean squared error compared to the observed data.

## Future work



## Files and folders




## Requirements:

- pyenv with Python: 3.9.8


### Setup

Use the requirements file in this repo to create a new environment as follows:

```BASH
make setup
```
or

```BASH
pyenv local 3.9.8
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

The `requirements.txt` file contains the libraries needed for deployment.

