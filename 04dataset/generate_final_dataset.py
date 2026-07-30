
"""
generate_final_dataset.py

Creates a flattened session-level analytics dataset by merging:
- users_master.csv
- sessions_calendar.csv
- products_master.csv

Output:
- fashion_ga4_events_90_days.csv
- fashion_ga4_events_90_days.xlsx

One row = One session
"""

import pandas as pd
import numpy as np
import random
import uuid

np.random.seed(42)
random.seed(42)

users = pd.read_csv("users_master.csv", parse_dates=["first_visit_date","first_purchase_date"])
sessions = pd.read_csv("sessions_calendar.csv", parse_dates=["session_date"])
products = pd.read_csv("products_master.csv")

df = sessions.merge(users,on=["customer_id","user_pseudo_id"],how="left")
df = df.sort_values(["customer_id","session_date","session_number"])

cat_weights={"Women":0.40,"Men":0.23,"Accessories":0.12,"Beauty":0.10,"Footwear":0.10,"Kids":0.05}
cats=list(cat_weights.keys())
probs=list(cat_weights.values())

cust_orders={}
cust_rev={}

rows=[]

for _,r in df.iterrows():

    page_view=1
    view_item=np.random.rand()<0.75
    add_to_cart=view_item and (np.random.rand()<0.22)
    begin_checkout=add_to_cart and (np.random.rand()<0.14/0.22)
    purchase=begin_checkout and (np.random.rand()<0.08/0.14)
    refund=False

    product_id=product_name=product_category=brand=None
    price=discount_percent=quantity=0
    item_revenue=coupon_discount=refund_amount=net_revenue=0
    order_id=transaction_id=None
    payment_method=delivery_type=None
    coupon_code=None
    returned_product=False
    return_reason=None

    if purchase:
        cat=np.random.choice(cats,p=probs)
        p=products[products.product_category==cat].sample(1).iloc[0]

        product_id=p.product_id
        product_name=p.product_name
        product_category=p.product_category
        brand=p.brand
        price=float(p.price)
        discount_percent=float(p.discount_percent)

        quantity=np.random.choice([1,2,3],p=[0.8,0.17,0.03])

        gross=price*quantity
        coupon_discount=0 if random.random()<0.6 else round(gross*0.10,2)
        item_revenue=round(gross-coupon_discount,2)

        if random.random()<0.03:
            refund=True
            returned_product=True
            refund_amount=item_revenue
            net_revenue=0
            return_reason=random.choice(
                ["Wrong Size","Damaged Product","Changed Mind","Late Delivery"]
            )
        else:
            refund_amount=0
            net_revenue=item_revenue

        order_id="ORD"+str(random.randint(100000,999999))
        transaction_id="TXN-"+str(uuid.uuid4())[:12]
        payment_method=random.choice(
            ["UPI","Credit Card","Debit Card","Net Banking","Cash on Delivery"]
        )
        delivery_type=random.choice(
            ["Standard","Express","Same Day"]
        )

        coupon_code=random.choice(
            [None,None,None,"WELCOME10","SAVE20","SUMMER15","FREESHIP"]
        )

        cust_orders[r.customer_id]=cust_orders.get(r.customer_id,0)+1
        cust_rev[r.customer_id]=cust_rev.get(r.customer_id,0)+net_revenue

    rows.append({
        "customer_id":r.customer_id,
        "user_pseudo_id":r.user_pseudo_id,
        "session_id":r.session_id,
        "session_number":r.session_number,
        "session_date":r.session_date,
        "first_visit_date":r.first_visit_date,
        "user_type":"Returning" if r.session_number>1 else "New",
        "country":r.country,
        "city":r.city,
        "gender":r.gender,
        "age_group":r.age_group,
        "customer_segment":r.customer_segment,
        "source":r.source,
        "medium":r.medium,
        "campaign":r.campaign,
        "channel_group":r.channel_group,
        "landing_page":r.landing_page,
        "device_category":r.device_category,
        "page_view":page_view,
        "view_item":int(view_item),
        "add_to_cart":int(add_to_cart),
        "begin_checkout":int(begin_checkout),
        "purchase":int(purchase),
        "refund":int(refund),
        "product_id":product_id,
        "product_name":product_name,
        "product_category":product_category,
        "brand":brand,
        "price":price,
        "discount_percent":discount_percent,
        "quantity":quantity,
        "item_revenue":item_revenue,
        "coupon_discount":coupon_discount,
        "refund_amount":refund_amount,
        "net_revenue":net_revenue,
        "order_id":order_id,
        "transaction_id":transaction_id,
        "payment_method":payment_method,
        "delivery_type":delivery_type,
        "coupon_code":coupon_code,
        "returned_product":returned_product,
        "return_reason":return_reason,
        "lifetime_orders":cust_orders.get(r.customer_id,0),
        "lifetime_revenue":cust_rev.get(r.customer_id,0)
    })

out=pd.DataFrame(rows)
out["month"]=out.session_date.dt.month
out["week"]=out.session_date.dt.isocalendar().week.astype(int)
out["quarter"]=out.session_date.dt.quarter
out["year"]=out.session_date.dt.year
out["day_of_week"]=out.session_date.dt.day_name()
out["is_weekend"]=out.session_date.dt.dayofweek>=5

out.to_csv("fashion_ga4_events_90_days.csv",index=False)
out.to_excel("fashion_ga4_events_90_days.xlsx",index=False)

print(out.shape)
print("Purchases:",int(out.purchase.sum()))
print("Revenue:",round(out.net_revenue.sum(),2))
