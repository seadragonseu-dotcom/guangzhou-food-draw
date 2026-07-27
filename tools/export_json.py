"""
Guangzhou Food Draw V2.0

Excel To JSON Exporter V2.1

功能:
1. Excel读取
2. 数据清洗
3. restaurants.json生成
4. dishes.json生成
5. food.json关系表生成

Python:
3.12+

依赖:
pandas
openpyxl
"""


from pathlib import Path
from datetime import datetime
import json


import pandas as pd





# =====================================================
# 路径配置
# =====================================================


BASE_DIR = Path(__file__).resolve().parent.parent


SOURCE_DIR = BASE_DIR / "source"


DATA_DIR = BASE_DIR / "data"


DATA_DIR.mkdir(
    exist_ok=True
)



RESTAURANT_EXCEL = (
    SOURCE_DIR /
    "restaurants_source.xlsx"
)



DISH_EXCEL = (
    SOURCE_DIR /
    "dishes_source.xlsx"
)





RESTAURANT_JSON = (
    DATA_DIR /
    "restaurants.json"
)



DISH_JSON = (
    DATA_DIR /
    "dishes.json"
)



FOOD_JSON = (
    DATA_DIR /
    "food.json"
)







# =====================================================
# JSON保存
# =====================================================


def save_json(
        file_path: Path,
        data: list
):

    """
    保存JSON文件
    """


    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:


        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )







# =====================================================
# 生成餐厅JSON
# =====================================================


def export_restaurants() -> list:

    """
    Excel生成restaurants.json
    """


    df = pd.read_excel(
        RESTAURANT_EXCEL
    )



    restaurants = []



    for _, row in df.iterrows():


        item = {


            "id":

                int(row["restaurant_id"]),



            "name":

                str(row["name"]),



            "district":

                str(row["district"]),



            "area":

                str(row.get(
                    "area",
                    ""
                )),



            "address":

                str(row.get(
                    "address",
                    ""
                )),



            "category":

                str(row["category"]),



            "price":

                int(row["price"]),



            "rating":

                float(row["rating"]),



            "couple_score":

                int(row["couple_score"]),



            "latitude":

                float(
                    row.get(
                        "latitude",
                        0
                    )
                ),



            "longitude":

                float(
                    row.get(
                        "longitude",
                        0
                    )
                ),



            "business_hours":

                str(
                    row.get(
                        "business_hours",
                        ""
                    )
                ),



            "source":

                str(
                    row.get(
                        "source",
                        ""
                    )
                ),



            "update_date":

                str(
                    row.get(
                        "update_date",
                        datetime.now()
                    )
                )

        }



        restaurants.append(
            item
        )



    save_json(
        RESTAURANT_JSON,
        restaurants
    )



    return restaurants







# =====================================================
# 生成菜品JSON
# =====================================================


def export_dishes() -> list:

    """
    Excel生成dishes.json
    """


    df = pd.read_excel(
        DISH_EXCEL
    )



    dishes = []



    for index, row in df.iterrows():


        item = {


            "id":

                int(row["dish_id"]),



            "restaurant_id":

                int(
                    row["restaurant_id"]
                ),



            "name":

                str(
                    row["dish_name"]
                ),



            "meal":

                [
                    str(
                        row["meal_type"]
                    )
                ],



            "recommend":

                bool(
                    row.get(
                        "recommend",
                        True
                    )
                ),



            "tags":

                str(
                    row.get(
                        "tags",
                        ""
                    )
                ).split(";"),



            "reason":

                str(
                    row.get(
                        "reason",
                        ""
                    )
                ),



            "source":

                str(
                    row.get(
                        "source",
                        ""
                    )
                )

        }



        dishes.append(
            item
        )



    save_json(
        DISH_JSON,
        dishes
    )


    return dishes







# =====================================================
# 生成推荐关系表
# =====================================================


def export_food(
        restaurants:list,
        dishes:list
):

    """
    生成food.json
    """


    restaurant_ids = {

        item["id"]

        for item in restaurants

    }



    food = []



    for index, dish in enumerate(
        dishes
    ):


        if (
            dish["restaurant_id"]
            not in restaurant_ids
        ):

            continue



        item = {


            "id":

                30000 + index + 1,



            "restaurant_id":

                dish["restaurant_id"],



            "dish_id":

                dish["id"],



            "meal":

                dish["meal"],



            "reason":

                dish["reason"],



            "tags":

                dish["tags"]

        }



        food.append(
            item
        )



    save_json(
        FOOD_JSON,
        food
    )



    return food







# =====================================================
# 主程序
# =====================================================


def main():


    print(
        "="*50
    )


    print(
        "广州美食数据库 JSON生成工具 V2.1"
    )


    print(
        "="*50
    )



    restaurants = (

        export_restaurants()

    )



    print(
        f"✅ restaurants.json: {len(restaurants)}"
    )



    dishes = (

        export_dishes()

    )



    print(
        f"✅ dishes.json: {len(dishes)}"
    )



    food = export_food(
        restaurants,
        dishes
    )



    print(
        f"✅ food.json: {len(food)}"
    )



    print(
        "\n🎉 JSON生成完成"
    )





if __name__ == "__main__":

    main()