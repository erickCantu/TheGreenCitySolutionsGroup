import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from green_city.utils import datetime2index, index2datetime
import mlflow

# Function for plotting actual vs predicted net energy usage
def plot_ts(actual, predicted, title=None):
    """
    Plots the actual net energy usage against the predicted net energy usage
    """
    fig, ax = plt.subplots(figsize=(12,4))
    actual.plot(ax=ax, label="Actual net usage")
    predicted.plot(ax=ax, label="Predicted net usage")
    plt.xlabel('Date')
    plt.ylabel('Net energy usage [kW]')
    plt.legend()
    plt.title(title)
    plt.show()
    
    
def error_metrics(y_train, y_pred_train, y_test, y_pred_test, title=None):
    """
    Calculate and print error metrics for train and test data
    """
    r2_train = r2_score(y_train, y_pred_train)
    r2_test = r2_score(y_test, y_pred_test)
    mae = mean_absolute_error(y_test, y_pred_test)
    mse = mean_squared_error(y_test, y_pred_test)
    rmse = np.sqrt(mse)

    print("----------------------------------------")
    print(title)
    print("----------------------------------------")
    print("R2 (train):", r2_train.round(3))
    print("R2 (test) :", r2_test.round(3))
    print(f"MAE (test): {mae.round(3)}")
    print(f"MSE (test): {mse.round(3)}")
    print(f"RMSE(test): {rmse.round(3)}")
    
    return [mae, mse, r2_test]


def train_test_time_split(df, features, target, dummy_features):
    """
    Split data into train and test set
    Train data: First 3 years
    Test data:  Last year
    """
    df_train = df.iloc[:(len(df)-365*24)]   # First 3 years as train data
    df_test = df.iloc[(len(df)-365*24):]    # Last year as test data

    X = df[features]
    y = df[target]

    # Dummy variables
    for col in dummy_features:
        X[col] = X[col].astype('category')
    X = pd.get_dummies(X, drop_first=True)

    # First 3 years is the training data
    X_train = X[:(len(X)-365*24)]
    y_train = y[:(len(y)-365*24)]

    # Last year is the test data
    X_test = X[(len(X)-365*24):]
    y_test = y[(len(y)-365*24):]

    return X_train, y_train, X_test, y_test, df_train, df_test


def forecast_dates(df_test, run_name, write_data=False):
    
    # Randomly chosen list of indices to forecast
    pred_indices = [32135, 33311, 26478, 33357, 30387, 30794, 31800, 28783]

    mae_list = []
    mse_list = []
    r2_list = []
    forecasts = pd.DataFrame(columns=['prediction','run_id','id'])

    fig, ax = plt.subplots(4,2,figsize=(14,16))
    i = 1
    for index in pred_indices:

        day = index2datetime(index)
        start_hour = day + pd.DateOffset(hours=1)
        end_hour = day + pd.DateOffset(hours=24)
        forecast_hours = pd.date_range(start=start_hour, end=end_hour, freq='H')
        y_pred = df_test[run_name][df_test.index.isin(forecast_hours)]
        y_test = df_test['net_load_kW'][df_test.index.isin(forecast_hours)]

        # Print error metrics
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f"Day: {day}, mae: {mae:.3f}, mse: {mse:.3f}, rmse: {np.sqrt(mse):.3f}, r2: {r2:.3f}")
        mae_list.append(mae)
        mse_list.append(mse)
        r2_list.append(r2)

        # Plot actual vs predicted net energy usage for each of the chosen days
        plt.subplot(4, 2, i)
        df_test['net_load_kW'][df_test.index.isin(forecast_hours)].plot()
        df_test[run_name][df_test.index.isin(forecast_hours)].plot()
        plt.title(day)
        i = i + 1

        if write_data:
      
            # Starting the MLFlow run
            r = mlflow.start_run(run_name=run_name)
            print("run-uuid:", r.info.run_uuid)

            for k, v in global_params.items():
                mlflow.log_param(k, v)
                mlflow.log_param("model", run_name)
                mlflow.log_param("datetime", day)
                mlflow.log_param("feature", "net_load_kW")
                mlflow.log_metric("mse", mse)
                mlflow.log_metric("mae", mae)
                mlflow.log_metric("r2_score", r2)
            mlflow.end_run()
      
            # DataFrame for writing to SQL database
            day_forecast = pd.DataFrame(columns=['prediction','run_id','id'])
            day_forecast['prediction'] = y_pred
            day_forecast['run_id'] = r.info.run_uuid
            day_forecast['id'] = np.arange(index+1,index+25)
            forecasts = pd.concat([forecasts, day_forecast], axis=0)

    # Write to SQL DB
    if write_data:
        forecasts = forecasts.set_index('id')
        forecasts.to_sql("forecast", con=db, if_exists="append")

    print(f"Avg mae: {np.mean(mae_list):.3f}, Avg mse: {np.mean(mse_list):.3f}, Avg rmse: {np.sqrt(np.mean(mse_list)):.3f}, Avg r2: {np.mean(r2):.3f}")
    plt.subplots_adjust(hspace=0.5)
    plt.show()


def seasons(x):
    """
    Group months into seasons
    """
    if x in [12,1,2]:
        return 'winter'
    elif x in [3,4,5]:
        return 'spring'
    elif x in [6,7,8]:
        return 'summer'
    elif x in [9,10,11]:
        return 'autumn'


def time_of_day(x):
    """
    Group hours into morning, afternoon, evening or night
    """
    if x in [7, 8, 9, 10, 11]:
        return 'morning'
    elif x in [12, 13, 14, 15, 16]:
        return 'afternoon'
    elif x in [17, 18, 19, 20, 21]:
        return 'evening'
    elif x in [22, 23, 0, 1, 2, 3, 4, 5, 6]:
        return 'night'        


def add_fourier_terms(df, year_k, week_k, day_k):
    """
    df: dataframe to add the fourier terms to 
    year_k: the number of Fourier terms the year period should have. Thus the model will be fit on 2*year_k terms (1 term for 
    sine and 1 for cosine)
    week_k: same as year_k but for weekly periods
    day_k:same as year_k but for daily periods
    """
    
    for k in range(1, year_k+1):
        # year has a period of 365.25 including the leap year
        df['year_sin'+str(k)] = np.sin(2 *k* np.pi * df.index.dayofyear/365.25) 
        df['year_cos'+str(k)] = np.cos(2 *k* np.pi * df.index.dayofyear/365.25)

    for k in range(1, week_k+1):
        
        # week has a period of 7
        df['week_sin'+str(k)] = np.sin(2 *k* np.pi * df.index.dayofweek/7)
        df['week_cos'+str(k)] = np.cos(2 *k* np.pi * df.index.dayofweek/7)

    for k in range(1, day_k+1):
        
        # day has period of 24
        df['hour_sin'+str(k)] = np.sin(2 *k* np.pi * df.index.hour/24)
        df['hour_cos'+str(k)] = np.cos(2 *k* np.pi * df.index.hour/24) 