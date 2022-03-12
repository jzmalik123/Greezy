import datetime as dt
import time
import cbpro

from theDic import decisions, prediction

################USER SETTINGS########################################
key = 'cf0941b45a3bfa6ff7a25071715c6b95'
secret = 'O/u2pgXexpG7d75/KH8eAeaviE+193JsEMzBvenM0yEzao2xi5AW0l/JfNhpNLhuwVAxo6HhbNzEkfXKMsinag=='
passphrase = '62mwus5144k'
fiat = 'EUR'
coins = ['EOS', 'BNT', 'ETH', 'XLM']
purchaseFund = 20  # percent
desiredGain = 1.005  # this is the minimum gain before considering a sell. 1.00 = 0%, gain 1.02 = 2% gain, 1.33 = 33% gain
desiredBuy = 0.005  # this is the minimum price percentage decrease before considering a buy 0.15 = 15%
stopLoss = None  # left for now
candles = [float(60), float(300), float(900), float(3600), float(21600), float(86400)]
for candle in candles:
    candle = candles[0]
########################################################
###### DEVELOPER SETTINGS ###########################


testing = True
language = 'english'
margin = '     '


def messages(i):
    if i == 'localTime':
        data = datetime = dt.datetime.now()

    elif i == 'introduction':
        data = (margin + margin + margin + margin + '|  GREEZY  ')
        print('\n', '\n', '\n')


    elif i == 'orderCount':
        data = ('buys:', buyCount, 'Sells:', sellCount)

    elif i == 'iteration':
        data = ('-----------', 'iteration: ', iteration)

    elif i == 'theSignal':
        data = ('  The signal to sell', decisions.size(), currency, '@', price, 'has been given.')

    else:
        if i == 'sellReceipt':
            for ii in tradeReceipt:
                trade, size, pair, side = float(ii['id']), float(ii['size']), float(ii['product_id']), float(ii['side'])
                type = ii['type']
                time = ii['created_at']
                volume = float((size * price))
                fees = volume * 0.005
                data = ('-----trade receipt---'
                        '\n', time, '\n', pair,
                        '\n', 'Type:', type, '\n', size, '@', price,
                        '\n', 'volume:', volume, '\n', 'fees', fees, '\n')
    return data


def cbProAuth():
    try:
        auth = cbpro.AuthenticatedClient(key, secret, passphrase)
        return auth
    except Exception as error:
        print('Error! cbProAuth():', error)


def account(iD):
    for account in auth.get_accounts():
        if account['currency'] == iD:
            return account['id']


def getFiatBalance():
    i = float(auth.get_account(account(fiat[:3]))['available'])
    return i


def getTotals():
    fiatBalance = getFiatBalance()
    total = fiatBalance
    for account in auth.get_accounts():

        try:

            coin = account['currency']
            currency = str(coin + '-' + fiat)
            owned = float(account['balance'])

            if owned > 0:

                time.sleep(.5)
                price = float(auth.get_product_ticker(product_id=(currency))['price'])
                value = owned * price
                total = total + value
                if coin in [fiat, 'USDC', 'SHIB', 'DOGE']:
                    continue
                else:
                    coins.append(coin)

                if testing == True:
                    print(margin, '>===<', coin, '>===<', 'Price:', price, fiat.lower(), 'Owned:', owned, ' Value:',
                          value, '>===<')
        except Exception as e:
            time.sleep(1)
            continue

    total = total
    return total


print(messages(i='introduction'))

auth = cbProAuth()
cash = getFiatBalance()
startingValue = getTotals()
startingValue = float(startingValue)
print('\n', margin, margin, 'startingPortfolio Value:', startingValue, '\n', margin, margin, fiat, 'balance:', cash)

iteration, buyCount, sellCount, stopCount, reupCount = [0, 0, 0, 0, 0]
coinn, coinCount = [0, len(coins)]
coinCount = coinCount - 1

candle = candles[0]

iteration = 1
while True:
    try:

        coin = str(coins[coinn])
        currency = str(coin + '-' + fiat)
        specificID = account(currency[:3])
        # print('\n', '------<', coin, '>-----')
        time.sleep(0.333)
        owned = float(auth.get_account(specificID)['available'])
        price = float(auth.get_product_ticker(product_id=(currency))['price'])
        value = owned * price

        time.sleep(1)

        funding = round((purchaseFund / 100) * cash, 2)
        fills = list(auth.get_fills(currency))

        virgin = (fills == [])
        if virgin:
            permission = 'cherryPop'
            print('buying', currency, 'for the first time...')
            receipt = auth.place_market_order(product_id=str(currency), side='buy', funds=str(funding))
            buyCount = buyCount + 1
            print('Trade Receipt:', receipt)
            time.sleep(3)
            fills = list(auth.get_fills(currency))

        fill = fills[0]
        fillPrice = float(fill['price'])
        lastSide = (fill['side'])

        print('\n', margin, 'lastTrade:', lastSide, '@', fillPrice, fiat,
              '\n', margin, '  currentPrice:', price,
              '\n', margin, '   owned:', owned,
              '\n', margin, '    value:', value)

        estimatedGain = round(owned * price - owned * fillPrice, 4)

        size = decisions.getSize(coin, owned)
        availableFunds = getFiatBalance()

        if lastSide == 'sell':
            targetPrice = fillPrice - (fillPrice * desiredBuy)
            # print(margin, '      targetPrice', targetPrice, fiat)
            if price < targetPrice:
                signal = prediction.coppockCurve(currency, auth)
                print(margin, ' signal:', signal)
                if signal:
                    if funding < availableFunds:
                        print(currency)
                        placeBuyOrder = auth.place_market_order(product_id=currency, side='buy', funds=funding)
                        buyReceipt = placeBuyOrder
                        print(buyReceipt)
        elif lastSide == 'buy':
            targetPrice = (fillPrice * desiredGain)
            theDifference = targetPrice - fillPrice
            if price > targetPrice:
                signal = prediction.coppockCurve(currency, auth)
                print(margin, margin, 'signal:', signal)
                if signal:
                    placeMarketSellOrder = auth.place_market_order(product_id=str(currency), side='sell',
                                                                   size=str(size))
                    tradeReceipt = placeMarketSellOrder
                    print(tradeReceipt)

        time.sleep(1.11)
        if coinn == coinCount:
            portfolioValue = float(getTotals())
            sessionEarnings = portfolioValue - float(startingValue)
            coinn = 0
            iteration = iteration + 1
            print('\n', '      starting portfolio value: ', startingValue, '\n', '      current portfolio value:',
                  portfolioValue, '\n', '      total session earnings:', sessionEarnings)
            time.sleep(3)

        coinn = coinn + 1
    except Exception as e:
        print('error encountered')
        time.sleep(3)
