# Statistical Assumptions and Diagnostic Procedures

This document provides comprehensive guidance on checking and validating statistical assumptions for various analyses.

## General Principles

1. **Always check assumptions before interpreting test results**
2. **Use relevant diagnostic methods** (design assessment, plots, and formal tests where informative); non-rejection does not establish an assumption.
3. **Consider robustness**: Some tests are robust to violations under certain conditions
4. **Document all assumption checks** in analysis reports
5. **Report violations and remedial actions taken**

## Common Assumptions Across Tests

### 1. Independence of Observations

**What it means**: Each observation is independent; measurements on one subject do not influence measurements on another.

**How to check**:
- Review study design and data collection procedures
- For time series: Check autocorrelation (ACF/PACF plots, Durbin-Watson test)
- For clustered data: Consider intraclass correlation (ICC)

**What to do if violated**:
- Use mixed-effects models for clustered/hierarchical data
- Use time series methods for temporally dependent data
- Use generalized estimating equations (GEE) for correlated data

**Critical severity**: HIGH - violations can severely inflate Type I error

---

### 2. Normality

**What it means**: Data or residuals follow a normal (Gaussian) distribution.

**When required**:
- t-tests (group distributions for independent means; within-pair differences for paired means, interpreted with robustness and sampling assumptions)
- ANOVA (model errors or within-group distributions, interpreted with the design and robustness of the intended inference)
- Linear regression (for residuals)
- Some correlation tests (Pearson)

**How to check**:

**Visual methods** (primary):
- Q-Q (quantile-quantile) plot: Points should fall on diagonal line
- Histogram with normal curve overlay
- Kernel density plot

**Formal tests** (secondary):
- Shapiro-Wilk test (good default; scipy handles n up to ~5000 and warns above that)
- Lilliefors test (`statsmodels.stats.diagnostic.lilliefors`) — use this instead of a plain Kolmogorov-Smirnov test, which is invalid when the mean/SD are estimated from the data
- Anderson-Darling test

**Python implementation**:
```python
from scipy import stats
import matplotlib.pyplot as plt

# Shapiro-Wilk test
statistic, p_value = stats.shapiro(data)

# Q-Q plot
stats.probplot(data, dist="norm", plot=plt)
```

**Interpretation guidance**:
- A Shapiro-Wilk non-rejection does not prove normality; rejection alone does not select a replacement analysis.
- Interpret diagnostic sensitivity and precision with the sample size, plots, scientific target, and design. Fixed thresholds such as 30 or 100 do not certify model suitability.
- Look for severe skewness, outliers, or bimodality

**What to do if violated**:
- Reassess the intended inference with skewness, tails, influential observations, and dependence in view.
- Consider justified robust estimation, model-based inference, or resampling for the original target. Document any changed analysis and its assumptions.
- A transformation or rank test may answer a different question. Explain that change instead of treating it as an automatic remedy.

**Critical severity**: MEDIUM - parametric tests are often robust to mild violations with adequate sample size

---

### 3. Homogeneity of Variance (Homoscedasticity)

**What it means**: Variances are equal across groups or across the range of predictors.

**When required**:
- Pooled-variance Student t-test; Welch's t-test does not assume equal group variances
- Ordinary one-way ANOVA; Welch's ANOVA allows unequal group variances
- Linear regression (constant variance of residuals)

**How to check**:

**Visual methods** (primary):
- Box plots by group (for t-test/ANOVA)
- Residuals vs. fitted values plot (for regression) - should show random scatter
- Scale-location plot (square root of standardized residuals vs. fitted)

**Formal tests** (secondary):
- Levene's test (robust to non-normality)
- Bartlett's test (sensitive to non-normality, not recommended)
- Brown-Forsythe test (median-based version of Levene's)
- Breusch-Pagan test (for regression)

**Python implementation**:
```python
from scipy import stats
import pingouin as pg

# Levene's test
statistic, p_value = stats.levene(group1, group2, group3)

# For regression
# Breusch-Pagan test
# Note: exog must include the constant column (e.g. exog = sm.add_constant(X),
# or pass the fitted model's model.exog)
from statsmodels.stats.diagnostic import het_breuschpagan
_, p_value, _, _ = het_breuschpagan(residuals, exog)
```

**Interpretation guidance**:
- A variance ratio is descriptive; no fixed ratio establishes acceptable inference.
- Levene non-rejection does not establish equal variances or justify a pooled-variance test by itself.
- For ANOVA: Test is robust if groups have equal sizes
- For regression: Look for funnel patterns in residual plots

**What to do if violated**:
- **t-test**: Use Welch's t-test (does not assume equal variances)
- **ANOVA**: Use Welch's ANOVA or Brown-Forsythe ANOVA
- **Regression**:
  - Transform dependent variable (log, square root)
  - Use weighted least squares (WLS)
  - Use robust standard errors (HC3)
  - Use generalized linear models (GLM) with appropriate variance function

**Critical severity**: MEDIUM - tests can be robust with equal sample sizes

---

## Test-Specific Assumptions

### T-Tests

**Assumptions**:
1. Independence of observations
2. Normality (each group for independent t-test; differences for paired t-test)
3. Homogeneity of variance for the pooled Student test, not for Welch's test

**Diagnostic workflow**:
```python
import scipy.stats as stats
import pingouin as pg

# For independent mean contrasts, inspect group distributions and influential observations.
stats.shapiro(group1)
stats.shapiro(group2)
# For a paired mean contrast, assess within-pair differences instead.
# stats.shapiro(group1 - group2)

# Check homogeneity of variance
stats.levene(group1, group2)

# A mean-contrast analysis permitting unequal variances:
pg.ttest(group1, group2, correction=True)  # correction=True applies Welch's
# Use explicit settings for the intended model rather than diagnostic-driven switching.

# For an appropriate rank/distribution target with its own assumptions:
pg.mwu(group1, group2)  # Not an automatic substitute for a mean contrast.
```

---

### ANOVA

**Assumptions**:
1. Independence of observations within and between groups
2. Normality in each group
3. Homogeneity of variance across groups

**Additional considerations**:
- For repeated measures ANOVA: Sphericity assumption (Mauchly's test)

**Diagnostic workflow**:
```python
import pingouin as pg
from scipy import stats

# Check normality per group
for group in df['group'].unique():
    data = df[df['group'] == group]['value']
    w, p = stats.shapiro(data)
    print(f"{group}: W = {w:.3f}, p = {p:.4f}")

# Check homogeneity of variance
print(pg.homoscedasticity(df, dv='value', group='group'))

# For repeated measures: Check sphericity
# Automatically tested in pingouin's rm_anova
```

**What to do if sphericity violated** (repeated measures):
- Greenhouse-Geisser correction (ε < 0.75)
- Huynh-Feldt correction (ε > 0.75)
- Use multivariate approach (MANOVA)

---

### Linear Regression

**Assumptions**:
1. **Linearity**: Relationship between X and Y is linear
2. **Independence**: Residuals are independent
3. **Homoscedasticity**: Constant variance of residuals
4. **Normality**: Residuals are normally distributed
5. **No multicollinearity**: Predictors are not highly correlated (multiple regression)

**Diagnostic workflow**:

**1. Linearity**:
```python
import matplotlib.pyplot as plt
import seaborn as sns

# Scatter plots of Y vs each X
# Residuals vs. fitted values (should be randomly scattered)
plt.scatter(fitted_values, residuals)
plt.axhline(y=0, color='r', linestyle='--')
```

**2. Independence**:
```python
from statsmodels.stats.stattools import durbin_watson

# Durbin-Watson test (for time series)
dw_statistic = durbin_watson(residuals)
# Values between 1.5-2.5 suggest independence
```

**3. Homoscedasticity**:
```python
# Breusch-Pagan test
# Note: exog must include the constant column (e.g. sm.add_constant(X))
from statsmodels.stats.diagnostic import het_breuschpagan
_, p_value, _, _ = het_breuschpagan(residuals, exog)

# Visual: Scale-location plot
plt.scatter(fitted_values, np.sqrt(np.abs(std_residuals)))
```

**4. Normality of residuals**:
```python
# Q-Q plot of residuals
stats.probplot(residuals, dist="norm", plot=plt)

# Shapiro-Wilk test
stats.shapiro(residuals)
```

**5. Multicollinearity**:
```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Calculate VIF for each predictor
vif_data = pd.DataFrame()
vif_data["feature"] = X.columns
vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(len(X.columns))]

# VIF > 10 indicates severe multicollinearity
# VIF > 5 indicates moderate multicollinearity
```

**What to do if violated**:
- **Non-linearity**: Add polynomial terms, use GAM, or transform variables
- **Heteroscedasticity**: Transform Y, use WLS, use robust SE
- **Non-normal residuals**: Transform Y, use robust methods, check for outliers
- **Multicollinearity**: Remove correlated predictors, use PCA, ridge regression

---

### Logistic Regression

**Assumptions**:
1. **Independence**: Observations are independent
2. **Linearity**: Linear relationship between log-odds and continuous predictors
3. **No perfect multicollinearity**: Predictors not perfectly correlated
4. **Adequate information**: Justify sample size for event frequency, model complexity, and estimation method; a fixed events-per-predictor rule is not a guarantee.

**Diagnostic workflow**:

**1. Linearity of logit**:
```python
# Box-Tidwell test: Add interaction with log of continuous predictor
# If interaction is significant, linearity violated
```

**2. Multicollinearity**:
```python
# Use VIF as in linear regression
```

**3. Influential observations**:
```python
# Cook's distance, DFBetas, leverage (statsmodels >= 0.10)
# Do NOT use OLSInfluence on Logit/GLM results; use get_influence(),
# which returns MLEInfluence (Logit) or GLMInfluence (GLM)
influence = model.get_influence()
cooks_d, cooks_p = influence.cooks_distance  # returns a tuple: (distances, p_values)
```

**4. Model fit / calibration**:
```python
# Calibration curve: compare predicted probabilities to observed event rates
# (e.g. sklearn.calibration.calibration_curve), plus the Brier score
# Pseudo R-squared
# Classification metrics (accuracy, AUC-ROC)
# Note: the Hosmer-Lemeshow test is not implemented in scipy/statsmodels
# and is sensitive to the choice of bins; prefer calibration curves
```

---

## Outlier Detection

**Methods**:
1. **Visual**: Box plots, scatter plots
2. **Statistical**:
   - Z-scores: |z| > 3 suggests outlier
   - IQR method: Values < Q1 - 1.5×IQR or > Q3 + 1.5×IQR
   - Modified Z-score using median absolute deviation (robust to outliers)

**For regression**:
- **Leverage**: High leverage points (hat values)
- **Influence**: Cook's distance > 4/n suggests influential point
- **Outliers**: Studentized residuals > ±3

**What to do**:
1. Investigate data entry errors
2. Consider if outliers are valid observations
3. Report sensitivity analysis (results with and without outliers)
4. Use robust methods if outliers are legitimate

---

## Sample Size Considerations

### Design-specific justification

Specify the estimand, independent sampling or experimental unit, plausible variation or effect scenarios, precision or power target, dependence, missingness, and model complexity. Use an appropriate calculation or simulation and state its assumptions. A fixed number of observations, events, or seeds does not certify power, robustness, or validity.

### Small Sample Considerations

For small samples:
- Assumptions become more critical
- Use exact tests when available (Fisher's exact, exact logistic regression)
- Consider rank, exact, permutation, or bootstrap methods only when their target and assumptions fit the design.
- Be conservative with interpretation

---

## Reporting Assumption Checks

When reporting analyses, include:

1. **Statement of assumptions checked**: List all assumptions tested
2. **Methods used**: Describe visual and formal tests employed
3. **Results of diagnostic tests**: Report test statistics and p-values
4. **Assessment**: State whether assumptions were met or violated
5. **Actions taken**: If violated, describe remedial actions (transformations, alternative tests, robust methods)

**Example reporting statement**:
> "Normality was assessed using Shapiro-Wilk tests and Q-Q plots. Data for Group A (W = 0.97, p = .18) and Group B (W = 0.96, p = .12) showed no significant departure from normality. Homogeneity of variance was assessed using Levene's test, which was non-significant (F(1, 58) = 1.23, p = .27), indicating equal variances across groups. Therefore, assumptions for the independent samples t-test were satisfied."
