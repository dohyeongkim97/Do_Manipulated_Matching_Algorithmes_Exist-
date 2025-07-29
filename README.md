# Do_Manipulated_Matching_Algorithmes_Exist-

A statistical study on league of legends' matching algorithms. 

Despite the official statement which is denying the existence of any matchmaking manipulation system, such as placing players on a 'loser's team' after a win streak, many players remains skeptical.

Therefore, this study investigates whether such a system exists.

Specially, I'll analyse the question, "If a player is on a winning streak, is there matchmaking still fair?"

Theory Basis. H0: There are no manipulated matching algorithmes.
<s>
Thus, Always the expected winning rates are 0.5.
</s>
If a player placed on higher tier as a result of win streaks, his winning rates will naturally fall cause of his skill level.

Match data will be collected upon platinum tier.

experiment plan: 

###  METHOD I. Normality test by number of wins and losses.

  1. Data Collection

     Gather match history data using the official Riot API, focusing on solo queue ranked games.
  
  3. Players Classification

     Devide players into two groupes based on their recent match history.

       Groupe A: Players currently on a winning streak

       Groupe B: Players not on a winning streak
  
  4. Skill Proxy(Tier Based MMR Approximation)

     Since Riot does not publicly disclose exact MMR of each users, we will use the visible rank tiers e.g Platinum, Emerald, Diamond as a proxy for players skill level.

  6. Troll Indicators

     Additional features such as low KDA, irregular builds, AFK behavior, or excessive deaths will be used to detect 'troll' behavior in teammates.

<s>
  7. Fair Matchmaking Hypothesis

  If the matchmaking system is fair, the players should have approximately equal win probabilities regardless of streak status.

  Thus, over a large samples, their nmbers of wins in 20 games should follow a binomial distribution, and normal distribution which is derived from binomial distribution.

  Binomial(n = 20, p = 0.5)

  N(mu = 10, sigma^2 = 5)

  8. Statistical Testing
     
      Analyse the histogram of win counts for both groupes. If players on winning streaks show statistically significant skew, e.g lower win rates, more trolls in their teams, this could suggest matchmaking manipulation.

      In particular, kurtosis (which is 3 for a normal distribution) will be a key metric. Anomalously high kurtosis (e.g., 5 or 6) would serve as strong evidence of manipulation.
</s>

if a players who has same tier with their skill, there winning rate after win streak/lose streak will changes naturally.

if there were no decline of win rates after winning streaks, then this probleme not has to be considered seriously.


###  METHOD II. Analyze whether, in matches involving players on a winning streak, there is a significant imbalance between the average tiers of the two teams.

  1. Collect game data to track users' winning and losing streaks, then compare the tier differences between allies and enemies for each user.

     Track each player's win/loss streak and compare the average tier (or MMR proxy) of their allies versus enemies.

     This method investigates whether players on winning streaks are systematically placed on weaker teams.

###  METHOD III. 

  1. Compare the expected win rates trends for each number of consecutive wins.

     Analyze how the expected win rate of the next game varies by the current streak length.

     Question: Does a winning or losing streak affect the likelihood of winning the next game?

     If matchmaking is unbiased and players are independent, the win rate should consistently hover around 0.5 mathematically(p==0.5).

     However, due to external factors such as fatigue or tilt, we hypothesize that players on extended streaks may show win rates in the mid-to-high 40% range, deviating from the theoretical 50%.

### METHOD IV.
  1. Using DTMC Model.
     
Packages: 




## Acknowledgement

This project includes portions of code from [renecotyfanboy's LeagueProject](https://github.com/renecotyfanboy/LeagueProject),  
which is licensed under the MIT License.


----------------------------------------
