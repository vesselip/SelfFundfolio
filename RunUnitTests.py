import unittest
from TimeSeries import TimeSeries
from Portfolio import Portfolio
from Instrument import Instrument, Index, Option
from Position import Position
from Strategy import Strategy
from BlackScholes import BlackScholes

class TestBacktests(unittest.TestCase):
    """
    Running tests: Check validity of of timeseries dates/vols
    test get_data_with_frequency
    """
    def setUp(self):
        self.ts = TimeSeries('spx_vols.txt')
        date = '20130204'
        all_rows_for_date = self.ts.get_rows('Date',int(date))

        initial_notional = 1000
        rate = 0.05
        self.portfolio = Portfolio(initial_notional,rate)

        #Index position
        instr1 = Index('SPX',1056.0)
        pos1 = Position(instr1,10,'20130204')
        #pos1.calc_value(rate,all_rows_for_date)
        instr2 = Option('C',1510,'20130220')
        pos2 = Position(instr2,10,'20130204')
        pos2.set_initial_value(rate,all_rows_for_date)
        instr3 = Option('P',1510,'20130220')
        pos3 = Position(instr3,10,'20130204')
        pos3.set_initial_value(rate,all_rows_for_date)

        self.portfolio.insert_position(pos1)
        self.portfolio.insert_position(pos2)
        self.portfolio.insert_position(pos3)

    def test_calculate_position_index(self):
        date = '20130204'
        all_rows_for_date = self.ts.get_rows('Date',int(date))

        for pos in self.portfolio.positions:
            if pos.Instrument.get_type() == 'Index':
                pos_value = pos.calculate_value(self.portfolio._rate,all_rows_for_date)

        self.assertEqual(round(pos_value,2), 1495.71)

    def test_calculate_position_option(self):
        date = '20130204'
        all_rows_for_date = self.ts.get_rows('Date',int(date))
        mat = all_rows_for_date['Maturity']

        for pos in self.portfolio.positions:
            if pos.Instrument.get_type() == 'Option':
                pos_value = pos.calculate_value(self.portfolio._rate,all_rows_for_date)

        self.assertEqual(round(pos_value,4), round(21.4005,4))

    def test_position_pl(self):

        date = '20130205'
        all_rows_for_date = self.ts.get_rows('Date',int(date))
        self.portfolio.calc_pos_pl(all_rows_for_date)

        PL = self.portfolio.get_total_pl()

        self.assertEqual(round(PL,4), round(4504.9577,4))

    def test_bs_greeks(self):
        S0 = 1520.0
        K = 1520.0
        r = 0.05
        vol = 0.11
        T = 0.083 #a month

        c_BS = BlackScholes('C',S0, K, r, vol, T)

        self.assertEqual(round(c_BS.calc_value(),4),22.488)
        self.assertEqual(round(c_BS.calc_delta(),4),0.4416)
        self.assertEqual(round(c_BS.calc_gamma(),4),0.0082)
        self.assertEqual(round(c_BS.calc_vega(),4),1.7283)
        self.assertEqual(round(c_BS.calc_theta('C'),4),-0.4269)

    def test_portfolio_calc_delta(self):
        date = '20130205'
        all_rows_for_date = self.ts.get_rows('Date',int(date))

        instr = Option('P',1596.0,'20130220')
        pos = Position(instr,5,date)

        self.portfolio.insert_position(pos)

        self.portfolio.calc_delta(self.portfolio._rate,all_rows_for_date)

        total_delta = self.portfolio.get_delta()

        self.assertEqual(round(total_delta,4), round(-1.2165,4))

    def test_portfolio_calc_gamma(self):
        date = '20130205'
        all_rows_for_date = self.ts.get_rows('Date',int(date))

        instr = Option('P',1596.0,'20130220')
        pos = Position(instr,50,date)

        self.portfolio.insert_position(pos)

        self.portfolio.calc_gamma(self.portfolio._rate,all_rows_for_date)

        total_gamma = self.portfolio.get_gamma()

        self.assertEqual(round(total_gamma,4), round(0.2851,4))

    def test_portfolio_calc_vega(self):
        date = '20130205'
        all_rows_for_date = self.ts.get_rows('Date',int(date))

        instr = Option('P',1596.0,'20130220')
        pos = Position(instr,50,date)

        self.portfolio.insert_position(pos)

        self.portfolio.calc_vega(self.portfolio._rate,all_rows_for_date)

        total_vega = self.portfolio.get_vega()

        self.assertEqual(round(total_vega,4), round(31.0876,4))

    def test_portfolio_calc_theta(self):
        date = '20130205'
        all_rows_for_date = self.ts.get_rows('Date',int(date))

        instr = Option('P',1596.0,'20130220')
        pos = Position(instr,50,date)

        self.portfolio.insert_position(pos)

        self.portfolio.calc_theta(self.portfolio._rate,all_rows_for_date)

        total_theta = self.portfolio.get_theta()

        self.assertEqual(round(total_theta,4), round(-0.2879,4))

    def test_hedge_portfolio(self):
        date = '20130204'
        all_rows_for_date = self.ts.get_rows('Date',int(date))

        st = Strategy(self.ts,self.portfolio)

        instr = Option('P',1596.0,'20130225')
        pos = Position(instr,50,date)

        self.portfolio.set_notional(3000)
        self.portfolio.insert_position(pos)
        self.portfolio.calc_delta(self.portfolio._rate,all_rows_for_date)

        total_delta = self.portfolio.get_delta()

        self.portfolio.delta_hedge_portfolio(total_delta,all_rows_for_date)

        self.assertEqual(round(self.portfolio.get_notional(),4), 1504.29)

if __name__ == "__main__":
    unittest.main()
    exit(0)
