import pandas as pd


def process(data1, data2):

    #filtering the summer olympics
    data1 = data1[data1['Season'] == 'Summer']

    #merge with region df
    data1 = data1.merge(data2, on='NOC', how='left')

    #drop duplicate

    data1.drop_duplicates(inplace=True)

    #encoding medals

    pd.concat([data1, pd.get_dummies(data1['Medal'])], axis=1)
    return data1