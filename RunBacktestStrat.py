import argparse
from Portfolio import Portfolio
from Instrument import Instrument
from TimeSeries import TimeSeries
from Strategy import Strategy
import time

class Backtest(object):
    def __init__(self,portfolio,percent_notional,days_to_maturity,rate):
        self.portfolio = portfolio
        self.dataframe = None
        self.percent_notional = percent_notional
        self.days_to_maturity = days_to_maturity

    def run_backtest(self):
        try:
            self.dataframe = TimeSeries('spx_vols.txt')

        except (FileNotFoundError, IOError):
            print("Wrong file or file path")

        data = self.dataframe.get_data()
        dates = sorted(set(data['Date']))
        strategy = Strategy(self.dataframe,self.portfolio)
        rate = self.portfolio.get_rate()

        for date in dates:
            strategy.generate_freq_straddle(str(date),'S','W-FRI',self.percent_notional,self.days_to_maturity)
            all_rows_for_date = self.dataframe.get_rows('Date',int(date))
            self.portfolio.calc_delta(rate,all_rows_for_date)
            self.portfolio.calc_gamma(rate,all_rows_for_date)
            self.portfolio.calc_vega(rate,all_rows_for_date)
            self.portfolio.calc_theta(rate,all_rows_for_date)
            print('Portfolio level greeks for Date: {} Delta {}, Gamma = {}, Vega = {}, Theta = {}'.format(date,self.portfolio.get_delta(),self.portfolio.get_gamma(),self.portfolio.get_vega(), self.portfolio.get_theta()))
            self.portfolio.delta_hedge_portfolio(self.portfolio.get_delta(),all_rows_for_date)
            self.portfolio.close_expired_options(date,all_rows_for_date)
            self.portfolio.calc_pos_pl(all_rows_for_date)
            self.portfolio.adjust_notional_by_pl()
            print('Portfolio composed of #Index {} #Calls {} #Puts {} PL {} Cash {} negative values for Call/Put indicates short position'.format(self.portfolio.get_num_index(),self.portfolio.get_num_calls(),self.portfolio.get_num_puts(),self.portfolio.get_total_pl(),self.portfolio.get_notional()))
            if self.portfolio.get_notional() <= 0.0:
                print('Sorry the reference notional is 0, we run out of cash')
                exit(0)

def main():
    initial_notional = 10000
    rate = 0.05
    portfolio = Portfolio(initial_notional,rate)

    backtest = Backtest(portfolio,0.25,25,0.05)
    backtest.run_backtest()

if __name__ == '__main__':
    main()