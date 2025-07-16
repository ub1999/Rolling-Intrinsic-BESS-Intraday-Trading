# To Do:
- [ ] Create a notebook for generating Synthetic Data
  - [ ] First chose format .parquet or .csv etc
  - [ ] Choose how the table should look, it should be similar to the database in the Original Repo
- [ ] Replicate the method for calculating VWAP using your own synthetic data
- [ ] Suggestion from Mehmet: VWAP is not enough, include additional weights that add more value to more recent transactions to benefit from higher liquidity.
- [ ] Is there correlation between reserve markets and CID when looking at the revenues
  - [ ] The parameters for VWAP should adjust dynamically based on priod Reserve data, train parameters from that, and then keep them in production (for example) 


### Other Notes 
- It appears the the generated prices **all execute at quarter hours,** so we have already put everything into 15 min buckets in the repo
  -  but IRL it would have to be **collected into buckets live**!    
- Possible Idea:
  - Use the dynamic programming library, within each bucket, assign exponentially increasing weights to prices, as you get closer to the end of the bucket.
    - eg. bucket is 5 min. first min VWAP has weight 1, second min has 2, third min has 4, fourth min has 8, fifth minute has 16 ...
    - Ideally these parameters should be recalibrating themselves using market data regularly.... 
      - How do you accomplish this?
      - 