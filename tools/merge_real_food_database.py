"""
广州真实美食数据库合并工具 V1.1

功能:
1. 读取真实餐厅坐标数据库
2. 生成标准 dishes
3. 生成 food_relation
4. 输出兼容 import_food_database.py V2.3 的Excel


Input:
source/
└── restaurant_source_geocoded.xlsx


Output:
source/
└── guangzhou_food_real_database.xlsx


Sheets:
- restaurants
- dishes
- food_relation
"""


from pathlib import Path
from datetime import datetime

import pandas as pd



# =====================================================
# Path
# =====================================================


BASE_DIR = Path(__file__).resolve().parent.parent


SOURCE_DIR = BASE_DIR / "source"


INPUT_FILE = (

    SOURCE_DIR /

    "restaurant_source_geocoded.xlsx"

)


OUTPUT_FILE = (

    SOURCE_DIR /

    "guangzhou_food_real_database.xlsx"

)



# =====================================================
# Dish Library
# =====================================================


DISH_LIBRARY = {


    "粤菜/早茶": [

        {
            "name": "虾饺",
            "type": "点心",
            "tags": "早茶,粤菜,经典",
            "description": "传统广式虾饺"
        },

        {
            "name": "叉烧包",
            "type": "点心",
            "tags": "早茶,粤菜",
            "description": "广式叉烧包"
        },

        {
            "name": "烧卖",
            "type": "点心",
            "tags": "早茶,点心",
            "description": "传统广式烧卖"
        },

        {
            "name": "凤爪",
            "type": "点心",
            "tags": "早茶,粤菜",
            "description": "豉汁蒸凤爪"
        },

        {
            "name": "肠粉",
            "type": "小吃",
            "tags": "早餐,广州美食",
            "description": "广式肠粉"
        }

    ],



    "粤菜": [

        {
            "name": "白切鸡",
            "type": "主菜",
            "tags": "粤菜,经典",
            "description": "广东传统白切鸡"
        },

        {
            "name": "烧鹅",
            "type": "主菜",
            "tags": "粤菜,烧腊",
            "description": "广式烧鹅"
        },

        {
            "name": "叉烧",
            "type": "烧腊",
            "tags": "粤菜,烧腊",
            "description": "蜜汁叉烧"
        },

        {
            "name": "老火靓汤",
            "type": "汤品",
            "tags": "粤菜,传统",
            "description": "广东老火汤"
        }

    ],



    "甜品": [

        {
            "name": "双皮奶",
            "type": "甜品",
            "tags": "甜品,广州",
            "description": "传统广东甜品"
        },

        {
            "name": "杨枝甘露",
            "type": "甜品",
            "tags": "甜品,香港风味",
            "description": "经典水果甜品"
        }

    ],



    "小吃": [

        {
            "name": "牛杂",
            "type": "小吃",
            "tags": "广州小吃,街头美食",
            "description": "广州传统牛杂"
        },

        {
            "name": "云吞面",
            "type": "小吃",
            "tags": "广州美食",
            "description": "广式云吞面"
        }

    ]

}



DEFAULT_DISH = [

    {

        "name": "招牌菜",

        "type": "特色菜",

        "tags": "广州美食",

        "description": "餐厅特色推荐"

    }

]



# =====================================================
# Load Restaurant
# =====================================================


def load_restaurants():


    df = pd.read_excel(

        INPUT_FILE

    )


    df = df[

        df["name"].notna()

    ]


    return df



# =====================================================
# Generate dishes
# =====================================================


def generate_dishes(restaurants):


    dishes = []


    dish_id = 1



    for _, row in restaurants.iterrows():


        category = str(

            row.get(

                "category",

                ""

            )

        )


        library = (

            DISH_LIBRARY.get(

                category,

                DEFAULT_DISH

            )

        )

        for item in library:
            dishes.append(

                {

                    "id": dish_id,

                    "restaurant_id": row["id"],

                    "restaurant": row["name"],

                    "name": item["name"],

                    "type": item["type"],

                    "category": category,

                    "tags": item["tags"],

                    "description": item["description"],

                    "meal": (

                        "早餐"

                        if "早茶" in item["tags"]

                        else "午餐"

                    )

                }

            )

            dish_id += 1


            dish_id += 1



    return pd.DataFrame(dishes)



# =====================================================
# Generate Relation
# =====================================================


def generate_relation(dishes):


    relations = []


    relation_id = 1



    for _, row in dishes.iterrows():


        relations.append(

            {

                "id":

                    relation_id,


                "restaurant_id":

                    row["restaurant_id"],


                "restaurant":

                    row["restaurant"],


                "dish_id":

                    row["id"],


                "dish":

                    row["name"],


                "meal":

                    row["meal"],


                "tags":

                    row["tags"],


                "reason":

                    f"{row['restaurant']}推荐{row['name']}",

            }

        )


        relation_id += 1



    return pd.DataFrame(relations)



# =====================================================
# Main
# =====================================================


def main():


    print("=" * 60)

    print(

        "广州真实美食数据库合并工具 V1.1"

    )

    print("=" * 60)



    restaurants = load_restaurants()



    dishes = generate_dishes(

        restaurants

    )


    relation = generate_relation(

        dishes

    )



    with pd.ExcelWriter(

        OUTPUT_FILE,

        engine="openpyxl"

    ) as writer:


        restaurants.to_excel(

            writer,

            sheet_name="restaurants",

            index=False

        )


        dishes.to_excel(

            writer,

            sheet_name="dishes",

            index=False

        )


        relation.to_excel(

            writer,

            sheet_name="food_relation",

            index=False

        )



    print()

    print(

        f"餐厅:{len(restaurants)}"

    )


    print(

        f"菜品:{len(dishes)}"

    )


    print(

        f"推荐关系:{len(relation)}"

    )


    print()

    print(

        "输出:",

        OUTPUT_FILE

    )


    print()

    print(

        "更新时间:",

        datetime.now()

    )


    print()

    print(

        "数据库合并完成"

    )





if __name__ == "__main__":

    main()