from workshop import get_price, MA, RSI
from account import Account

data = get_price(2330, 3008, 2317)


MA(2330, 5)
RSI(2330, 5)
RSI(2330, 15)


a = Account()

counter_hold = 0

pre2330_open = 0

for date, row in data.iterrows():
    print('-'*10, date, '-'*10)
    a.handle_order(row)

    
    if a.is_empty():
        # a.buy(2330)
        pass

    else: # is not empty
        # a.sell()
        pass
    pre_open = row[2330, 'open']

    print('-'*13, 'end', '-'*13,'\n')


