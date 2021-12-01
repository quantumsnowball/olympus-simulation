import math
import logging
from rich.logging import RichHandler
from rich import print


FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('Olympus')


class Olympus:
    def __init__(self, supply=100):
        self._index = 1.0
        self._treasury = supply * 1.0
        self._supply = supply

    #
    # routines
    #
    def __call__(self, epoch, *, price):
        self._epoch_price = price
        self._epoch_count = epoch
        return self

    def __enter__(self):
        self._epoch_bonded = 0
        self._epoch_minted = 0
        self._epoch_profit = 0
        self._epoch_rebased = 0
        return self

    def __exit__(self, type, value, traceback):
        # metrics
        roi = self._epoch_rebased / self._supply
        apy = (1+roi)**365 - 1
        runway = math.log(self._treasury/self.market_cap + 1) / math.log(1+roi)

        # settlement
        self._treasury += self._epoch_bonded
        self._supply += self._epoch_minted
        self._supply += self._epoch_rebased
        self._index *= 1 + roi
        #
        logger.info((
            f'REBASE: '
            f'Rewards=${self._epoch_rebased:,.0f}, '
            f'ROI={roi:,.2%}, '
            f'APY={apy:,.2%}, '
            f'Runway={runway:.4f}'
        ))
        # dashboard
        print((
            f'Epoch {self._epoch_count: >2} | '
            f'Treasury: ${self._treasury:,.0f}, '
            f'Supply: {self._supply:,.0f} OHM, '
            f'Price: ${self._epoch_price:,.2f}, '
            f'Index: {self._index:.4f}, '
            f'MCap: ${self._supply*self._epoch_price:,.0f}'
        ))

    #
    # metrics
    #
    @property
    def market_cap(self):
        return self._supply * self._epoch_price

    @property
    def treasury(self):
        return self._treasury

    #
    # operations
    #
    def bond(self, asset_value):
        # asset locked to treasury
        self._epoch_bonded += asset_value
        # $10,000 assets swaped for 10 ohm @ $1000
        self._epoch_minted += asset_value / self._epoch_price
        # profit is asset value net of $1 for each minted coin
        self._epoch_profit += asset_value - self._epoch_minted*1
        # increase supply by using all profit to mint new ohm to all stakers
        self._epoch_rebased += self._epoch_profit / self._epoch_price
        #
        logger.info((
            f'BOND: '
            f'Bonded=${self._epoch_bonded:,.0f}, '
            f'Profit=${self._epoch_profit:,.0f}, '
            f'Mint={self._epoch_minted:,.2f} OHM'
        ))


def main():
    ohm = Olympus(supply=1_000_000)

    N = 30
    for epoch in range(1, N+1):
        # market
        with ohm(epoch, price=100.0) as project:
            # simulate the bonding amount
            amount = (N-epoch+1)/N*0.25 * ohm.treasury
            # someone do 1,1 (bonding)
            project.bond(amount)

            # assume everybody 3,3 (staking)
            pass


if __name__ == '__main__':
    main()
