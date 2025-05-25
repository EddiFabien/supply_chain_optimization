import pandas as pd
from ast import literal_eval
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose
from pmdarima import auto_arima
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import os
import warnings

warnings.filterwarnings("ignore")


def load_data(filepath):
    df = pd.read_csv(filepath)
    df['Date'] = pd.to_datetime(df['Date'])
    df['context'] = df['context'].apply(safe_literal_eval)
    return df


def prepare_time_series(df):
    grouped = df.groupby('context')
    context_series = {}

    for context, group in grouped:
        ts = group.sort_values('Date').set_index('Date')['Quantity']
        ts = ts.resample('D').sum().fillna(0)
        context_series[context] = ts

    return context_series


def test_stationarity(ts):
    result = adfuller(ts)
    return result[1] < 0.05  # Stationary if p-value < 0.05


def decompose_series(ts, context, output_dir):
    result = seasonal_decompose(ts, model='additive', period=7)
    result.plot()
    plt.suptitle(f"Decomposition for {context}", fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, f"decomposition_{context[0]}_{context[1][:10]}.png"))
    plt.close()


def fit_predict_arima(ts, train_size=0.8, steps=30):
    stationary = test_stationarity(ts)
    if not stationary:
        ts = ts.diff().dropna()

    split_idx = int(len(ts) * train_size)
    train, test = ts[:split_idx], ts[split_idx:]

    model = auto_arima(train, seasonal=False, stepwise=True, suppress_warnings=True)
    forecast, conf_int = model.predict(n_periods=len(test), return_conf_int=True, alpha=0.05)
    rmse = mean_squared_error(test, forecast, squared=False)
    return forecast, conf_int, model, test, rmse


def main():
    DATA_PATH = "dataset/data_processed/demand_processed.csv"
    OUTPUT_PREDICTIONS_DIR = "src/models/demand_predictions"
    OUTPUT_DECOMP_DIR = "src/models/demand_decompositions"
    OUTPUT_METRICS_FILE = "src/models/performance_metrics/demand_performance.csv"

    os.makedirs(OUTPUT_PREDICTIONS_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DECOMP_DIR, exist_ok=True)
    os.makedirs("src/models", exist_ok=True)

    print("🔄 Loading data...")
    df = load_data(DATA_PATH)

    print("🔄 Preparing time series per context...")
    series_dict = prepare_time_series(df)

    print("📈 Training ARIMA models and forecasting...")
    metrics = []

    for context, ts in series_dict.items():
        if len(ts) < 60:
            continue

        try:
            print(f"→ Processing context: {context}")
            decompose_series(ts, context, OUTPUT_DECOMP_DIR)
            forecast, conf_int, model, test, rmse = fit_predict_arima(ts, steps=30)

            dates = test.index
            pred_df = pd.DataFrame({
                'Date': dates,
                'Forecasted_Quantity': forecast,
                'Lower_Bound': conf_int[:, 0],
                'Upper_Bound': conf_int[:, 1],
                'Actual': test.values
            })
            filename = f"{context[0]}_{context[1][:10]}_forecast.csv".replace(' ', '_')
            pred_df.to_csv(os.path.join(OUTPUT_PREDICTIONS_DIR, filename), index=False)

            metrics.append({
                'Context': f"{context[0]}_{context[1]}",
                'RMSE': rmse
            })

        except Exception as e:
            print(f"⚠️ Erreur pour {context}: {e}")

    # Save performance metrics
    pd.DataFrame(metrics).to_csv(OUTPUT_METRICS_FILE, index=False)


def safe_literal_eval(val):
    try:
        return literal_eval(val)
    except Exception:
        return val


if __name__ == "__main__":
    main()
