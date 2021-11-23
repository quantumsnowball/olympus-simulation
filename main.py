from olympus import Olympus


ohm = Olympus(ohm_supply=1_000_000)

for _ in range(30):
    price = 500
    

    ohm.bond(ohm.market_cap(price)*0.1)

    ohm.rebase(price)
    ohm.dashboard(price)