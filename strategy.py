from itertools import accumulate, repeat
from typing import Callable, Iterable, List, NamedTuple, Tuple, TypeVar, Union, Any
import logging


logger = logging.getLogger(__name__)


class StrategyResult(NamedTuple):
    roi: float
    balance: List[Any]


T = TypeVar('T')


def spreadsheet(*,
                initial: T,
                inputs: Iterable[Union[float, Tuple[float, ...]]],
                transactions: Callable[..., T]) -> List[T]:
    # accumulate results
    result = accumulate(inputs, func=transactions, initial=initial)
    # return
    return list(result)


def staking(principal: float, price: float, *,
            rebase_rate: float, period_len: int = 5, rebase_per_day: int = 3) -> StrategyResult:
    # types
    class Row(NamedTuple):
        balance: float
        value: float
    # some constant
    period = period_len * rebase_per_day
    multiple = (1+rebase_rate/100)

    # what happen over one period
    def transactions(begin: Row, price: float) -> Row:
        end_balance = begin.balance*multiple
        end_value = end_balance*price
        return Row(end_balance, end_value)
    # constructure the spreadsheet
    balance = spreadsheet(
        initial=Row(principal/price, principal),
        transactions=transactions,
        inputs=repeat(price, period))
    # metrics
    roi = multiple**period - 1
    # bundle as result
    return StrategyResult(roi=roi, balance=balance)


def bonding_with_restake(principal: float, price: float, *,
                         rebase_rate: float, bond_discount: float,
                         period_len: int = 5, rebase_per_day: int = 3, fee: float = 0.2) -> StrategyResult:
    # types
    class Row(NamedTuple):
        bonded: float
        staked: float
        value: float
    # some constant
    period = period_len * rebase_per_day
    multiple = (1+rebase_rate/100)
    bond_price = price / (1+bond_discount/100)
    bonded = principal/bond_price
    period_vest = bonded / period

    # what happen over one period
    def transactions(begin: Row, data: Tuple[float, float]) -> Row:
        price, period_vest = data
        end_bonded = begin.bonded - period_vest
        # end_staked = begin.staked*multiple + period_vest
        end_staked = (begin.staked+period_vest-fee/price)*multiple
        end_balance = end_bonded + end_staked
        end_value = end_balance * price - fee
        return Row(end_bonded, end_staked, end_value)
    # constructure the spreadsheet
    balance = spreadsheet(
        initial=Row(bonded, 0, bonded*price),
        transactions=transactions,
        inputs=repeat((price, period_vest), period))
    # metrics
    roi = balance[-1].value/principal-1
    # bundle as result
    return StrategyResult(roi=roi, balance=balance)


def demo():
    from rich import print
    result = staking(10000, 8700, rebase_rate=0.9695)
    print(result)
    result = bonding_with_restake(
        10000, 8700, rebase_rate=0.9695, bond_discount=6, fee=0.2)
    print(result)


if __name__ == '__main__':
    demo()