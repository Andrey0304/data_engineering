import pandas as pd
import numpy as np
import string
import random
from init_logger import log


@log('WARNING')
def create_dividends(user_id_list: list,
                     fin_instrument: pd.DataFrame,
                     N: int)->pd.DataFrame:
    
    dividends = pd.DataFrame(columns=[
        'user_id',
        'bank_id',
        'sec_id',
        'currency',
        'date',
        'description',
        'amount'
        ])

    dividends.user_id = random.sample(user_id_list, N)
    
    stocks = fin_instrument[fin_instrument['asset_category'] == 'Stocks']
    random_index = [random.choice(stocks.index) for _ in range(N)]
    
    dividends.bank_id = [stocks.bank_id[i] for i in random_index]
    dividends.sec_id = [stocks.security_id[i] for i in random_index]
    
    dividends.description = [random.choice(['Cash Dividend', 'Expire Dividend Right', 'Payment in Lieu of Dividend'])
                             for _ in range(N)]
    dividends.currency = [random.choice(['USD', 'AUD', 'GBP', 'EUR', 'NZD', 'CAD', 'CHF'])
                          for _ in range(N)]
    dividends.date = [(pd.to_datetime('2021-01-01') + pd.to_timedelta(random.randint(1,300), unit='d')).date()
                      for _ in range(N)]
    dividends.amount = random.sample(range(-100, 200), N)

    return dividends


@log('WARNING')
def create_interests(datafrm_for_copying: pd.DataFrame,
                     fin_instrument: pd.DataFrame,
                     user_id_list: tuple,
                     N: int)->pd.DataFrame:
    
    interest = datafrm_for_copying
    interest.user_id = random.sample(user_id_list, N)

    bonds = fin_instrument[fin_instrument['asset_category'] == 'Bonds']
    random_index = [random.choice(bonds.index) for _ in range(N)]
    
    interest.bank_id = [bonds.bank_id[i] for i in random_index]
    interest.sec_id = [bonds.security_id[i] for i in random_index]
    
    interest.description = [random.choice(['Purchase Accrued Interest',
                                           'Debit Interest',
                                           'Net Short Stock Interest',
                                           'Sold Accrued Interest',
                                           'Sold Accrued Interest',
                                           'Credit Interest',
                                           'Bond Coupon Payment'])
                            for _ in range(N)]
    return interest


@log('WARNING')
def create_withholding_tax(datafrm_for_copying:pd.DataFrame)->pd.DataFrame:
    
    witholding_tax = datafrm_for_copying
    witholding_tax.amount = random.sample(range(-100, 0), datafrm_for_copying.shape[0])
    
    return witholding_tax


@log('WARNING')
def create_change_in_dividend_accruals(datafrm_for_copying:pd.DataFrame)->pd.DataFrame:
    
    change_in_dividend_accruals = datafrm_for_copying
    change_in_dividend_accruals.drop(columns=['amount', 'currency', 'description'], inplace=True)
    change_in_dividend_accruals.rename(columns={'date': 'pay_date'}, inplace=True)
    change_in_dividend_accruals['quantity'] = random.sample(range(100, 10000, 100), datafrm_for_copying.shape[0])
    change_in_dividend_accruals['ex_date'] = change_in_dividend_accruals.pay_date.apply(
        lambda date: date - pd.to_timedelta(random.randint(1,20), unit='d')
        )

    return change_in_dividend_accruals


@log('WARNING')
def create_trades(fin_instrument: pd.DataFrame,
                user_id_list: list,
                users: pd.DataFrame,
                code_list: list,
                N: int)->pd.DataFrame:
    
    trades = pd.DataFrame(columns=['user_id',
                                    'bank_id',
                                    'conn_id',
                                    'currency',
                                    'symbol',
                                    'datetime',
                                    'quantity',
                                    't_price',
                                    'comm_fee',
                                    'code'])

    random_index = [random.choice(fin_instrument.index) for _ in range(N)]
    
    trades.bank_id = [fin_instrument.bank_id[i] for i in random_index]
    trades.conn_id = [fin_instrument.conn_id[i] for i in random_index]
    trades.symbol = [fin_instrument.symbol[i] for i in random_index]

    trades.user_id = [random.choice(user_id_list) for _ in range(N)]
    trades.currency = [random.choice(['USD', 'AUD', 'GBP', 'EUR', 'NZD', 'CAD', 'CHF'])
                       for _ in range(N)]
    trades.datetime = trades.user_id.apply(
        lambda id: users[users.id == id].registration.item() + pd.to_timedelta(random.randint(1, 5000), unit='h')
        )
    trades.quantity = random.sample(range(1000, 500_000, 1000), N)
    trades.t_price = random.sample(np.arange(1.5, 200, 0.5).tolist(), N)
    trades.comm_fee = random.sample(np.arange(-100, 0, 0.2).tolist(), N)
    trades.code = [random.choice(code_list) for _ in range(N)]

    return trades
