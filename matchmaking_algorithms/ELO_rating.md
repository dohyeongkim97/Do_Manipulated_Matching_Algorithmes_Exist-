# ELO rating system


An algorithms that calculate expected winning rates maded by a Statistician Elo Arpad Imre, who came from Hungary.

Maded for calculating classic mind-sports like chess or go. Therefore the algorithm has some traits which classic games have.

    1. A specific player do not meet every other players.

    2. Best fit in 1:1 situation

    3. No other features to consider, like cs or dpm in league.

It follows basic rules, the Stronger bets a lot, the Weaker bets a little.

For example, if GenG or T1 mets a team which plays in LLA league, GenG will earn just a bit points when they won, and will lose a lot when the contrary.

And the special parts: Easier to use and understand.

That's the reason many leagues or sports use ELO rating, for example, FIFA changes their ranking system to ELO ratings.

One of the best merits to use ELO rating is the intuitivitiness. 

Formula of ELO Rating System

$$ E_A = \frac{1}{1+10^{(R_B - R_A) / 400}}$$

ELO Rating after each game

$$ R'_A = R_A + K\cdot(S_A - E_A)$$

R' = New rating of A player

R_A = Original rating

K = weight of each game result(like K=20)

S_A = result of game(1 for winner, 0.5 for draw, 0 for lose)

E_A = expected winning rates

When A = 1000, B = 800, and A won, k = 20

R_A = 1000, 

$$E_A = \frac{1}{1+10^{-200/400}}, $$
$$10^{-0.5} \approx 3.1, $$
$$E_A = 1/4.1 = 0.24$$

But ELO Rating system has some critical flaw; the system fitted best when the game is 1:1, and it doesn't consider each teams deviation of power.

Therefore, there are so many transformations of ELO Rating system, representatively Glicko(I, II). 

And Trueskill algorithme is one of them, and RIOT Games tried to apply it in riot matching system ** important.