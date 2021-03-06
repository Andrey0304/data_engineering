-- withdraw those shares that have been bought daily more than 300,000 times in the last 3 days.
select symbol,
       sum(sum)
--        count(symbol) as count_symbol
from (select trades.symbol,
             date(trades.pay_date) as pay_day,
             sum(quantity)
      from trades
               inner join financial_instrument fi
                          on trades.bank_id = fi.bank_id and
                             trades.conn_id = fi.conn_id
      where asset_category = 'Stocks'
        and quantity > 0
        and pay_date > NOW() - INTERVAL '3 DAY'
      group by trades.symbol,
               pay_day
      having sum(quantity) >= 300000) as SUB
group by symbol
having count(symbol)=3;


with table1 as (
    select date(trades.pay_date) as pay_day,
           trades.symbol,
           sum(quantity)
    from trades
             inner join financial_instrument fi
                        on trades.bank_id = fi.bank_id and
                           trades.conn_id = fi.conn_id
    where asset_category = 'Stocks'
      and quantity > 0
    group by pay_day,
             trades.symbol
)
SELECT *
FROM (
         select pay_day,
                symbol,
                sum,
                rank() over (partition by pay_day order by sum desc)
         from table1
    ) a
WHERE a.rank = 1;