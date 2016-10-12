from BlackScholes import BlackScholes
from abc import ABCMeta, abstractmethod
from Helpers import Helpers
import math

class Instrument(object):

    def __init__(self, type):
        self._type = type
        self._value = 0.0#value
        self._initial_value = 0.0
        self._delta = 0

    @abstractmethod
    def get_type(self):
        pass

    def get_value(self):
        return self._value

    @abstractmethod
    def calc_greeks(self):
        pass

    @abstractmethod
    def calc_value(self,*args,modelname='BlackScholes'):
        pass

class Option(Instrument):
    #putcall = 'C|P', spot price, strike, rate, sigma, time to maturity in year fraction
    def __init__(self,putcall,strike,expiry):
        self._type = 'Option'
        self.putcall = putcall
        self._strike = strike
        self._expiry = int(expiry)
        self._model = None
        self._value = 0.0
        self._initial_value = 0.0

    def get_value(self):
        return self._value

    def get_initial_value(self):
        return self._initial_value

    def set_initial_value(self,args):
        self._initial_value = self.calc_value(args)

    #def calc_value(self,valuedate,spot,rate,sigma,modelname='BlackScholes'):
    def calc_value(self,args,modelname='BlackScholes'):
        rate = args[0]
        rows = args[1]
        valuedate = rows['Date'].iloc[0]
        spot = rows['Spot'].iloc[0]
        #rounded_spot = int(math.ceil(spot / 10.0)) * 10
        vol = Helpers.get_vol_for_expiry(self._expiry,rows)

        if valuedate < self._expiry:
            buss_days = Helpers.get_business_days(str(valuedate),str(self._expiry))
            day_fract = Helpers.get_day_fraction(buss_days,250)
            if modelname == 'BlackScholes':
                self._model = BlackScholes(self.putcall,spot,self._strike,rate,vol,day_fract)
                self._value = self._model.calc_value()

        return self._value

    def get_exercise_amount(self,*args,modelname='BlackScholes'):
        rows = args[1]
        short_long = args[2]
        spot = rows['Spot'].iloc[0]

        if short_long == 'S' and self.putcall == 'C': # and spot < (self._strike + self._initial_value): #short call spot < strike
            profit_loss = self._strike + self._initial_value - spot
        elif short_long == 'S' and self.putcall == 'P': #and spot > self._strike: #long call spot > strike
            profit_loss = spot + self._initial_value - self._strike

        return profit_loss

    def calc_greeks(self,args,modelname='BlackScholes'):
        return self.get_delta(args,modelname='BlackScholes'), self.get_gamma(args,modelname='BlackScholes'), self.get_vega(args,modelname='BlackScholes'), self.get_theta(args,modelname='BlackScholes')

    def get_delta(self,args,modelname='BlackScholes'):
        rate = args[0]
        rows = args[1]
        valuedate = rows['Date'].iloc[0]
        spot = rows['Spot'].iloc[0]
        #rounded_spot = int(math.ceil(spot / 10.0)) * 10
        vol = Helpers.get_vol_for_expiry(self._expiry,rows)

        if valuedate < self._expiry:
            buss_days = Helpers.get_business_days(str(valuedate),str(self._expiry))
            day_fract = Helpers.get_day_fraction(buss_days,252)
            if modelname == 'BlackScholes':
                self._model = BlackScholes(self.putcall,spot,self._strike,rate,vol,day_fract)

                return self._model.calc_delta()
        else:
            return 0.0

    def get_gamma(self,args,modelname='BlackScholes'):
        rate = args[0]
        rows = args[1]
        valuedate = rows['Date'].iloc[0]
        spot = rows['Spot'].iloc[0]
        rounded_spot = int(math.ceil(spot / 10.0)) * 10
        vol = Helpers.get_vol_for_expiry(self._expiry,rows)

        if valuedate < self._expiry:
            buss_days = Helpers.get_business_days(str(valuedate),str(self._expiry))
            day_fract = Helpers.get_day_fraction(buss_days,250)
            if day_fract == 0.0:
                r = 0
            if modelname == 'BlackScholes':
                self._model = BlackScholes(self.putcall,rounded_spot,self._strike,rate,vol,day_fract)

                return self._model.calc_gamma()
        else:
            return 0.0

    def get_vega(self,args,modelname='BlackScholes'):
        rate = args[0]
        rows = args[1]
        valuedate = rows['Date'].iloc[0]
        spot = rows['Spot'].iloc[0]
        rounded_spot = int(math.ceil(spot / 10.0)) * 10
        vol = Helpers.get_vol_for_expiry(self._expiry,rows)

        if valuedate < self._expiry:
            buss_days = Helpers.get_business_days(str(valuedate),str(self._expiry))
            day_fract = Helpers.get_day_fraction(buss_days,250)
            if modelname == 'BlackScholes':
                self._model = BlackScholes(self.putcall,rounded_spot,self._strike,rate,vol,day_fract)
                vg = self._model.calc_vega()
                return self._model.calc_vega()
        else:
            return 0.0

    def get_theta(self,args,modelname='BlackScholes'):
        rate = args[0]
        rows = args[1]
        valuedate = rows['Date'].iloc[0]
        spot = rows['Spot'].iloc[0]
        rounded_spot = int(math.ceil(spot / 10.0)) * 10
        vol = Helpers.get_vol_for_expiry(self._expiry,rows)

        if valuedate < self._expiry:
            buss_days = Helpers.get_business_days(str(valuedate),str(self._expiry))
            day_fract = Helpers.get_day_fraction(buss_days,250)
            if modelname == 'BlackScholes':
                self._model = BlackScholes(self.putcall,rounded_spot,self._strike,rate,vol,day_fract)

                return self._model.calc_theta(self.putcall)
        else:
            return 0.0

    #difference of purchase value and current one
    def calc_value_diff(self,args):
        return self.calc_value(args) - self.get_initial_value()

    def get_type(self):
        return 'Option'

    def get_expiry(self):
        return self._expiry

class Index(Instrument):

    def __init__(self, name, value):
        self._initial_value = value
        self._name = name

    def get_name(self):
        return self._name

    def get_value(self):
        return self._value

    def get_initial_value(self):
        return self._initial_value

    def get_type(self):
        return 'Index'

    def calc_value(self,args):
        rows = args[1]
        self._value = rows['Spot'].iloc[0]
        return self._value

    def calc_value_diff(self,args):
        return self.calc_value(args) - self.get_initial_value()


def main():
    idx = Index('SPX',100.0)
    sd = idx.get_type()

    yearfrac = 20/365

    call = Option('C',2050.0,2050.0,0.05,0.3,yearfrac)
    callval = call.calc_value()
    delta,gamma,vega,theta = call.calc_greeks()

    put = Option('P',2050.0,2050.0,0.05,0.3,yearfrac)
    putval = put.calc_value()
    delta,gamma,vega,theta = put.calc_greeks()

    pass

if __name__ == '__main__':
    main()