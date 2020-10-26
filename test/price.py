from context import bellykit_workshop

from bellykit_workshop.workshop import Price

p = Price(2330, 3008)
p.MA(2330, 5)
p.RSI(2330, 9)
p.KD(2330, 9, 5, 5)
print(p.data)
