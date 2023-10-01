import pandas as pd

def get_summary_stats(df: pd.DataFrame, category_column: str, value_columns: list[str]):
    agg_dict = {}
    for value_col in value_columns:
        agg_dict[value_col] = ['count', 'sum', 'mean', 'median', 'min', 'max']
    return df.groupby(category_column).agg(agg_dict)
