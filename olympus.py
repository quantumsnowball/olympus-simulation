import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Olympus:
    def __init__(self, ohm_supply=100):
        self.index = 1.0
        self.treasury = 0
        self.ohm_supply = ohm_supply
        self.profit = 0

    #
    # properties
    #
    def market_cap(self, price):
        return self.ohm_supply * price

    def dashboard(self, price):
        print((
            f'Treasury: ${self.treasury:,.0f}, '
            f'Supply: {self.ohm_supply:,.0f} OHM, '
            f'Price: ${price:,.2f}, '
            f'Index: {self.index:.2f}, '
            f'MCap: ${self.ohm_supply*price:,.0f}'
        ))

    #
    # operations
    #
    def mint(self, amount):
        self.ohm_supply += amount
        logging.info(f'MINT: amount={amount:,.2f}')

    def bond(self, assets):
        self.treasury += assets
        self.profit += assets - 1
        logging.info(f'BOND: profit={self.profit:,.0f}')

    def rebase(self, price):
        to_be_minted = self.profit / price
        self.profit = 0
        self.mint(to_be_minted)
