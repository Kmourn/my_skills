# Statistical Test Selection Guide

Choose the estimand and independent unit before using this guide. Pairing, clustering, repeated measures, the outcome scale, and the model assumptions determine the eligible analyses. A normality-test p-value alone does not choose a test; changing to ranks or transforming an outcome can change the scientific target.

## Decision Tree for Test Selection

### 1. Comparing Groups

#### Two Independent Groups
- **Mean contrast**: Consider Welch's t-test; use a pooled-variance Student test only with a justified common-variance model. Assess distribution and influential observations for the intended inference.
- **Rank/distribution contrast**: Mann-Whitney U test (Wilcoxon rank-sum). Its null concerns the underlying distributions; a location or median interpretation needs additional assumptions.
- **Binary outcome**: Chi-square test or Fisher's exact test (if expected counts < 5)
- **Ordinal outcome**: Mann-Whitney U test

#### Two Paired/Dependent Groups
- **Mean of within-pair differences**: Paired t-test; assess differences, not the two marginal distributions.
- **Signed-rank contrast**: Wilcoxon signed-rank test; assess symmetry of differences and specify treatment of zeros and ties.
- **Binary outcome**: McNemar's test
- **Ordinal outcome**: Choose an analysis justified for the paired scale and the meaning of differences; signed ranks require meaningful differences and their assumptions.

#### Three or More Independent Groups
- **Mean contrasts, justified equal variances**: One-way ANOVA
- **Mean contrasts, unequal variances**: Welch's ANOVA
- **Rank contrasts**: Kruskal-Wallis H test; state the target and assumptions needed for interpretation.
- **Binary/categorical outcome**: Chi-square test
- **Ordinal outcome**: Kruskal-Wallis H test

#### Three or More Paired/Dependent Groups
- **Mean contrasts**: Repeated measures ANOVA or a mixed model that reflects the dependence and missingness pattern.
- **Complete-block rank contrasts**: Friedman test
- **Binary outcome**: Cochran's Q test

#### Multiple Factors (Factorial Designs)
- **Continuous outcome**: Two-way ANOVA (or higher-way ANOVA)
- **With covariates**: ANCOVA
- **Mixed within and between factors**: Mixed ANOVA

### 2. Relationships Between Variables

#### Two Continuous Variables
- **Linear relationship, bivariate normal**: Pearson correlation
- **Monotonic rank association**: Spearman rank correlation; this estimates a different association from Pearson's linear correlation.
- **Rank-based data**: Spearman or Kendall's tau

#### One Continuous Outcome, One or More Predictors
- **Single continuous predictor**: Simple linear regression
- **Multiple continuous/categorical predictors**: Multiple linear regression
- **Categorical predictors**: ANOVA/ANCOVA framework
- **Non-linear relationships**: Polynomial regression or generalized additive models (GAM)

#### Binary Outcome
- **Single predictor**: Logistic regression
- **Multiple predictors**: Multiple logistic regression
- **Rare events**: Exact logistic regression or Firth's method

#### Count Outcome
- **Poisson-distributed**: Poisson regression
- **Overdispersed counts**: Negative binomial regression
- **Zero-inflated**: Zero-inflated Poisson/negative binomial

#### Time-to-Event Outcome
- **Comparing survival curves**: Log-rank test
- **Modeling with covariates**: Cox proportional hazards regression
- **Parametric survival models**: Weibull, exponential, log-normal

### 3. Agreement and Reliability

#### Inter-Rater Reliability
- **Categorical ratings, 2 raters**: Cohen's kappa
- **Categorical ratings, >2 raters**: Fleiss' kappa or Krippendorff's alpha
- **Continuous ratings**: Intraclass correlation coefficient (ICC)

#### Test-Retest Reliability
- **Continuous measurements**: ICC or Pearson correlation
- **Internal consistency**: Cronbach's alpha

#### Agreement Between Methods
- **Continuous measurements**: Bland-Altman analysis
- **Categorical classifications**: Cohen's kappa

### 4. Categorical Data Analysis

#### Contingency Tables
- **2x2 table**: Chi-square test or Fisher's exact test
- **Larger than 2x2**: Chi-square test
- **Ordered categories**: Cochran-Armitage trend test
- **Paired categories**: McNemar's test (2x2) or McNemar-Bowker test (larger)

### 5. Bayesian Alternatives

Any of the above tests can be performed using Bayesian methods:
- **Group comparisons**: Bayesian t-test, Bayesian ANOVA
- **Correlations**: Bayesian correlation
- **Regression**: Bayesian linear/logistic regression

**Advantages of Bayesian approaches:**
- Provides probability of hypotheses given data
- Naturally incorporates prior information
- Provides credible intervals instead of confidence intervals
- Requires justified likelihoods and priors, suitable diagnostics, and careful interpretation of posterior quantities; it does not remove design or inference problems.

## Key Considerations

### Sample Size
- Justify sample size or precision using the intended contrast, independent units, plausible variation or effect scenarios, and the design. There is no universal `n = 30` eligibility rule.
- For small samples, evaluate whether a model, exact procedure, or resampling method has defensible assumptions; rank tests and bootstraps are not automatically valid substitutes.
- Distinguish repeated measurements or model seeds from independent sampling units.
- Report effect estimates and uncertainty at any sample size.

### Multiple Comparisons
- When conducting multiple tests, adjust for multiple comparisons using:
  - Bonferroni correction (conservative)
  - Holm-Bonferroni (less conservative)
  - False Discovery Rate (FDR) control (Benjamini-Hochberg)
  - Tukey HSD for post-hoc ANOVA comparisons

### Missing Data
- Complete case analysis (listwise deletion)
- Multiple imputation
- Maximum likelihood methods
- State the missingness assumptions (MCAR, MAR, MNAR), investigate available evidence, and assess sensitivity; an observed-data diagnostic does not establish the mechanism.

### Effect Sizes
- Always report effect sizes alongside p-values
- See `effect_sizes_and_power.md` for guidance

### Study Design Considerations
- Randomized controlled trials: Standard parametric/non-parametric tests
- Observational studies: Consider confounding and use regression/matching
- Clustered/nested data: Use mixed-effects models or GEE
- Time series: Use time series methods (ARIMA, etc.)

## Sources for the distinctions above

Checked 2026-10-01: official SciPy documentation for [Welch's t-test](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html), [Mann-Whitney U](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html), and [Wilcoxon signed-rank](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html); [ASA statement on p-values](https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf). These sources support the test-null and p-value distinctions; sample-size choices still need a task-specific design rationale.
