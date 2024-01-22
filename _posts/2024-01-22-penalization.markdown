---
layout: post
title:  "About Penalization"
show_date: true
comments: true
---

I've changed penalization parameters, specifically `lambda` and `alpha` in the xgboost.

To be brief, the penalization parameters were effective for `default XGBoost` but not for the `XGBoost with random forest`.<br>
This may only be true for this issue, so it should not be misunderstood.

When changing lambda or alpha, alpha is set as the default value when changing lambda, and alpha is set as the default value when changing alpha(Other parameters are not changed).<br>

I attached the RMSE graph in each case below.<br>

**[`lambda` ranges from 1 to 20; alpha = 1]**<br>
**1. Default XGBoost**<br>
{% include plotly/RMSE_of_BT_lambda_change.html %}

**2. XGBoost with Random Forest**
{% include plotly/RMSE_of_BTRF_lambda_change.html %}

**[`alpha` ranges from 1 to 19; lambda = 0]**<br>
**1. Default XGBoost**<br>
{% include plotly/RMSE_of_BT_alpha_change.html %}

**2. XGBoost with Random Forest**
{% include plotly/RMSE_of_BTRF_alpha_change.html %}

<br>
The below plot is the mean of RMSE for the whole test period.
![image](/assetsimages/mean_of_rmse.png)
