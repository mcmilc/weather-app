import pandas as pd


def tuples_to_dataframe(data, columns):
    df = pd.DataFrame(data, columns=columns)
    return df
