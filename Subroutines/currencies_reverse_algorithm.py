def diffCurrencies(x):
    currencies = ['baht','dollar','euro','koruna','lira','rand','rupee','yen']
    return currencies[x]

for i in range(7,-1,-1):
    print(diffCurrencies(i))
