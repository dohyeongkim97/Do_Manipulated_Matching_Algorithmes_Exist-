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

Study plan: 

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



Do_Manipulated_Matching_Algorithmes_Exist / 리그 오브 레전드 매칭 알고리즘에 대한 통계적 연구

공식적으로 라이엇 게임즈는 연승 이후 '패배 팀(loser's team)'에 일부러 배치하는 등의 매칭 조작 시스템이 존재하지 않는다고 발표했지만, 여전히 많은 유저들은 이에 대해 회의적인 반응을 보인다.

따라서 본 연구는 그러한 매칭 시스템이 실제로 존재하는지를 조사하는 것을 목적으로 한다.

특히, 다음의 질문을 중심으로 분석을 진행한다:
"연승 중인 플레이어의 경우, 매칭은 여전히 공정한가?"

이론적 기반
귀무가설(H₀): 매칭 알고리즘은 조작되어 있지 않다.
<s>
즉, 모든 플레이어의 기대 승률은 항상 0.5로 유지된다.
</s>

특정 플레이어가 연승의 결과로 높은 티어로 간다면(혹은 높은 레이팅의 유저들과 매치된다면) 그의 승률은 자연스럽게 떨어질 것.

연구에서는 플래티넘 티어 이상의 매치 데이터를 수집 대상으로 삼는다.

연구 계획

방법론 I. 승/패 수에 대한 정규성 검정

데이터 수집

공식 Riot API를 활용해 솔로 랭크 게임의 전적 데이터를 수집한다.

플레이어 분류
최근 전적을 기준으로 플레이어를 다음 두 그룹으로 나눈다:

그룹 A: 현재 연승 중인 플레이어

그룹 B: 연승 상태가 아닌 플레이어

실력 추정치 (티어 기반 MMR 근사)

라이엇이 실제 MMR을 공개하지 않기 때문에, 플래티넘, 에메랄드, 다이아몬드 등의 공식 티어를 실력의 근사치로 사용한다.

트롤 지표

이상치 KDA, 비정상적인 아이템 빌드, 게임 도중 이탈(AFK), 과도한 데스 등은 팀 내 '트롤링' 행동을 나타내는 지표로 활용한다.

<s>
공정 매칭 가설

매칭 시스템이 공정하다면, 연승 여부와 무관하게 플레이어는 동등한 승률을 가져야 한다.

즉, 충분한 표본에서 20판 중 승리 횟수는 다음과 같은 분포를 따라야 한다:

Binomial(n = 20, p = 0.5), N(mu = 10, sigma^2 = 5)

통계적 검정

각 그룹의 승수 분포를 히스토그램과 정규성검정으로 분석한다.

연승 중인 그룹에서 승률이 비정상적으로 낮거나, 트롤 팀원이 유의하게 많다는 결과가 도출된다면, 이는 매칭 조작 가능성을 시사할 수 있다.

특히, **첨도(kurtosis)**는 이 분석에서 핵심 지표로 작용한다. 정규분포의 첨도는 3인데, 5나 6과 같은 이례적으로 높은 첨도가 관측될 경우, 이는 매칭 알고리즘 조작의 강력한 근거가 될 수 있다.
</s>

만약 어떤 플레이어가 자기 수준에 맞는 티어를 갖고 있다면, 확률에 따른 연승/연패 이후 변경된 지표에서의 승률은 자연스럽게 변동할 것(연승 이후 승리확률 감소 / 연패 이후 승리확률 증가)

확률에 따른 연승/연패 이후 승률이 상승/하락하는 지표가 나타난다면, 해당 측면에 대한 고려가 불필요할 수 있음.


방법론 II. 아군/적군 간 티어 불균형 분석


유저의 연승/연패를 추적하고, 각 게임에서 자신의 아군과 적군의 평균 티어 차이를 비교한다.

이 방법은 연승 중인 플레이어가 의도적으로 낮은 티어의 팀원들과 배치되는지 여부를 검증하는 데 초점을 둔다.


+ 티어 외, 승률에 대해서도 고려가 가능하다면(연산량이 허락한다면) 고려할 것.


방법론 III. 연승 수에 따른 다음 게임 기대 승률 분석


연승 횟수에 따라 다음 게임의 기대 승률이 어떻게 변화하는지를 분석한다.

핵심 질문:
연승 또는 연패가 다음 게임의 승률에 영향을 미치는가?

수학적으로 공정한 매칭이라면, 각 게임의 승률은 항상 0.5 수준에서 유지되어야 한다.
그러나 실제 게임 환경에서는 피로, 멘탈 붕괴(‘틸트’) 등 외적 요인으로 인해, 연속적으로 게임을 플레이한 유저가 중반~후반 40%대의 승률을 보일 가능성이 있다는 가설을 설정한다.

따라서 이 방법론은 방법론 II의 결과와 상충되지 않는 범위 내에서 해석하고 검증을 진행한다.


방법론 IV. 마코프 체인?

방법론 1에서 제기된 문제를 해결할 수 있을지를 더 검토해 볼 필요가 있음. 방법론 2와 함께 사용하는 것을 고려.


Packages:



## 라이선스 고지사항
해당 프로젝트는 renecotyfanboy의 코드와 분석 일부(https://github.com/renecotyfanboy/leagueProject)를 차용하여 작성되었습니다.
해당 프로젝트는 MIT License의 규정 아래 있습니다.
