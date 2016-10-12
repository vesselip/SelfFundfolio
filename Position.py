from Instrument import Instrument, Option
import time

class Position(object):
    #Quantity positive for long and negative for short
    #Concept in the case of options: has the same type Put/Call, expiry, strike
    def __init__(self,Instrument,quantity,date):
        self.Instrument = Instrument
        self._quantity = quantity
        self._date = date #time.strftime("%d/%m/%Y")
        #self._value = Instrument.get_value()

    def calc_greeks(self):
        delta,gamma,vega,theta = self.Instrument.calc_greeks()
        return delta*self._quantity,gamma*self._quantity,vega*self._quantity,theta*self._quantity

    def set_quantity(self,quantity):
        self._quantity = quantity

    def get_quantity(self):
        return self._quantity

    def set_date(self,date):
        self._date = date

    def get_date(self):
        return self._date

    def get_value(self):
        return self._value

    def set_initial_value(self,*args):
        self._value = self.Instrument.set_initial_value(args)

    def calculate_value(self,*args):
        self._value = self.Instrument.calc_value(args)
        return self._value

    def calculate_position_pl(self,*args):
        return self.Instrument.calc_value_diff(args)*abs(self._quantity)

    def calculate_delta(self,*args):
        return self.Instrument.get_delta(args)*self._quantity

    def calculate_vega(self,*args):
        return self.Instrument.get_vega(args)*self._quantity

    def calculate_gamma(self,*args):
        return self.Instrument.get_gamma(args)*self._quantity

    def calculate_theta(self,*args):
        return self.Instrument.get_theta(args)*self._quantity

def main():
    #yearfrac = 20/365

    call = Option('C',2050.0,2050.0,0.05,0.3,'20160208')

    pos = Position(call,10,'20160208')
    a,b,c,d = pos.calc_greeks()
    pass

if __name__ == '__main__':
    main()
