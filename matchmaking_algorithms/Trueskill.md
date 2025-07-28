# Trueskill Algorithm. Can new algorith replace ELO Rating?

Trueskill algorithm additionally consider the standard deviation of each player(or team)'s performance. 

For example, 

![ELO](./images/elo.png)

This is the example of classical rating algorithms image. They don't consider about their dev of performances.

![Trueskill](./images/trueskill.png)

And this is the image of what trueskill algorithm calculate. 

As considering the dev of performances of each team, that algorithm can calculate each team's expected winning rate more precisely.

I exampled two teams, which have elo rating 800 and 1000, and the expected rate for the weaker was 24%. However if the two teams have huge deviations, the weaker's rate became bigger.

### Basic Formulas of Trueskill Algorithmes(for simplest case; 1:1)

$$\mu_{winner} = \mu_{winner, prior} + \frac{\sigma^2}c\cdot v(\frac{(\mu_{winner, prior}-\mu_{loser, prior})}c\cdot\frac{\epsilon}c)$$

$$\mu_{loser} = \mu_{loser, prior} - \frac{\sigma^2}{c} \cdot v\left( \frac{\mu_{winner, prior} - \mu_{loser, prior}}{c} \cdot \frac{\epsilon}{c} \right)$$

$$\sigma^2_{winner} = \sigma^2_{winner, prior} \cdot \left[ 1 - \frac{\sigma^2_{winner, prior}}{c^2} \cdot w \left( \frac{\mu_{winner, prior} - \mu_{loser, prior}}{c} \cdot \frac{\epsilon}{c} \right) \right]$$

$$\sigma^2_{\text{loser}} = \sigma^2_{\text{loser, prior}} \cdot \left[ 1 - \frac{\sigma^2_{\text{loser, prior}}}{c^2} \cdot w \left( \frac{\mu_{\text{winner, prior}} - \mu_{\text{loser, prior}}}{c} \cdot \frac{\epsilon}{c} \right) \right]$$

$$ c^2 = 2\beta^2 + \sigma^2_{winner} + \sigma^2_{loser}$$