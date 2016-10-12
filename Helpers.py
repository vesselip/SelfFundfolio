import numpy as np
import datetime as dt

class Helpers(object):

    @staticmethod
    def get_business_days(startdate,enddate):
        start = dt.datetime.strptime(startdate,'%Y%m%d').date()
        end = dt.datetime.strptime(enddate,'%Y%m%d').date()

        return np.busday_count( start, end )

    @staticmethod
    def get_day_fraction(interval,day_count_convention):
        return interval/day_count_convention

    #TODO: Here it should really be interpolating between the dates ot getting the vol close to expiry
    @staticmethod
    def get_vol_for_expiry(expiry,df):
        vol_tr = df['Volatility'].where(df['Maturity'] >= float(expiry))
        vol_not_nan = [x for x in vol_tr if str(x) != 'nan']
        return vol_not_nan[0]

    @staticmethod
    def timestamp_str(tstamp):
        strdate = dt.time.strftime('%Y%m%d', tstamp)
        return strdate



def main():
    days = Helpers.get_business_days('20160506','20160511')
    fract = Helpers.get_day_fraction(days,356)
    pass

if __name__ == '__main__':
    main()