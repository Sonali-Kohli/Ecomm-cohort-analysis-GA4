# E-commerce Cohort Analysis on GA4-style Dataset

Power BI | Excel | Python <br>

### Objective:
To analyze 180 days of GA4 event-level data to answer following questions: \
Which customer acquisition cohorts generate the highest long-term value? \
Which marketing channels acquire customers who actually return? \
Which seasonal campaigns create lasting customers rather than one-time buyers? 

### Dashboard:
Image

### Business Problem:
#### Company: TrendHive Fashion (fictional)
TrendHive is a Series A funded online fashion and apparel marketplace operating in India. \
Their growth team believes acquisition is working, but customers are not returning frequently enough. 

### Executive Summary (Top metrics):
| Acquisition | Retention | Engagement |
| --- | --- | --- |
| Total acquired users, 3.912k | Avg. order per user, 3.17 | Product view rate%, 75.62%  |
| Best channel return rate (Push), 12.18% | Avg. D90 retention, 17.05% | Cart addition rate%, 16.09% |
| Avg. revenue LTV, $9.79k | Avg. D30 retention, 10.66% |  Cart to purchase rate%, 37.64% |     

### Executive Summary (Dashboard walkthrough):
Tab 1 highlights there is evidence for strong Product-Market fit with overall D30 bounded retention at 10.66% (industry standards). \
Push and meta retargeting are showing better retention rates, suggesting acquisition of quality customers over google shopping \
where repeat purchase rate is higher but revenue is low. \
The customers from the these campaigns can be seasonal or discount buyers who has longer purchase cycle because of a lower repeat rate. 

Tab 2 highlights that highest LTV is coming from “Always on search” campaign for D30 and “Instagram influencers” for D90. 

Tab 3 highlights in the funnel steps, worst leakage is happening in product view to add to cart step (only 21% added items in the cart). \
As for the engagement depth, on average less than 1 product is viewed in a session. \
This hints towards large homepage bounces. \
In the RFM segment, around 1.18k are in the Can’t Lose category, meaning they used to buy regularly (in the D90, D180 LTV milestone) \
but has stopped returning (low RFM scores). 2.48k customers are already in the Lost category. 

### Recommendations: 
Execute 4 strategies chronologically according to their urgency and impact on the situation (detailed explanation in full report): 
1. Churn Strategy for retention
2. Customer Segmentation for acquiring right target audience
3. Improving bounce rates to counter high landing page bounce rates
4. Product page analysis to improve UI/UX issues
