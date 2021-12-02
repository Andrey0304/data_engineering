import pandas as pd
import numpy as np
import string
import random
from init_logger import log


@log('WARNING')
def create_banks()->pd.DataFrame:
    banks = pd.DataFrame(columns=[
        'id',
        'name',
        'contact',
        'cooperation',
        ])
    banks.id = list(range(1,7))
    banks.name = (
        'Converse Bank',
        'Ameria Bank',
        'HSBC Bank Armenia',
        'ARARATBANK',
        'ID Bank',
        'UniBank'
        )
    banks.contact = (
        '(010) 511211',
        '(060) 616100',
        '(010) 561111',
        '(010) 542323',
        '(010) 593333',
        '(010) 595555'
        )
    banks.cooperation = pd.date_range(start='2021-01-01', end='2021-12-31', periods=6)

    return banks


@log('WARNING')
def create_users(N: int)->pd.DataFrame:
    
    users = pd.DataFrame(columns=[
        'name',
        'surname',
        'sex',
        'passport_no',
        'nationality',
        'date_of_birth',
        'phone',
        'registration'
        ])

    boy_names = ('Andrey', 'Artur', 'Aramayis', 'Karen', 'Hayk', 'Koryun', 'Eduard', 'Armen', 'Samvel', 'Arayik')
    girl_names = ('Lilit', 'Susanna', 'Maga', 'Meri', 'Elina', 'Ashkhen', 'Liza', 'Luiza', 'Marina', 'Emiliya')
    surnames = ('Manukyan', 'Hakobyan', 'Karapetyan', 'Sargsyan', 'Hunanyan', 'Sevlikyan', 'Soghomonyan',
                'Stepanyan', 'Avagyan', 'Arushanyan')

    users['name'] = [random.choice(boy_names + girl_names) for _ in range(N)]
    users['id'] = list(range(1, N+1))
    users['surname'] = [random.choice(surnames) for _ in range(N)]

    users['sex'] = ['M' if name in boy_names else 'F' for name in users['name'].values]

    users['passport_no'] = [f"{''.join(random.sample(string.ascii_uppercase, 2))}{code}"
                            for code in random.sample(range(10_000, 99_999), N)]
    users['phone'] = ["(+374){}-{}".format(str(number)[:2], str(number)[2:])
                      for number in random.sample(range(10_000_000, 99_999_999), N)]
    users['registration'] = pd.date_range(start='2021-01-01', end='2021-12-31', periods=N)

    users['date_of_birth'] = [(pd.to_datetime('1975-01-01') + pd.to_timedelta(random.randint(1,10000), unit='d')).date()
                              for _ in range(N)]
    users['nationality'] = [random.choice(['Armenian', 'Polish', 'Russian', 'Italian', 'English'])
                            for _ in range(N)]
    return users


@log('WARNING')
def create_codes(banks_id: list)->pd.DataFrame:

    codes = pd.DataFrame(columns=['bank_id', 'code', 'meaning'])

    codes.bank_id = [random.choice(banks_id) for _ in range(50)]
    codes.code = ['A', 'ADR', 'AEx', 'Adj', 'Al', 'Aw', 'B', 'Bo', 'C', 'CD',
       'CP', 'Ca', 'Co', 'Cx', 'ETF', 'Ep', 'Ex', 'FP', 'FPA', 'G', 'HC',
       'HFI', 'HFR', 'I', 'IA', 'INV', 'IPO', 'L', 'LD', 'LI', 'LT', 'Lo',
       'M', 'MEx', 'ML', 'MLG', 'MLL', 'MSG', 'MSL', 'O', 'P', 'PI', 'Po',
       'Pr', 'R', 'RED', 'RP', 'RPA', 'Re', 'Ri']
    codes.meaning = [
        'Assignment',
        'ADR Fee Accrual',
        'Automatic exercise for dividend-related recommendation.',
        'Adjustment',
        'Allocation',
        'Away Trade',
        'Automatic Buy-in',
        'Direct Borrow',
        'Closing Trade', 
        'Cash Delivery',
        'Complex Position', 
        'Cancelled', 
        'Corrected Trade',
        'Part or all of this transaction was a Crossing executed as dual agent by IB for two IB customers',
        'ETF Creation/Redemption', 
        'Resulted from an Expired Position',
        'Exercise',
        'IB acted as principal for the fractional share portion of this trade',
        'IB acted as principal for the fractional share portion and as agent for the whole share portion of this trade',
        'Trade in Guaranteed Account Segment',
        'Highest Cost tax basis election',
        'Investment Transferred to Hedge Fund',
        'Redemption from Hedge Fund', 
        'Internal Transfer',
        'This transaction was executed against an IB affiliate',
        'Investment Transfer from Investor',
        'This transaction was executed as part of an IPO in which IB was a member of the selling group and is classified as a Principal trade.',
        'Ordered by IB (Margin Violation)',
        'Adjusted by Loss Disallowed from Wash Sale',
        'Adjusted by Loss Disallowed from Wash Saleasasa',
        'Long Term P/L',
        'Direct Loan', 
        'Entered manually by IB',
        'Manual exercise for dividend-related recommendation.',
        'Maximize Losses tax basis election',
        'Maximize Long Term Gain tax basis election',
        'Maximize Long Term Loss tax basis election',
        'Maximize Short Term Gain tax basis election',
        'Maximize Short Term Loss tax basis election',
        'Opening Trade',
        'Partial Execution', 
        'Price Improvement',
        'Interest or Dividend Accrual Posting',
        'Part or all of this transaction was executed by the Exchange as a Crossing by IB against an IB affiliate and is therefore classified as a Principal and not an agency trade',
        'Dividend Reinvestment', 
        'Redemption to Investor',
        'IB acted as riskless principal for the fractional share portion of this trade',
        'IB acted as riskless principal for the fractional share portion and as agent for the whole share portion of this trade',
        'Interest or Dividend Accrual Reversal',
        'Reimbursement'
        ]

    return codes


@log('WARNING')
def create_currency_exchange()->pd.DataFrame:
    base_currency = {
        'USD': 1.,
        'AUD': 0.77135,
        'GBP': 1.4112,
        'EUR': 1.21212,
        'NZD': 0.71454,
        'CAD': 0.81,
        'CHF': 1.09,
        'JPY': 0.0090,
        'HKD': 0.13,
        'MXN': 0.050
    }
    currency_exchange = pd.DataFrame(
        columns = ['currency', 'coeff', 'datetime'])
    currency_exchange.currency = base_currency.keys()
    currency_exchange.coeff = base_currency.values()
    currency_exchange.datetime = [
        pd.to_datetime('2021-11-10 12:33:33') + pd.to_timedelta(random.randint(1,100), unit='m')
        for _ in range(10)
        ]
    return currency_exchange


@log('WARNING')
def create_financial_instrument(banks_id: list)->pd.DataFrame:

    fin_instrument = pd.DataFrame(columns=[
        'bank_id',
        'asset_category',
        'symbol',
        'description',
        'conn_id',
        'security_id',
        'multiplier',
        'type'
    ])
    fin_instrument.bank_id = [random.choice(banks_id) for _ in range(50)]
    fin_instrument.asset_category = [random.choice(['Stocks', 'Equity and Index Options','Futures', 'Options On Futures', 'Bonds'])
                                           for _ in range(50)]
    fin_instrument.symbol = ['GILD', 'IGY', 'RL', 'TAHO', 'CLU7',
                                   'CLX7', 'FDAX JUN 17', 'FDAX JUN 18', '4ADN7 P0765', 'LO4Q7 P4700',
                                   'LOX7 C4900', 'LOX7 C5100', 'LOX7 P4800',
                                   'ALRSRU 7 3/4 11/03/20 9320', 'ARCO 6 5/8 09/27/23',
                                   'ATI 5 7/8 08/15/23', 'BANBRA 5 7/8 01/26/22 2DN0', 'C 5.35 PERP',
                                   'CMC 4 7/8 05/15/23', 'COH 4 1/8 07/15/27', 'GT 4 7/8 03/15/27',
                                   'IM 5 08/10/22', 'PETBRA 8 3/4 05/23/26', 'RIG 3.8 10/15/22',
                                   'VALEBZ 6 1/4 08/10/26', '3436.T', '700', '968', '9888', 'ABN', 'AGS', 'BN', '6AH1', '6EM1',
                                   'S30YK1', 'ZB   JUN 21', 'ZN   JUN 21', 'ZN   SEP 21',
                                   'ADUJ1 P0760', 'OGJ1 P1700', 'WE1H1 C1215', 'WE1J1 P1190',
                                   'WE2J1 C1192', 'WE3H1 P1200', 'WE4G1 C1215',
                                   'BRASKM 6.45 02/03/24', 'DSPORT 5 3/8 08/15/26',
                                   'FLR 3 1/2 12/15/24', 'MUR 6 7/8 08/15/24', 'SIG 4.7 06/15/24']

    fin_instrument.description = ['GILEAD SCIENCES INC', 'INNOGY SE',
                                        'RALPH LAUREN CORP', 'TAHOE RESOURCES INC', 'CL SEP17', 'CL NOV17',
                                        'DAX 16JUN17', 'DAX 15JUN18', 'AUD 28JUL17 0.765 P',
                                        'CL 25AUG17 47.0 P', 'CL NOV17 49.0 C', 'CL NOV17 51.0 C',
                                        'CL NOV17 48.0 P', 'ALRSRU 7 3/4 11/03/20', 'ARCO 6 5/8 09/27/23',
                                        'ATI 5 7/8 08/15/23', 'BANBRA 5 7/8 01/26/22', 'C 5.35 PERP',
                                        'CMC 4 7/8 05/15/23', 'TPR 4 1/8 07/15/27', 'GT 4 7/8 03/15/27',
                                        'IM 5 08/10/22', 'PETBRA 8 3/4 05/23/26', 'RIG 3.8 10/15/22',
                                        'VALEBZ 6 1/4 08/10/26', 'SUMCO CORP', 'TENCENT HOLDINGS LTD', 'XINYI SOLAR HOLDINGS LTD',
                                        'BAIDU INC-CLASS A', 'ABN AMRO BANK NV-CVA', 'AGEAS',
                                        'DANONE', 'AUD 15MAR21', 'EUR 14JUN21',
                                        '30YSME 21MAY21', 'ZB 21JUN21', 'ZN 21JUN21', 'ZN 21SEP21',
                                        'AUD 09APR21 0.76 P', 'GC APR21 1700.0 P', 'EUR 03MAR21 1.215 C',
                                        'EUR 07APR21 1.19 P', 'EUR 14APR21 1.1925 C', 'EUR 17MAR21 1.2 P',
                                        'EUR 24FEB21 1.215 C',
                                        'BRASKM 6.45 02/03/24', 'DSPORT 5 3/8 08/15/26',
                                        'FLR 3 1/2 12/15/24', 'MUR 6 7/8 08/15/24', 'SIG 4.7 06/15/24']

    fin_instrument.conn_id = [''.join(random.sample(string.digits, 8)) for _ in range(50)]
    
    fin_instrument.security_id = fin_instrument['asset_category'].apply(
            lambda x:''.join(random.sample(string.digits + string.ascii_uppercase, 8)) if x in ('Bonds', 'Stocks') else None
            )
    fin_instrument.type = [random.choice(['COMMON', 'Corp', 'DUTCH CERT', 'ADR', 'ETF', 'RIGHT', 'PREFERENCE'])
                                for _ in range(50)]
    fin_instrument.multiplier = [random.choice([1, 25, 100, 1000, 100_000, 125_000]) for _ in range(50)]

    return fin_instrument


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


@log('WARNING')
def create_open_positions(datafrm_for_copy: pd.DataFrame)->pd.DataFrame:

    data_no_duplicates = datafrm_for_copy.drop_duplicates(
        subset=['bank_id', 'conn_id'])
    random_index = random.sample(data_no_duplicates.index.tolist(), 30)
    open_positions = datafrm_for_copy.iloc[random_index]
    open_positions.drop(columns=['code'], inplace=True)

    return open_positions

@log('WARNING')
def create_corporate_actions(banks_id: list)->pd.DataFrame:

    corporate_actions = pd.DataFrame(columns=['bank_id',
                                              'description',
                                              'report_date'])
    
    corporate_actions.bank_id = [random.choice(banks_id) for _ in range(4)]
    corporate_actions.report_date = [
        (pd.to_datetime('2021-01-01') + pd.to_timedelta(random.randint(1,300), unit='d')).date()
        for _ in range(4)
        ]
    corporate_actions.description = [
        'GE Spinoff WAB',
        'TAHO Cash and Stock Merger (Acquisition) PAAS',
        'RDSA Dividend Rights Issue RDSA.DIV',
        'RDSA.DIV Expire Dividend Right RDSA.DIV',
    ]
    return corporate_actions
