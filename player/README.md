# Player

## Parameter

| Parameter | type | Description | Example |
| :---: | :---: | :--- | :---: |
| player_id | int | Player unique identification. | 1 |
| play_times | int | Times of the player to gamble at most, or finish if the player bankrupted. | 10 |
| strategy_provider | [StrategyProvider](StrategyProvider) | To provide a strategy table about bet for player reference. | N/A |
| combination | int | Game combination, if combination is n, you could got win if all of these games are win. | 1 |
| money | int | Initial money of the player. | 5000 |
| put_strategy | string | Strategy about the volume of bet to put, which obtain from [StrategyProvider](StrategyProvider) and usually a table. | linear_response |
| bet_strategy | string | Strategy about how to determine the result of the next game, currently is just some foo strategy, and the win ration technically is 1 / 2^combination, **but it will based on deep learning to improve win ratio**, and it's the key value of this project | random |
| bet_data | list | Predictions of games, the size equal to play_times | [0, 1, 0, 1, 0, 1, 0, 1, 0, 1] |
   