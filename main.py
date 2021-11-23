from olympus import Olympus

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