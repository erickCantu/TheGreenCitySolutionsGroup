import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

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
    