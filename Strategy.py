from TimeSeries import TimeSeries
from Portfolio import Portfolio
from Instrument import Instrument,Option,Index
from Position import Position
import pandas as pd
from pandas.tseries.offsets import BDay
import math

class Strategy(object):
    ''' Knows how to run itself will take data produce
    performance metrics P/L etc
    assumptions data format is csv file with rows: Date,Maturity,Spot,Volatility
    reference notional amount up to date
    '''
    def __init__(self,data,portfolio):
        self._data = data
        self._portfolio = portfolio

    def generate_freq_straddle(self,date,buy_sell,freq,percent_notional,days):
        '''
        long/short ('B'|'S') put/call at predefined day of the week as percentage of notional 25% is 0.25
        DOW expressed as in pandas DateIndex frequency - for every Friday - 'W-FRI' every 3rd Fri 'W-3FRI' and so on
        days maturity of the option(s)
        '''
        if percent_notional > 0.25:
            raise ValueError('Invest max 25% of notional')

        equivalent_notional_amount = self._portfolio.get_notional()*percent_notional

        trigger_days = self._data.get_data_with_frequency(freq)

        if date in trigger_days:
        #buy/sell equivalent options
            if equivalent_notional_amount > 0.0:
                try:
                    all_rows_for_date = self._data.get_rows('Date',int(date))
                except ValueError:
                    print('Date {} not found in datafile'.format(date))

                datetm = pd.to_datetime(date, format='%Y%m%d')
                expiry = (datetm + BDay(days)).date()

                self._generate_trade(date,all_rows_for_date,equivalent_notional_amount,expiry.strftime('%Y%m%d'),self._portfolio.get_rate())


    def _generate_trade(self,date,all_rows_for_date,equivalent_amount,expiry,rate):

        #vol = Helpers.get_vol_for_expiry(expiry,all_rows_for_date)
        spot = all_rows_for_date['Spot'].iloc[0]
        rounded_spot = int(math.ceil(spot / 10.0)) * 10
        call = Option('C',rounded_spot,int(expiry))
        args = rate, all_rows_for_date
        call_value = call.calc_value(args)

        put = Option('P',rounded_spot,int(expiry))
        args = rate, all_rows_for_date
        put_value = put.calc_value(args)

        avg_value = (call_value + put_value) / 2

        if call_value > 0.0 and put_value > 0.0:
            num_options = int(equivalent_amount/avg_value/2)

            call_pos = Position(call,-num_options,date)
            call_pos.set_initial_value(rate, all_rows_for_date)
            self._portfolio.insert_position(call_pos)

            put_pos = Position(put,-num_options,date)
            put_pos.set_initial_value(rate, all_rows_for_date)
            self._portfolio.insert_position(put_pos)

            #we sold num_calls and num_puts so amend the notional
            new_notional = self._portfolio.get_notional() + num_options*call_value + num_options*put_value

            self._portfolio.set_notional(new_notional)

    def hedge_portfolio(self,all_rows_for_date,delta):
        '''
        Calculate delta for date of the p-folio and buy/sell index
        :param all_rows_for_date:
        :param delta:
        :return:
        '''
        spot = all_rows_for_date['Spot'].iloc[0]

        df = self._portfolio.get_num_puts()
        total_options = self._portfolio.get_num_calls() + self._portfolio.get_num_puts()

        delta_hedge_amount = total_options*spot

def main():
    ts = TimeSeries('spx_vols.txt')
    pfolio = Portfolio(1000,0.05)

    strat = Strategy(ts,pfolio)

    date = '20130208'

    strat.generate_freq_straddle('20130208','S','W-FRI',0.25,25)



    #num_puts = pfolio.get_num_puts()

    #num_calls = pfolio.get_num_calls()

    #all_rows_for_date = ts.get_rows('Date',int(date))

    #instr = Option('C',1596.0,20160208)
    #pos = Position(instr,50)

    #pfolio.insert_position(pos)
    #pfolio.calc_delta(pfolio._rate,all_rows_for_date)

    #total_delta = pfolio.get_delta()

    #strat.hedge_portfolio(all_rows_for_date,total_delta)

if __name__ == '__main__':
    main()