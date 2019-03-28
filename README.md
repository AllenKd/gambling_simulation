# Gambling Simulation

To simulate gambling behavior based on win response ratio and player strategy, 
you can simulate players to gambling with a banker, each player have it's own strategy
based on strategy provider.

## Strategy Provider

Players can design strategies to battle with the banker, the strategy be defined as a 
dataframe, players bet based on 'current_put' field, which gives the players how 
much the players should bet if it lose for x runs continuously.

### linear response

The concept of this strategy is focus on the result of current, 
it calculate how much of bet for this run  can cover past lost, and 
the result will be the same as win for each run with minimum bet.

### fibonacci base

As the name implies, the bet will increasing along with continuous lose, based on 
fibonacci series.

### foo double

Put double bet of last run if lose, otherwise put minimum bet.

## TODO

- [ ] Dockerize
- [x] Add strategy based on Kelly formula
- [ ] Make some plot to display gambling pattern
- [ ] Use real data from NBA

