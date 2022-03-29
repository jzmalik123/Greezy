import numpy, time





class prediction():

    def coppockCurve(currency,auth):


                hd = auth.get_product_historic_rates(currency, granularity=60)
                p = numpy.squeeze(numpy.asarray(numpy.matrix(hd)[:, 4]))
                ROC11 = numpy.zeros(13)
                ROC14 = numpy.zeros(13)
                ROCSUM = numpy.zeros(13)
                for ii in range(0, 13):
                    ROC11[ii] = (100 * (p[ii] - p[ii + 11]) / float(p[ii + 11]))
                    ROC14[ii] = (100 * (p[ii] - p[ii + 14]) / float(p[ii + 14]))
                    ROCSUM[ii] = (ROC11[ii] + ROC14[ii])
                    coppock = numpy.zeros(4)
                for ll in range(0, 4):
                    coppock[ll] = (((1 * ROCSUM[ll + 9]) + (2 * ROCSUM[ll + 8]) + (3 * ROCSUM[ll + 7]) \
                                    + (4 * ROCSUM[ll + 6]) + (5 * ROCSUM[ll + 5]) + (6 * ROCSUM[ll + 4]) \
                                    + (7 * ROCSUM[ll + 3]) + (8 * ROCSUM[ll + 2]) + (9 * ROCSUM[ll + 1]) \
                                    + (10 * ROCSUM[ll])) / float(55))
                coppockD1 = numpy.zeros(3)
                for mm in range(3): coppockD1[mm] = coppock[mm] - coppock[mm + 1]
                outputA = (coppockD1[0] / abs(coppockD1[0]))
                outputB = (coppockD1[1] / abs(coppockD1[1]))
                if outputA == 1.0 and outputB == -1.0:
                    signal = True
                else:
                    signal = False

                return signal



# --------------------------------------------------------#



class decisions():
    def tradeApproval(currency):
        fill = coinbasePro.filledOrders(currency)

        if str('No trade history') in fill:

            lastSide = 'sell'
            fillPrice = 100000000000
            i = [lastSide,fillPrice]
            return i

        else:

            i = [fill['side'], float(fill['price'])]
            return i


    def buyApproval(funding, currency):

        for i in cbProCurrencies():
            if currency == i['id']:
                minimumSize = float(i['min_market_funds'])
                fundingApproval = float(round((funding * 0.10), 5))
                if funding > minimumSize:
                    approval = str('buy')
                elif funding < minimumSize:
                    approval = 'funding does not meet minimum size'
                else:
                    approval = 'hold'
                i = [approval,fundingApproval]
                return i


    def getSize(coin,owned):


            if coin == 'BTC': size = round((owned - 0.000001), 8)
            if coin == 'ENJ': size = round((owned - 0.001), 3)

            if coin == 'BAL': size = round((owned - 0.001), 3)
            if coin == 'BCH': size = round((owned - 0.0001), 8)
            if coin == 'BNT': size = round((owned - 0.01), 2)
            if coin == 'EOS': size = round((owned - 0.1), 1)
            if coin == 'ETH': size = round((owned - 0.0001), 8)
            if coin == 'ETC': size = round((owned - 0.0001), 8)
            if coin == 'FIL': size = round((owned - 0.001), 3)
            if coin == 'GRT': size = round((owned - 1), 3)
            if coin == 'KNC': size = round((owned - 0.1), 1)
            if coin == 'LRC': size = round((owned - 0.0001), 6)
            if coin == 'LTC': size = round((owned - 0.3), 1)
            if coin == 'MKR': size = round((owned - 0.0001), 4)
            if coin == 'NMR': size = round((owned - 0.001), 3)
            if coin == 'OXT': size = round((owned - 1), 0)
            if coin == 'OMG': size = round((owned - 0.1), 1)
            if coin == 'REP': size = round((owned - 0.00001), 8)
            if coin == 'REN': size = round((owned - 0.00001), 8)
            if coin == 'UMA': size = round((owned - 0.001), 3)
            if coin == 'XLM': size = round((owned - 1), 0)
            if coin == 'XRP': size = round((owned - 0.00001), 8)
            if coin == 'XTZ': size = round((owned - 1), 2)
            if coin == 'UNI': size = round((owned - 0.1), 3)
            if coin == 'YFI': size = round((owned - 0.00001), 8)
            if coin == 'ZEC': size = round((owned - 0.01), 2)
            if coin == 'ZRX': size = round((owned - 1), 2)
            if coin == 'USDC': size = round((owned - 1), 2)

            return size

    def sellApproval(holding, currency):

        for i in cbProCurrencies():
            if currency == i['id']:
                minimumSize = float(i['min_market_funds'])

                fundingApproval = float(round((holding * 1), 5))
                if holding > minimumSize:
                    approval = str('sell')
                elif holding < minimumSize:
                    approval = 'holdings do not meet minimum sell size'
                else:
                    approval = 'hold'
                i = [approval,fundingApproval]
                return i


# --------------------------------------------------------#


class userOperations():

    def manualMoney():
        while True:
            userInput = input('\n' + '|A.Balances | B.PlaceOrder |C.Transfer D.Exit|' + '\n')

            if userInput in ['a', 'A']:
                holdings = coinbasePro.allAvailableBalances()
                print(holdings)

            elif userInput in ['b', 'B']:
                side = input('buy or sell? ').lower()
                if side == 'buy':
                    currency = input('what currency?  ').upper()

                    for i in coinbasePro.currencyPairDetails():
                        l = []
                        if currency == i[0]:
                            quoteCur = i[1]
                            l.append(quoteCur)
                            currencyPair = str(currency + '-' + quoteCur)
                            try:
                                funding = float(coinbasePro.availableBalance(quoteCur))
                            except:
                                time.sleep(2)
                                continue
                            if funding > 0:
                                price = float(auth.get_product_ticker(product_id=(currencyPair))['price'])
                                print('available', quoteCur, ':', funding, '|', currency, 'price:', price)
                    quoteCur = input('Input a quote currency from the list above: ').upper()
                    funding = input('how much do you want to spend?')
                    funding = float(funding)
                    value = float(funding / price)
                    quoteCur = str(quoteCur)
                    currencyPair = str(currency + '-' + quoteCur)
                    print('trading:', funding, quoteCur, 'for', value, currency)
                    print('---Trade Reciept---')
                    print(auth.place_market_order(product_id=str(currencyPair), side='buy', funds=str(funding)))

                if side == 'sell':
                    currency = input('what currency?  ').upper()
                    available = float(coinbasePro.availableBalance(currency))
                    print('available', currency, ':', available)
                    available = float(input('how much do you want to sell? '))
                    print('\n' + '------------------------')
                    for i in coinbasePro.currencyPairDetails():
                        l = []
                        if currency == i[0]:
                            quoteCur = i[1]
                            l.append(quoteCur)
                            currencyPair = str(currency + '-' + quoteCur)
                            price = float(auth.get_product_ticker(product_id=(currencyPair))['price'])
                            value = float(price * available)
                            print(quoteCur, 'sell @', price, 'for', value)
                    quoteCur = input('Input a quote currency from the list above: ').upper()
                    quoteCur = str(quoteCur)
                    currencyPair = str(currency + '-' + quoteCur)
                    print('trading:', currencyPairs)
                    print('---Trade Reciept---')
                    print(auth.place_market_order(product_id=str(currencyPairs), side='sell', size=str(available)))


            elif userInput in ['D', 'd']:
                break
        else:
            print('try again')