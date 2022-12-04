import pandas as pd

def get_performance_data(metrics_data):
  performance_df = pd.DataFrame()
  for model_name in metrics_data:
    df = pd.DataFrame(metrics_data[model_name])
    df.insert(loc=0, column='model_name', value=model_name)
    performance_df = pd.concat([df, performance_df])

  performance_df.reset_index(drop=True, inplace=True)
  return performance_df
