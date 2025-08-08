# To Do:
### Phase 1:
- [x] Create a notebook for generating Synthetic Data
  - [x] First chose format .parquet or .csv etc
  - [x] Choose how the table should look, it should be similar to the database in the Original Repo
- [x] Replicate the method for calculating VWAP using your own synthetic data
### Phase 2:
- [x] Enable the setting of bucket size in simulation 
  - Implemented already. The __execution_time_end__ variable is dynamically adjusted based on bucket size!
- [x] Enable the function get closest time
  - Operation is performed by the function get_average_prices()
- [ ] Start Visualisation with DASH

### Phase 3: 
- [ ] Build a visualiation page to compare different strategies 
- [ ] Strategies
  - [ ] Different weights in VWAP depending on execution time of transaction
  - [ ] Different bucket sizes in rolling intrinsic window
  - [ ] Forecast based strategy 
### Phase 4:
- [ ] Each day is currently simulated individually. Adapt strategy to join days.
  - [ ] How does this look for a system incorporating resopt?
### Graph 
::: mermaid

graph TD
    subgraph B[Step 1: Gather Information]
    direction LR
        C[Create a notebook for generating Synthetic Data]:::completed
        C --> D[Choose format .parquet or .csv]:::completed
        C --> E[Choose table structure similar to Original Repo]:::completed
        F[Replicate method for calculating VWAP]:::completed
        F_1[Get some sample LOB transaction Data]:::completed
        F_2[Get access to Axpo Git ⏳]:::inProgress
    end
    
    subgraph G[Step 2: Helper Functions]
    direction LR
        H[Enable setting of bucket size in simulation]
        I[Enable function get closest time]
        J[Start Visualisation with DASH]
    end

    subgraph K[Step 3: Testing Outcomes]
        L[Build a visualisation page to compare different strategies]
        M[Strategies]
        M --> N[Different weights in VWAP depending on execution time]
        M --> O[Different bucket sizes in rolling intrinsic window]
        M --> P[Forecast based strategy]
    end

    B --> G --> K

    classDef completed fill:#d4edda, stroke:#c3e6cb, stroke-width:2px;
    classDef inProgress fill:#fff3cd, stroke:#ffeeba, stroke-width:2px;

:::


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