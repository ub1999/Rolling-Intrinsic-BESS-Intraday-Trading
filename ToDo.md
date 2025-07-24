# To Do:
### Phase 1:
- [x] Create a notebook for generating Synthetic Data
  - [x] First chose format .parquet or .csv etc
  - [x] Choose how the table should look, it should be similar to the database in the Original Repo
- [x] Replicate the method for calculating VWAP using your own synthetic data
### Phase 2:
- [ ] Enable the setting of bucket size in simulation 
- [ ] Enable get closest time
- [ ] Start Visualisation with DASH
### Phase 3: 
- [ ] Build a visualiation page to compare different strategies 


# Other Notes 
- It appears the the generated prices **all execute at quarter hours,** so we have already put everything into 15 min buckets in the repo
  -  but IRL it would have to be **collected into buckets live**!    
- Possible Idea:
  - Use the dynamic programming library, within each bucket, assign exponentially increasing weights to prices, as you get closer to the end of the bucket.
    - eg. bucket is 5 min. first min VWAP has weight 1, second min has 2, third min has 4, fourth min has 8, fifth minute has 16 ...
    - Ideally these parameters should be recalibrating themselves using market data regularly.... 
      - How do you accomplish this?
- Suggestion from Mehmet: VWAP is not enough, include additional weights that add more value to more recent transactions to benefit from higher liquidity.
  1. Option : [Gauss–Laguerre](https://en.wikipedia.org/wiki/Gauss%E2%80%93Laguerre_quadrature)
  2. Option : ["Chebyshev Polynomials"](https://en.wikipedia.org/wiki/Chebyshev_polynomials)
  3. Option : Use unsupervised learning to decide what max weights should be

- Is there correlation between reserve markets and CID when looking at the revenues
- The parameters for VWAP should adjust dynamically based on prior Reserve data, train parameters from that, and then keep them in production (for example)