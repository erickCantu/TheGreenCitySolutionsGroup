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
 
## Prerequisites / How to run
The project notebooks require a `pyenv with Python: 3.9.8`.  To properly setup the environment use the requirements file in the repository as follows:

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


The `requirements.txt` file contains the libraries needed for the EDA, Time Series Analysis and the dash board deployment. 

The time series models results (MAE, MSE and R2)P are trackable through [MLFlow](https://mlflow.org).  The required MLFLOW URI file is not part of this repository.  Before running the time series jupyter notebooks and locally save the results you require a `.mlflow_uri` file in the repository root. In bash do:

```BASH
echo http://127.0.0.1:5000/ > .mlflow_uri
```

This will create a local file where the uri is stored which will not be added on github (`.mlflow_uri` is in the `.gitignore` file). 

Before running the time series notebook, check your local mlflow by:


```bash
mlflow ui
```

and open the link [http://127.0.0.1:5000](http://127.0.0.1:5000)

The dashboard deployment can be accessed by running:

```BASH
cd dashboard
python dasboard.py 
````
and openning the link [http://127.0.0.1:8113/](http://127.0.0.1:8113/)

## Files 
Original data is available at [Citylearn v1.0.0 release](https://github.com/intelligent-environments-lab/CityLearn/releases/tag/v1.0.0). Preprocessed data for our analysis is located at the [preprocessed folder](https://github.com/eaunaicr97/TheGreenCitySolutionsGroup/tree/main/data/preprocessed).

Jpyther notebooks are divided in two sections. Exploratory Data Analysis (EDA) and Time Series (TS) models. These sections are part of the notebook prefix name. 

|EDA   | Description |
|:---|---|
|[Data Pre-processing](https://github.com/eaunaicr97/TheGreenCitySolutionsGroup/blob/main/notebooks/EDA_preprocessing.ipynb)|Data setup for time series analysis|
|[Weather analysis](https://github.com/eaunaicr97/TheGreenCitySolutionsGroup/blob/main/notebooks/EDA_weather.ipynb)|Exploratory analysis on weather variables. e.g. Temperature, Solar radiation.|
|[Seasonality decomposition](https://github.com/eaunaicr97/TheGreenCitySolutionsGroup/blob/main/notebooks/EDA_Weekly_Decomposition.ipynb)|Seasonality decomposition. Moving average period = 7 days|
|[Data Visualization](https://github.com/eaunaicr97/TheGreenCitySolutionsGroup/blob/main/notebooks/EDA_data_visualization.ipynb)|Data visualization|
|[Yearly seasonality decomposition](https://github.com/eaunaicr97/TheGreenCitySolutionsGroup/blob/main/notebooks/EDA_data_visualization_weekly.ipynb)|Yearly seasonality decomposition. And meteorological seasons analysis. Moving average period = 7 days|
|||


|TS 8 day predictions models |Description|
|:---|:---|
|[Base line](https://github.com/eaunaicr97/TheGreenCitySolutionsGroup/blob/main/notebooks/TS_baseline.ipynb)|Previous 24 hrs energy demand value|
|[Linear Regression](https://github.com/eaunaicr97/TheGreenCitySolutionsGroup/blob/main/notebooks/Regression.ipynb)||
|[Polynomial Regression](https://github.com/eaunaicr97/TheGreenCitySolutionsGroup/blob/main/notebooks/Regression.ipynb)||
|[SARIMAX](https://github.com/eaunaicr97/TheGreenCitySolutionsGroup/blob/main/notebooks/TS_24h_sarimax.ipynb)||
|[Prophet](https://github.com/eaunaicr97/TheGreenCitySolutionsGroup/blob/main/notebooks/TS_prophet.ipynb)|Model with hyperparameter optimization, holidays, weather data as additional reggressors and weekly seasonality by meteorological seasons|
|[TBats](https://github.com/eaunaicr97/TheGreenCitySolutionsGroup/blob/main/notebooks/TS_24h_tbats.ipynb)||
|[XGBoost](https://github.com/eaunaicr97/TheGreenCitySolutionsGroup/blob/main/notebooks/TS_XGBoost.ipynb)||
|[Random Forest](https://github.com/eaunaicr97/TheGreenCitySolutionsGroup/blob/main/notebooks/ML.ipynb)||
|||




## Future work
We have two approaches for our future work. A business approach and an Machine Learning optimization approach. 

For our business oriented future work. We plan to implement a dashboard solution to predict real-time energy demand.  The solution will allow the stockholder to feed current data, helping them with their decisions to balance their energy demand.

At our Machine Learning optimization approach. We plan to optimize the models generalization with respect to different climate zones. Our plan is to evaluate a one solution for all climate zones vs individual climate zone solutions. Furthermore we plant to develop a reinforcement learning agent(s) with the aim of battery usage optimization towards cost reduction and energy grid stability improvement.