import numpy as np
import scipy.stats as ss
import math


#Black and Scholes

class BlackScholes(object):
    def __init__(self,type,S0,K,r,sigma,T):
        self._S0 = S0
        self._K = K
        self._r = r
        self._sigma = sigma
        self._T = T
        self._type = type
        self._d1 = None
        self._d2 = None
        self._year_days = 365

    def calc_d1(self):
        self._d1 = (np.log(self._S0/self._K) + (self._r + self._sigma**2 / 2) * self._T)/(self._sigma * np.sqrt(self._T))

    def calc_d2(self):
        self._d2 = (np.log(self._S0 / self._K) + (self._r - self._sigma**2 / 2) * self._T)/(self._sigma * np.sqrt(self._T))

    def calc_value(self):
        if not self._d1:
            self.calc_d1()
        if not self._d2:
            self.calc_d2()
        if self._type=="C":
            return self._S0 * ss.norm.cdf(self._d1) - self._K * np.exp(-self._r * self._T) * ss.norm.cdf(self._d2)
        else:
            return self._K * np.exp(-self._r * self._T) * ss.norm.cdf(-self._d2) - self._S0 * ss.norm.cdf(-self._d1)

    def calc_delta(self):
        if not self._d1:
            self.calc_d1()

        if self._type=="C":
            return ss.norm.cdf(-self._d1)
        else:
            return ss.norm.cdf(-self._d1) - 1


    def calc_gamma(self):
        if not self._d1:
            self.calc_d1()

        gamma = np.exp(-self._d1**2/2)/(self._S0*self._sigma*np.sqrt(self._T)*np.sqrt(2*math.pi))

        return gamma

    def calc_vega(self):
        if not self._d1:
            self.calc_d1()
        vega = np.exp(-self._d1**2/2)*self._S0*np.sqrt(self._T)/(np.sqrt(2*math.pi)*100.0)
        return np.exp(-self._d1**2/2)*self._S0*np.sqrt(self._T)/(np.sqrt(2*math.pi)*100.0)

    def calc_theta(self,call_put):
        if not self._d1:
            self.calc_d1()

        if not self._d2:
            self.calc_d2()

        N_prime_d1 = np.exp(-self._d1**2/2)/np.sqrt(2*math.pi)

        if call_put == 'C':
            theta = (-((self._S0*self._sigma)*N_prime_d1)/(2*np.sqrt(self._T)) - self._r*self._K*np.exp(-self._r*self._T)*ss.norm.cdf(self._d2))/self._year_days
            return theta
        else:
            theta = (-((self._S0*self._sigma)*N_prime_d1)/(2*np.sqrt(self._T)) + self._r*self._K*np.exp(-self._r*self._T)*ss.norm.cdf(-self._d2))/self._year_days
            return theta

def main():
    S0 = 1520.0
    K = 1520.0
    r=0.05
    vol = 0.11
    T = 0.083 #a month

    print("S0\tstock price at time 0: ", S0)
    print("K\tstrike price: ", K)
    print("r\tcontinuously compounded risk-free rate: ", r)
    print("vol\tvolatility of the stock price per year: ", vol)
    print("T\ttime to maturity in trading years: ", T)

    c_BS = BlackScholes('C',S0, K, r, vol, T)

    print("Call Option:")
    print("Black-Scholes price: ", c_BS.calc_value())
    print("Black-Scholes delta: ", c_BS.calc_delta())
    print("Black-Scholes gamma: ", c_BS.calc_gamma())
    print("Black-Scholes vega: ", c_BS.calc_vega())
    print("Black-Scholes theta: ", c_BS.calc_theta('C'))

    p_BS = BlackScholes('P',S0, K, r, vol, T)

    print("Put Option:")
    print("Black-Scholes price: ", p_BS.calc_value())
    print("Black-Scholes delta: ", p_BS.calc_delta())
    print("Black-Scholes gamma: ", p_BS.calc_gamma())
    print("Black-Scholes vega: ", p_BS.calc_vega())
    print("Black-Scholes theta: ", p_BS.calc_theta('P'))

    print("end")

if __name__ == '__main__':
    main()