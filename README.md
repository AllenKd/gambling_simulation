# Gambling Simulation

A CLI to simulate gambling scenario,
go to each folder for detail description of each component.

## CLI

```bash
$ python3 main.py --help
Usage: main.py [OPTIONS] COMMAND1 [ARGS]... [COMMAND2 [ARGS]...]...

Options:
  --help  Show this message and exit.

Commands:
  run_simulator
```

To describe command and it's helping message:

```bash
$ python3 main.py run_simulator --help
Usage: main.py run_simulator [OPTIONS]

Options:
  -sd, --start_date TEXT   Start date of gambling, the format must follow the
                           pattern: YYYYmmDD, ex: 20190130.  [default:
                           20200425]
  -p, --principle INTEGER  Default principle unit of each gambler.  [default:
                           100]
  --help                   Show this message and exit.

```

## Simulator

To simulate gamblers based on each combination of *put_strategy*, *bet_strategy* and parameters, 
every gambler have different gamble strategy.

## Strategy

### Bet Strategy

A strategy to decide how to bet based on gambler's battle history and current gamble info, 
each *bet_strategy* contains a *put_strategy* to decide how much of bet should put in for this gamble.

#### Constant

Bet with first match of given gamble parameters for everyday. 

#### Confidence Base

Based on confidence index, the index obtain by members' vote, 
bet the game if the index over the given threshold.

#### Most Confidence

Extend from *Confidence Base*, bet the mose confidence one only. 

### Put Strategy

A strategy to decide how much of bet should put in for this gamble 
based on gamble's battle history, *bet_strategy* and other optional kwargs.

#### Constant

Put constant unit for each gamble no matter parameters and *bet_strategy*.

#### Foo Double

Double bet if lose, otherwise back to 1.

#### Linear Response

Calculate how much unit to put can resulting the response as linear since last time win the gamble.
