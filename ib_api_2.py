from ib_insync import *
import time
import sys
# util.startLoop()


# connect to API
def connect_ib(host, port, client_id):
    ib = IB()
    ib.connect(host, port, client_id)
    ib.reqMarketDataType(3)
    return ib


def get_option_contracts(ib, symbol, exchange, type):
    """
    :param symbol:
    :param exchange:
    :param type: "Index" or "Stock"
    :return:
    """
    symbol = symbol
    exchange = exchange
    if type == 'Index':
        contract = Index(symbol, exchange)
    elif type == 'Stock':
        contract = Stock(symbol, exchange)
    else:
        sys.exit('Invalid symbol type')

    # Fully qualify the given contracts in-place.
    # This will fill in the missing fields in the contract, especially the conId
    ib.qualifyContracts(contract)
    [ticker] = ib.reqTickers(contract)
    print(ticker.close)

    # get the option chain
    chains = ib.reqSecDefOptParams(contract.symbol, '', contract.secType, contract.conId)

    # convert to pandas dataframe:
    df = util.df(chains)

    # choose the target contract
    chain = next(c for c in chains if c.tradingClass == symbol and c.exchange == exchange)

    # full matrix of expirations x strikes
    strikes = chain.strikes
    expirations = sorted(exp for exp in chain.expirations)
    rights = ['P', 'C']

    contracts = [Option(symbol, expiration, strike, right, chain.exchange, chain.multiplier) for right in rights
                 for expiration in expirations for strike in strikes]

    contracts = ib.qualifyContracts(*contracts)
    print(len(contracts))

    return contracts


def get_option_price(ib, contracts):
    prices = []
    for contract in contracts:
        # request delayed market data to avoid permission problem
        # ib.reqMarketDataType(3)
        # start = time.time()
        [ticker] = ib.reqTickers(contract)
        # print(time.time() - start)
        data = str(ticker.time) + ' ' + contract.right + ' ' + str(contract.lastTradeDateOrContractMonth) + ' ' \
            + str(contract.strike) + ' ' + str(ticker.close)
        prices.append(data)
    return prices


if __name__ == "__main__":
    start = time.time()
    conn = connect_ib('127.0.0.1', '7497', '1')
    contracts = get_option_contracts(conn, 'VIX', 'CBOE', 'Index')
    prices = get_option_price(conn, contracts[:2])
    for price in prices:
        print(price)
    print(time.time() - start)
