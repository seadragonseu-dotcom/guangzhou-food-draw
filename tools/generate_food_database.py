"""
广州美食数据库生成工具 V1.1

Generate:
- restaurants sheet
- dishes sheet
- food_relation sheet

Database:
restaurants: 150
dishes: 400
food_relation: 400

Meal:
早餐 100
午餐 150
晚餐 150
"""

from pathlib import Path
from datetime import datetime
import random

import pandas as pd


# =====================================================
# Path
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

OUTPUT_FILE = (
    BASE_DIR
    /
    "source"
    /
    "guangzhou_food_database.xlsx"
)


# =====================================================
# Basic Data
# =====================================================

DISTRICTS = [
    "天河",
    "越秀",
    "荔湾",
    "海珠",
    "白云",
    "番禺",
    "黄埔",
    "南沙"
]


CATEGORIES = [
    "粤菜",
    "早茶",
    "火锅",
    "烧腊",
    "小吃",
    "日料",
    "川菜",
    "湘菜"
]


RESTAURANT_PREFIX = [
    "广州",
    "老字号",
    "岭南",
    "百年",
    "金牌",
    "传统",
    "新派"
]


DISH_LIBRARY = {

    "早餐": [
        "虾饺",
        "肠粉",
        "叉烧包",
        "艇仔粥",
        "云吞面",
        "烧卖",
        "萝卜糕",
        "牛肉肠粉",
        "皮蛋瘦肉粥",
        "蛋挞"
    ],

    "午餐": [
        "白切鸡",
        "烧鹅",
        "叉烧",
        "盐焗鸡",
        "煲仔饭",
        "清蒸鱼",
        "牛腩煲",
        "豉汁排骨",
        "梅菜扣肉",
        "炒牛河"
    ],

    "晚餐": [
        "广式火锅",
        "海鲜大餐",
        "潮汕牛肉火锅",
        "烧味拼盘",
        "砂锅粥",
        "粤式小炒",
        "椒盐虾",
        "蒸汽海鲜",
        "乳鸽",
        "顺德鱼生"
    ]

}


REASONS = [
    "广州经典特色美食",
    "适合情侣约会",
    "本地人常去",
    "环境舒适",
    "传统广州味道",
    "适合朋友聚餐"
]


# =====================================================
# Generate restaurants
# =====================================================

def generate_restaurants():

    restaurants = []

    for i in range(1, 151):

        district = random.choice(DISTRICTS)

        restaurants.append({

            "id": i,

            "name":
                random.choice(
                    RESTAURANT_PREFIX
                )
                +
                "餐厅"
                +
                str(i),

            "district":
                district,

            "category":
                random.choice(
                    CATEGORIES
                ),

            "rating":
                round(
                    random.uniform(
                        4.0,
                        5.0
                    ),
                    1
                ),

            "price":
                random.choice(
                    [
                        50,
                        80,
                        100,
                        150,
                        200
                    ]
                ),

            "couple_score":
                random.randint(
                    3,
                    5
                ),

            "taste_score":
                random.randint(
                    3,
                    5
                ),

            "environment_score":
                random.randint(
                    3,
                    5
                ),

            "business_hours":
                "08:00-22:00",

            "address":
                f"广州市{district}商业区"

        })

    return restaurants



# =====================================================
# Generate dishes
# =====================================================

def generate_dishes():

    dishes = []

    dish_id = 1


    for meal, count in [

        ("早餐", 100),

        ("午餐", 150),

        ("晚餐", 150)

    ]:


        for _ in range(count):

            dishes.append({

                "id":
                    dish_id,

                "name":
                    random.choice(
                        DISH_LIBRARY[meal]
                    ),

                "meal":
                    meal,

                "category":
                    random.choice(
                        CATEGORIES
                    )

            })


            dish_id += 1


    return dishes



# =====================================================
# Generate relation
# =====================================================

def generate_food_relation(
        restaurants,
        dishes
):

    relations = []


    for index, dish in enumerate(
        dishes,
        start=1
    ):

        restaurant = random.choice(
            restaurants
        )

        relations.append({

            "id":
                index,

            "restaurant_id":
                restaurant["id"],

            "dish_id":
                dish["id"],

            "meal":
                dish["meal"],

            "tags":
                "情侣,广州特色",

            "reason":
                random.choice(
                    REASONS
                )

        })


    return relations



# =====================================================
# Export Excel
# =====================================================

def export_excel(
        restaurants,
        dishes,
        relations
):

    OUTPUT_FILE.parent.mkdir(
        exist_ok=True
    )


    with pd.ExcelWriter(
        OUTPUT_FILE,
        engine="openpyxl"
    ) as writer:


        pd.DataFrame(
            restaurants
        ).to_excel(

            writer,

            sheet_name="restaurants",

            index=False

        )


        pd.DataFrame(
            dishes
        ).to_excel(

            writer,

            sheet_name="dishes",

            index=False

        )


        pd.DataFrame(
            relations
        ).to_excel(

            writer,

            sheet_name="food_relation",

            index=False

        )



# =====================================================
# Main
# =====================================================

def main():

    print("=" * 50)

    print(
        "广州美食数据库生成工具 V1.1"
    )

    print("=" * 50)


    restaurants = generate_restaurants()

    dishes = generate_dishes()

    relations = generate_food_relation(
        restaurants,
        dishes
    )


    export_excel(
        restaurants,
        dishes,
        relations
    )


    print()

    print(
        f"餐厅数量: {len(restaurants)}"
    )

    print(
        f"菜品数量: {len(dishes)}"
    )

    print(
        f"推荐数量: {len(relations)}"
    )

    print()

    print(
        "早餐: 100"
    )

    print(
        "午餐: 150"
    )

    print(
        "晚餐: 150"
    )

    print()

    print(
        "输出文件:"
    )

    print(
        OUTPUT_FILE
    )

    print()

    print(
        "🎉 数据库生成完成"
    )

    print(
        "更新时间:",
        datetime.now()
    )



if __name__ == "__main__":

    main()