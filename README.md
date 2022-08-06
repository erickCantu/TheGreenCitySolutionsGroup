# Forecasting building energy demand 

By: [Rafael Arndt](https://github.com/r4f), [Erick Cantu](https://github.com/eaunaicr97), [Leon Pichotka](https://github.com/Leee-P) and [Su Leen Wong](https://github.com/suleenwong)

![](images/splash.png)

This repository contains files and Jupyter notebooks related to our capstone project for the [Neuefische Data Science bootcamp](https://www.neuefische.de/en/bootcamp/data-science). This project focuses on forecasting the hourly building energy demand of 9 buildings in total from the CityLearn Challenge, based on 4 years energy consumption and weather data. 


## Introduction
Since energy prices are continuing to rise and the future of the energy 
situation is rather uncertain, cities may want to investigate the energy 
consumption of different building sectors to predict future energy demand and
identify areas where energy can be saved.

Energy demand forecasting is fundamental for an energy utility’s decision making on:

- Grid stability

- Planning power supply activities

- Reducing energy wastage

Since the data available consists of a series of energy consumption values taken sequentially with a fixed time interval over four years, time series analysis and models are ideal for this problem. 


## About the dataset

The dataset we used for this project consists of:
- Synthetic data of 4 years, 9 buildings from the CityLearn Challenge* (southern  US suburb)
- Hourly data of energy demand and solar generation
- Hourly weather data (temperature, humidity, solar radiation) 

The nine buildings in this dataset consist of:
- Building 1: Office building
- Building 2: Fast food restaurant
- Building 3: Standalone retail
- Building 4: Strip mall retail
- Buildings 5-9: Multi-family buildings

## Problem statement
Our goal is to model the net energy demand of a collection of 9 buildings which are part of the [2021 CityLearn Challenge](https://sites.google.com/view/citylearnchallenge).

First, the time series data was analyzed for trend and seasonality. 

It seemed suitable to forecast the energy demand for 24 hours, as weather predictions get less accurate further in the future. Else, the power suppliers energy management is mainly focused on a 24 hour period.


Different models were applied and compared:
- Baseline (last years values)
- Linear Regression
- Polynomial Regression
- SARIMAX
- Prophet
- TBats
- XGBoost
- Random Forest

## Results
A small trend in the net energy demand over 4 years was discovered with a slight increase over the first 3 years and a decrease in the 4th year (corresponding to the trend in the weather data). A clear yearly seasonality is found with the highest energy demand in summer (due to air conditioning) and the lowest energy demand in winter (due to mild winters). Furthermore a weekly as well as a daily seasonality was identified.  

> Figure with seasonality

The tree-based machine learning models (Random Forest and XGBoost) performed better than the time series models (SARIMAX, Prophet, TBats) taking the mean squared error as metric.

> Figure with model benchmark

> Figure with model predictions graph

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

