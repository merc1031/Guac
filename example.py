from guac import *

@monadic(ListMonad)
def make_change(amount_still_owed, possible_coins):
    change = []
    
    # Keep adding coins while we owe them money and there are still coins.
    while amount_still_owed > 0 and possible_coins:
    
        # "Nondeterministically" choose whether to give another coin of this value.
        # Aka, try both branches, and return both results.
        give_min_coin = yield [True, False]
        
        if give_min_coin:
            # Give coin
            min_coin = possible_coins[0]
            change.append(min_coin)
            amount_still_owed -= min_coin
        else:
            # Never give this coin value again (in this branch!)
            del possible_coins[0]
            
    # Did we charge them the right amount?
    yield guard(amount_still_owed == 0)
    
    # Lift the result back into the monad.
    yield lift(change)

print(make_change(27, [1, 5, 10, 25]))

