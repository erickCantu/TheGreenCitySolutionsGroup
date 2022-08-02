import pandas as pd
import sys
sys.path.append('../notebooks')
from green_city.regression import train_test_time_split, error_metrics

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

import warnings
warnings.filterwarnings('ignore')

def linreg_model(building_nr=5):

    df = pd.read_csv(f"../data/preprocessed/Building_{building_nr}.csv").astype({'datetime': 'datetime64'}).set_index('datetime')
    df.fillna(0.0, inplace=True)

    # Extra columns for time features
    df['hour'] = df.index.hour
    df['month'] = df.index.month
    df['year'] = df.index.year

    # Shift predicted weather values by 24hr
    df['pred_24h_diffuse_solar_W_m2_shift'] = df['pred_24h_diffuse_solar_W_m2'].shift(periods=24)
    df['pred_24h_direct_solar_W_m2_shift'] = df['pred_24h_direct_solar_W_m2'].shift(periods=24)
    df['pred_24h_outdoor_temp_shift'] = df['pred_24h_outdoor_temp'].shift(periods=24)
    df['pred_24h_outdoor_hum_shift'] = df['pred_24h_outdoor_hum'].shift(periods=24)
    df = df.dropna()    

    # Include current weather features for linear regression
    features = ['outdoor_temp', 'outdoor_hum', 
                'diffuse_solar_W_m2', 'direct_solar_W_m2', 
                'hour', 'month', 'holiday', 'workday']
    dummy_features = ['hour', 'month', 'holiday', 'workday']
    target = 'net_load_kW'

    # Do train-test split
    X_train, y_train, X_test, y_test, df_train, df_test = train_test_time_split(
                                                            df, features, target, 
                                                            dummy_features)

    # Scaling features
    scaled_features = ['outdoor_temp', 'outdoor_hum', 'diffuse_solar_W_m2', 'direct_solar_W_m2']
    scaler = StandardScaler()
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()
    X_train_scaled[scaled_features] = scaler.fit_transform(X_train_scaled[scaled_features])
    X_test_scaled[scaled_features] = scaler.transform(X_test_scaled[scaled_features])                                                    
    
    # here we will add the second degree polynomial features
    polynomial_features = PolynomialFeatures(degree=2, include_bias=False)
    x_poly_train = polynomial_features.fit_transform(X_train_scaled)   # Transform training data
    x_poly_test = polynomial_features.transform(X_test_scaled)         # Transform test data

    model_poly = LinearRegression() # Do linear regression
    model_poly.fit(x_poly_train, y_train)

    # Predict for train and test data
    y_pred_test = model_poly.predict(x_poly_test)
    y_pred_train = model_poly.predict(x_poly_train)

    # Calculate and print error metrics
    #_ = error_metrics(y_train, y_pred_train, y_test, y_pred_test, title="Linear regression with polynomial (n=2)")

    # Use 24h predicted weather features for linear regression
    features = ['pred_24h_outdoor_temp_shift', 'pred_24h_outdoor_hum_shift', 
                'pred_24h_diffuse_solar_W_m2_shift', 'pred_24h_direct_solar_W_m2_shift', 
                'hour', 'month', 'holiday', 'workday']
    dummy_features = ['hour', 'month', 'holiday', 'workday']
    target = 'net_load_kW'

    # Do train-test split
    X_train, y_train, X_test, y_test, df_train, df_test = train_test_time_split(
                                                            df, features, target, 
                                                            dummy_features)

    # Scaling features
    scaled_features_fc = ['pred_24h_outdoor_temp_shift', 'pred_24h_outdoor_hum_shift', 
                        'pred_24h_diffuse_solar_W_m2_shift', 'pred_24h_direct_solar_W_m2_shift']
    X_train_scaled_fc = X_train
    X_test_scaled_fc = X_test
    X_train_scaled_fc[scaled_features_fc] = scaler.transform(X_train_scaled_fc[scaled_features_fc])
    X_test_scaled_fc[scaled_features_fc] = scaler.transform(X_test_scaled_fc[scaled_features_fc])

    # Transform using previous transformation 
    x_poly_train_fc = polynomial_features.transform(X_train_scaled_fc) # Transform training x-data
    x_poly_test_fc = polynomial_features.transform(X_test_scaled_fc)   # Transform test x-data

    # Predict using already trained model
    y_pred_train_fc = model_poly.predict(x_poly_train_fc)
    y_pred_test_fc = model_poly.predict(x_poly_test_fc)

    # Save to DataFrame for plotting
    df_train['linreg_poly'] = y_pred_train_fc
    df_test['linreg_poly'] = y_pred_test_fc

    forecasts = df_test[['linreg_poly']]
    forecasts["datetime"] = forecasts.index
    #dates = df_test.index

    return forecasts