from olympus import Olympus


ohm = Olympus(ohm_supply=1_000_000)

for day in range(1, 31):
    price = 500

    # someone do 1,1 (bonding)
    ohm.bond(ohm.market_cap(price)*0.02)

    # assume everybody 3,3 (staking)
    ohm.rebase(price)

    # status at the end of period
    ohm.dashboard(day, price)