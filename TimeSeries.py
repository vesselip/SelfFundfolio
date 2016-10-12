import sys
import pandas as pd

#Check validity of of timeseries dates/vols
class TimeSeries(object):

    def __init__(self,path):
        self._dataframe = pd.read_csv(path)

    #freq='W-FRI' get Fridays from date range
    def get_data_with_frequency(self,freq):
        dates = self._dataframe['Date'].as_matrix()
        return pd.date_range(str(dates[0]),str(dates[-1]),freq=freq)

    def get_rows(self,colmn_name,value):
        rows = self._dataframe.loc[self._dataframe[colmn_name] == value]
        if rows.empty:
            raise ValueError('No rows found for value: {}'.format(value))
        return rows

    def get_volatility(self,maturity):
        return self._dataframe.loc(self._dataframe['Maturity'] >= maturity)

    def get_data(self):
        return self._dataframe

def main(path):
    df = TimeSeries(path[0])
    fridays = df.get_data_with_frequency('W-FRI')
    pass

if __name__ == '__main__':
    main(sys.argv[1:])