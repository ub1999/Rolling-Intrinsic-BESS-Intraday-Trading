# Exploring the outcomes of different strategies 
#### To start off, the influence of window size on outcomes is explored and verified.
* [Schaurecker et al claim a high frequency trading approach increases revenue by 14% compared to relying on a rolling window as small as 1 minute!](https://arxiv.org/html/2504.06932v2) 
    * Uses [BitePy](https://dschaurecker.github.io/bitepy/) python library which solves the optimisation problem faster
    * Enables sub minute calculations 
    * The paper also discusses effects on including the whole limit order book
    * Accounts for different open positions when doing simulations! (Many other approaches only consider CID)
      * Having initial open positions enables the incorporation of the optimal dispatch from ResOpt which plans day ahead schedule!
* [ The next effect that needs to be quantified is the influence of including forecasts into the price curve provided to the optimizier within each window](Hornek(https://arxiv.org/abs/2501.07121)). 
  * This is due to the claims of Hornek et al, which indicates that their rolling intrinsic approach including forecasts, performs better than using the ID1 index to set BESS dispatch daily.
  * However, the inclusion of forecasts with the basic BESS approach has not been compared, and neither has the effect of not completely utilizing the battery been explored in the study! 
    * Both these factors leave significant room for exploration. 
## Influence of different rolling window sizes 