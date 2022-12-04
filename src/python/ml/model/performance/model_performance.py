import pandas as pd

def get_performance_data(metrics_data):
  performance_df = pd.DataFrame()
  for model_name in metrics_data:
    df = pd.DataFrame(metrics_data[model_name])
    df.insert(loc=0, column='model_name', value=model_name)
    performance_df = pd.concat([df, performance_df])

  performance_df.reset_index(drop=True, inplace=True)
  return performance_df

def make_box_plots_for_models_performance_comparison(performance_df, metrics, title_metric):
  fig = make_subplots(rows=1, cols=len(metrics))
  for idx,metric_name in enumerate(metrics):
    metric_name_viz = metric_name.replace('_',' ').title()
    fig.add_trace(
        go.Box(x=performance_df['model_name'] ,y= performance_df[metric_name],
              name = metric_name_viz),
        row=1, col=idx+1,
        
    )      
  fig.update_layout(height=800, width=1200, title_text="Models Performance {} Comparison".format(title_metric))
  return fig