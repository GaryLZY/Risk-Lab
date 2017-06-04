from scipy.stats import norm
from math import *


class PricingEngine:

    def option(self, stock_price, strike_price, risk_free_rate, term, volatility, dividend_yield=0,
               type_of_option='American', call=True):
        # Prices a call/put option using Black Scholes for different types of options (American/European)

        d1 = (log(float(stock_price) / strike_price) + ((risk_free_rate - dividend_yield) + volatility**2 / 2.0) * term)\
             / (volatility * sqrt(term))
        d2 = d1 - volatility * sqrt(term)
        # d3 = (log(float(stock_price) / strike_price) + 0.5 * volatility**2 * term) / (volatility * sqrt(term))
        d4 = (log(float(stock_price) / strike_price) - 0.5 * volatility ** 2 * term) / (volatility * sqrt(term))
        if type_of_option == 'European':
            if call is True:
                return stock_price * exp(-dividend_yield * term) * norm.cdf(d1) - \
                       strike_price * exp(-risk_free_rate * term) * norm.cdf(d2)
            else:
                return strike_price * exp(-risk_free_rate * term) * norm.cdf(-d2) - \
                       stock_price * exp(-dividend_yield * term) * norm.cdf(-d1)

        if type_of_option == 'American':
            if call is True:
                # Since the we assume the dividend yield to be continues issued we can just deduct it from the
                # continuous compounding interest risk-free rate. We know for non-dividend paying stocks the value of a
                # European call should be the same with the equivalent American as an investor should not exercise the
                # option earlier.
                return self.option(stock_price, strike_price, risk_free_rate, term, volatility, dividend_yield,
                                   'European', True)
            else:
                # According to the paper at http://aeconf.com/articles/may2007/aef080111.pdf (Proposition 4, page 9)
                # we have a closed form solution for American put options.
                # Here we generalize the result of the above paper by assuming a paying (continues) a dividend yield.
                return self.option(stock_price, strike_price * exp(risk_free_rate*term), risk_free_rate, term,
                                   volatility, dividend_yield, 'European', False) * norm.cdf(-d4) + \
                       max(strike_price - stock_price, self.option(stock_price, strike_price * exp(risk_free_rate*term),
                                                                   risk_free_rate, term, volatility, dividend_yield,
                                                                   'European', False)) * norm.cdf(-d4)

    def imp_vol(self):
        # Returns the implied volatility of an option
        pass

    def bond(self):
        # Prices a bond
        pass

    def default_prob(self):
        # Calculate default probabilities
        pass

    def cds(self):
        # Price credit default swaps
        pass

