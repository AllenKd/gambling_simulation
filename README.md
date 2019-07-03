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
  analyze            Make judgement about crawled data.
  crawl_data         Start crawler to get sports gambling data.
  create_db          Create DB.
  simulate_gambling  Simulate gambling.

```

To describe command and it's helping message:

```bash
$ python3 main.py simulate_gambling --help
Usage: main.py simulate_gambling [OPTIONS]

  Simulate gambling.

Options:
  -p, --num_of_player INTEGER     Number of player of each put strategy in the
                                  gambling  [default: 10]
  -bs, --bet_strategy [random|follow_last|keep_false|keep_true]
                                  Bet strategy of each player.  [default:
                                  random]
  -gt, --game_times INTEGER       Gambling times.  [default: 100]
  -im, --init_money INTEGER       Initial money of each player.  [default:
                                  10000]
  --help                          Show this message and exit.

```

## [Player](https://github.com/AllenKd/gambling_simulation/tree/feature/refine-readme/player)

An instance to gambling with the [Banker](https://github.com/AllenKd/gambling_simulation/tree/feature/refine-readme/banker)

## [Strategy Provider](https://github.com/AllenKd/gambling_simulation/tree/feature/refine-readme/player)

Provide [Player]() strategies to gambling.

## [Banker](https://github.com/AllenKd/gambling_simulation/tree/feature/refine-readme/banker)

An instance for [Player](https://github.com/AllenKd/gambling_simulation/tree/feature/refine-readme/player) battle with.

## [Simulator](https://github.com/AllenKd/gambling_simulation/tree/feature/refine-readme/simulator)

Create multiple [Player](https://github.com/AllenKd/gambling_simulation/tree/feature/refine-readme/player) 
instances and a [Banker](https://github.com/AllenKd/gambling_simulation/tree/feature/refine-readme/banker) 
to simulate gambling scenario.

## [Crawler](https://github.com/AllenKd/gambling_simulation/tree/feature/refine-readme/crawler)

Crawl real sports gambling data and store into [Database](https://github.com/AllenKd/gambling_simulation/tree/feature/refine-readme/database)

## [Analyzer](https://github.com/AllenKd/gambling_simulation/tree/feature/refine-readme/analyzer)

Make judgements about crawled data and summarize it.

## [Database](https://github.com/AllenKd/gambling_simulation/tree/feature/refine-readme/database)

Store all simulation and crawled data.
