import datetime as dt
import time
import cbpro

from theDic import decisions, prediction
from app import app, db, User, Strategy, cbProAuth, CBCredentials

################USER SETTINGS########################################

candles = [float(86400), float(21600), float(3600), float(900), float(300), float(60)]
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


print(messages(i='introduction'))

iteration, buyCount, sellCount, stopCount, reupCount = [0, 0, 0, 0, 0]

all_users = User.query.all()

for user in all_users:
    try:
        auth = cbProAuth(user)
        cash = user.getFiatBalance()
        startingValue = user.getTotals()
        startingValue = float(startingValue)
        fiat = user.getFiatName()
        coins = user.coins
        candle = candles[user.strategy.aggressiveness-1]
        purchaseFund = 20  # percent

        desiredGain = 1+(user.strategy.minimum_gains / float(100.00)) # this is the minimum gain before considering a sell. 1.00 = 0%, gain 1.02 = 2% gain, 1.33 = 33% gain
        desiredBuy = desiredGain - 1  # this is the minimum price percentage decrease before considering a buy 0.15 = 15%
        stopLoss = None  # left for now
        print('\n', margin, margin, 'startingPortfolio Value:', startingValue, '\n', margin, margin, fiat, 'balance:', cash)

        for coin in coins:
            try:
                currency = str(coin + '-' + fiat)
                specificID = user.getAccountID(currency[:3])
                # print('\n', '------<', coin, '>-----')
                owned = float(auth.get_account(specificID)['available'])
                price = float(auth.get_product_ticker(product_id=(currency))['price'])
                value = owned * price

                funding = round((purchaseFund / 100) * cash, 2)
                fills = list(auth.get_fills(currency))

                virgin = (fills == [])
                if virgin:
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
                availableFunds = user.getFiatBalance()

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
                if coin == coins[-1]:
                    portfolioValue = float(user.getTotals())
                    sessionEarnings = portfolioValue - float(startingValue)
                    user.profit = user.profit + sessionEarnings
                    db.session.add(user)
                    db.session.commit()
                    iteration = iteration + 1
                    print('\n', '      starting portfolio value: ', startingValue, '\n', '      current portfolio value:',
                          portfolioValue, '\n', '      total session earnings:', sessionEarnings)
                    time.sleep(3)
            except Exception as e:
                print('Error! In Bot:', e)
                continue
    except Exception as e:
        print("Error", e)
        continue
