---
title:  "Model specification"
show_date: true
comments: true
layout: single
categories:
  - Oil price forecasting
tags:
  - Python
  - XGBoost
toc: true
toc_sticky: true
---

For the WTI nominal price forecasting, I specify the model as below.

- $y_{t} = \beta_{1}y_{t-1} + \beta_{2}y_{t-2} + \beta_{3}y_{t-3} + \beta_{4}y_{t-4} + f(X_{t-1}) + \epsilon_{t}$ 

where $y_{t} = WTI_{t} / CPI_{t-1}$