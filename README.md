# Do_Manipulated_Matching_Algorithmes_Exist-

A statistical study on league of legends' matching algorithms. 

Despite the official statement which is denying the existence of any matchmaking manipulation system, such as placing players on a 'loser's team' after a win streak, many players remains skeptical.

Therefore, this study investigates whether such a system exists.

Specially, I'll analyse the question, "If a player is on a winning streak, is there matchmaking still fair?"

Study plan: 
  1. Data Collection
     Gather match history data using the official Riot API, focusing on solo queue ranked games.
  
  2. Players Classification

     Devide players into two groupes based on their recent match history.

       Groupe A: Players currently on a winning streak

       Groupe B: Players not on a winning streak
  
  4. Skill Proxy(Tier Based MMR Approximation)

     Since Riot does not publicly disclose exact MMR of each users, we will use the visible rank tiers e.g Platinum, Emerald, Diamond as a proxy for players skill level.

  6. Troll Indicators

     Additional features such as low KDA, irregular builds, AFK behavior, or excessive deaths will be used to detect 'troll' behavior in teammates.

  8. Fair Matchmaking Hypothesis

     If the matchmaking system is fair, the players should have approximately equal win probabilities regardless of streak status.

     Thus, over a large samples, their nmbers of wins in 20 games should follow a binomial distribution, and normal distribution which is derived from binomial distribution.

     Binomial(n = 20, p = 0.5)

     N(mu = 10, sigma^2 = 5)

  10. Statistical Testing

    Analyse the histogram of win counts for both groupes. If players on winning streaks show statistically significant skew, e.g lower win rates, more trolls in their teams, this could suggest matchmaking manipulation.


Packages: 
