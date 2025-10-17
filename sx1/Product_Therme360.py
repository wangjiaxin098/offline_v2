import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# 生成时间范围：2025-10-08至2025-10-17
start_date = datetime(2025, 10, 8)
end_date = datetime(2025, 10, 17)
date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

# 1. 商品基础信息（20个商品）
products = {
    "product_id": range(1, 21),
    "product_name": [f"商品{i}" for i in range(1, 21)],
    "category": random.choices(["服装", "电子产品", "家居", "美妆"], k=20),
    "original_price": [round(random.uniform(50, 2000), 2) for _ in range(20)],
    "cost_price": [round(p * random.uniform(0.3, 0.7), 2) for p in [round(random.uniform(50, 2000), 2) for _ in range(20)]],
    "tax_rate": [0.13] * 20
}
df_product = pd.DataFrame(products)

# 2. SKU信息（每个商品3-5个SKU）
skus = []
for pid in range(1, 21):
    sku_count = random.randint(3, 5)
    specs = random.choices(["标准版", "升级版", "豪华版"], k=sku_count)
    colors = random.choices(["红", "蓝", "黑", "白", "绿"], k=sku_count)
    sizes = random.choices(["S", "M", "L", "XL", "均码"], k=sku_count)
    for i in range(sku_count):
        skus.append({
            "sku_id": len(skus) + 1,
            "product_id": pid,
            "spec": specs[i],
            "color": colors[i],
            "size": sizes[i]
        })
df_sku = pd.DataFrame(skus)

# 3. 访客流量表（5000条）
visitors = []
channels = ["search", "recommend", "store"]
keywords = ["夏季连衣裙", "无线耳机", "智能手表", "粉底液", "沙发", "牛仔裤", "充电宝", "面霜"]
modules = ["规格选择", "售后说明", "用户评价", "关联商品"]
for _ in range(5000):
    pid = random.randint(1, 20)
    vid = f"vid_{random.randint(10000, 99999)}"
    channel = random.choice(channels)
    keyword = random.choice(keywords) if channel == "search" else None
    visit_time = random.choice(date_range) + timedelta(hours=random.randint(8, 22), minutes=random.randint(0, 59))
    stay = random.randint(10, 300)
    is_bounce = 1 if random.random() < 0.3 else 0  # 30%跳失率
    click = ",".join(random.sample(modules, k=random.randint(0, 3))) if not is_bounce else None
    visitors.append({
        "flow_id": len(visitors) + 1,
        "product_id": pid,
        "visitor_id": vid,
        "channel": channel,
        "keyword": keyword,
        "visit_time": visit_time,
        "stay_seconds": stay,
        "is_bounce": is_bounce,
        "click_modules": click
    })
df_visitor = pd.DataFrame(visitors)

# 4. 加购收藏表（1000条）
carts = []
for _ in range(1000):
    pid = random.randint(1, 20)
    vid = f"vid_{random.randint(10000, 99999)}"
    behavior = random.choice(["cart", "collect"])
    ctime = random.choice(date_range) + timedelta(hours=random.randint(8, 22))
    carts.append({
        "id": len(carts) + 1,
        "product_id": pid,
        "visitor_id": vid,
        "behavior_type": behavior,
        "create_time": ctime
    })
df_cart = pd.DataFrame(carts)

# 5. 订单表（800条）
orders = []
for _ in range(800):
    pid = random.randint(1, 20)
    sku_ids = df_sku[df_sku["product_id"] == pid]["sku_id"].tolist()
    sid = random.choice(sku_ids)
    vid = f"vid_{random.randint(10000, 99999)}"
    channel = random.choice(channels)
    keyword = random.choice(keywords) if channel == "search" else None
    original = df_product[df_product["product_id"] == pid]["original_price"].values[0]
    discount = round(original * random.uniform(0, 0.3), 2) if random.random() < 0.6 else 0
    coupon = round(random.uniform(0, discount * 0.5), 2) if discount > 0 else 0
    pay_amt = original - discount - coupon
    ptime = random.choice(date_range) + timedelta(hours=random.randint(9, 21))
    orders.append({
        "order_id": len(orders) + 1,
        "product_id": pid,
        "sku_id": sid,
        "visitor_id": vid,
        "channel": channel,
        "keyword": keyword,
        "pay_amount": pay_amt,
        "discount_amount": discount,
        "coupon_amount": coupon,
        "pay_time": ptime
    })
df_order = pd.DataFrame(orders)

# 6. 退货表（80条，10%退货率）
refunds = []
order_ids = df_order["order_id"].tolist()
reasons = ["质量问题", "尺寸不符", "描述不符", "物流损坏", "不想要了"]
for _ in range(80):
    oid = random.choice(order_ids)
    order_time = df_order[df_order["order_id"] == oid]["pay_time"].values[0]
    apply_time = order_time + timedelta(hours=random.randint(2, 72))
    complete_time = apply_time + timedelta(hours=random.randint(1, 24))
    refunds.append({
        "refund_id": len(refunds) + 1,
        "order_id": oid,
        "apply_time": apply_time,
        "complete_time": complete_time,
        "reason": random.choice(reasons)
    })
df_refund = pd.DataFrame(refunds)

# 7. 内容数据表（50条）
contents = []
for _ in range(50):
    pid = random.randint(1, 20)
    ctype = random.choice(["live", "video"])
    start_time = random.choice(date_range) + timedelta(hours=random.randint(10, 20))
    view = random.randint(100, 5000)
    duration = view * random.randint(60, 300) if ctype == "live" else 0
    comment = random.randint(10, view // 10)
    like = random.randint(20, view // 5)
    share = random.randint(5, view // 20)
    collect = random.randint(10, view // 15) if ctype == "video" else 0
    visitor = random.randint(5, view // 10)
    contents.append({
        "content_id": len(contents) + 1,
        "product_id": pid,
        "content_type": ctype,
        "start_time": start_time,
        "view_count": view,
        "total_duration": duration,
        "comment_count": comment,
        "like_count": like,
        "share_count": share,
        "collect_count": collect,
        "visitor_count": visitor
    })
df_content = pd.DataFrame(contents)

# 8. 评价表（600条，75%评价率）
evals = []
eval_order_ids = random.sample(order_ids, 600)
for oid in eval_order_ids:
    order = df_order[df_order["order_id"] == oid].iloc[0]
    pid = order["product_id"]
    sid = order["sku_id"]
    dsr_desc = random.randint(1, 5)
    dsr_service = random.randint(1, 5)
    dsr_logistics = random.randint(1, 5)
    is_positive = 1 if (dsr_desc + dsr_service + dsr_logistics) / 3 >= 4 else 0
    is_active = 1 if random.random() < 0.6 else 0
    content = f"{'好评！' if is_positive else '差评！'} 商品质量{'不错' if is_positive else '一般'}"
    ctime = pd.to_datetime(order["pay_time"]) + timedelta(hours=random.randint(24, 168))
    evals.append({
        "eval_id": len(evals) + 1,
        "order_id": oid,
        "product_id": pid,
        "sku_id": sid,
        "dsr_desc": dsr_desc,
        "dsr_service": dsr_service,
        "dsr_logistics": dsr_logistics,
        "is_positive": is_positive,
        "is_active": is_active,
        "content": content,
        "create_time": ctime
    })
df_eval = pd.DataFrame(evals)

# 写入MySQL（需先安装pymysql）
import pymysql
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:password@localhost:3306/ecommerce?charset=utf8")
df_product.to_sql("product_info", engine, if_exists="append", index=False)
df_sku.to_sql("sku_info", engine, if_exists="append", index=False)
df_visitor.to_sql("visitor_flow", engine, if_exists="append", index=False)
df_cart.to_sql("cart_collect", engine, if_exists="append", index=False)
df_order.to_sql("orders", engine, if_exists="append", index=False)
df_refund.to_sql("refund", engine, if_exists="append", index=False)
df_content.to_sql("content_data", engine, if_exists="append", index=False)
df_eval.to_sql("evaluation", engine, if_exists="append", index=False)

print("数据生成完成，共生成 {} 条记录".format(
    len(df_product) + len(df_sku) + len(df_visitor) + len(df_cart) +
    len(df_order) + len(df_refund) + len(df_content) + len(df_eval)
))