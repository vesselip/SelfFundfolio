from Instrument import Instrument,Index,Option
from Position import Position
import pandas as pd

class Portfolio(object):

    def __init__(self,notional,rate):
        self.positions = []
        self.notional = notional
        self._rate = rate
        self._total_delta = 0.0
        self._total_delta_TMinus = 0.0
        self._total_vega = 0.0
        self._total_gamma = 0.0
        self._total_theta = 0.0
        self._total_put = 0.0
        self._total_call = 0.0
        self._total_index = 0.0
        self._total_PL = 0.0
        self._total_PL_TMinus = 0.0
        self._PL_TMinus_Diff = 0.0

    #calculate delta for the whole portfolio fore a date
    def calc_delta(self,rate,all_rows_for_date):
        self._total_delta_TMinus = self._total_delta
        self._total_delta = 0.0
        for pos in self.positions:
            if pos.get_quantity() != 0:
                if pos.Instrument.get_type() == 'Option':
                    self._total_delta += pos.calculate_delta(rate,all_rows_for_date)

        if self._total_delta == 0.0:
            r = 10
        return self._total_delta

    def get_delta(self):
        return self._total_delta

    #calculate delta for the whole portfolio fore a date
    def calc_gamma(self,rate,all_rows_for_date):
        self._total_gamma = 0.0
        for pos in self.positions:
            if pos.get_quantity() != 0:
                if pos.Instrument.get_type() == 'Option':
                    self._total_gamma += pos.calculate_gamma(rate,all_rows_for_date)
        return self._total_gamma

    def get_gamma(self):
        return self._total_gamma

    #calculate delta for the whole portfolio fore a date
    def calc_vega(self,rate,all_rows_for_date):
        self._total_vega = 0.0
        for pos in self.positions:
            if pos.get_quantity() != 0:
                if pos.Instrument.get_type() == 'Option':
                    self._total_vega += pos.calculate_vega(rate,all_rows_for_date)
        return self._total_vega

    def get_vega(self):
        return self._total_vega

    #calculate delta for the whole portfolio fore a date
    def calc_theta(self,rate,all_rows_for_date):
        self._total_theta = 0.0
        for pos in self.positions:
            if pos.get_quantity() != 0:
                if pos.Instrument.get_type() == 'Option':
                    self._total_theta += pos.calculate_theta(rate,all_rows_for_date)
        return self._total_theta

    def get_theta(self):
        return self._total_theta

    def value_portfolio(self, all_rows_for_date):
        #iterate through positions given
        for pos in self.positions:
            pos.get_value(all_rows_for_date)

    def insert_position(self,position):
        self.positions.append(position)

    def get_notional(self):
        return self.notional

    def set_notional(self,value):
        self.notional = value

    def get_rate(self):
        return self._rate

    def positions_count(self):
        return len(self.positions)

    def get_num_puts(self):
        self._total_put = 0
        for pos in self.positions:
            if pos.Instrument.get_type() == 'Option' and pos.Instrument.putcall == 'P' and pos.get_quantity() != 0:
                self._total_put += pos.get_quantity()
        return int(self._total_put)

    def get_num_calls(self):
        self._total_call = 0
        for pos in self.positions:
            if pos.Instrument.get_type() == 'Option' and pos.Instrument.putcall == 'C'  and pos.get_quantity() != 0:
                self._total_call += pos.get_quantity()

        return int(self._total_call)

    def get_num_index(self):
        for pos in self.positions:
            if pos.Instrument.get_type() == 'Index':
                self._total_index += pos.get_quantity()

        return int(self._total_index)

    def calc_pos_pl(self,all_rows_for_date):
        self._total_PL = 0.0
        for pos in self.positions:
            self._total_PL += pos.calculate_position_pl(self._rate,all_rows_for_date)
        self._PL_TMinus_Diff = self._total_PL - self._total_PL_TMinus
        self._total_PL_TMinus = self._total_PL

    def get_total_pl(self):
        return self._PL_TMinus_Diff

    def adjust_notional_by_pl(self):
        self.notional += self._PL_TMinus_Diff

    #close options about to expire
    def close_expired_options(self,date,all_rows_for_date):
        for pos in self.positions:
            if pos.Instrument.get_type() == 'Option' and pos.get_quantity() != 0:
                if pos.Instrument.get_expiry() == int(date):
                    if pos.get_quantity() < 0: #short
                        short_long = 'S'
                    else:
                        short_long = 'L'

                    new_notional = self.get_notional() + pos.Instrument.get_exercise_amount(self._rate,all_rows_for_date,short_long)*pos.get_quantity()
                    self.set_notional(new_notional)
                    pos.set_quantity(0)

    def delta_hedge_portfolio(self,delta,all_rows_for_date):
        spot = all_rows_for_date['Spot'].iloc[0]
        date = all_rows_for_date['Date'].iloc[0]
        #deltaDiff = self._total_delta - self._total_delta_TMinus
        #buy index
        if self._total_delta > 0.0:
            num = int(self._total_delta)
            if num > 0:
                notional = self.get_notional()
                amount = num*spot
                if amount <= notional:
                    instr = Index('SPX',spot)
                    pos = Position(instr,num,date)
                    self.insert_position(pos)
                    new_notional = notional - amount
                    self.set_notional(new_notional)

def main():

    yearfrac = 20/365
    call = Option('C',2050.0,2050.0,0.05,0.3,yearfrac)
    pos = Position(call,10)
    df = pd.DataFrame(pos)

    portfolio = Portfolio(100)
    #portfolio.add_position(pos)
    index = Index('SPX',2050.0)
    pos1 = Position(index,100)
    df.append(pos1)
    #portfolio.add_position(pos1)

    pass

if __name__ == '__main__':
    main()