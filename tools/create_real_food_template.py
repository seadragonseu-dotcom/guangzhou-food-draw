"""
广州真实美食采集模板生成工具

create_real_food_template.py V2.0

Generate:
1. restaurant_source_300.xlsx
2. dishes_source_300.xlsx

Compatible:
merge_real_food_database.py V1.1
export_json.py V2.7
"""


from pathlib import Path
from datetime import datetime

import pandas as pd



# ==================================================
# Path
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_DIR = BASE_DIR / "source"



# ==================================================
# Config
# ==================================================

RESTAURANT_COUNT = 300



# ==================================================
# Restaurant Template
# ==================================================


def create_restaurant_template():


    data=[]


    for i in range(1, RESTAURANT_COUNT + 1):


        data.append(

            {

                "id": i,

                "name": "",

                "district": "",

                "area": "",

                "category": "",

                "price": "",

                "rating": "",

                "taste_score": "",

                "environment_score": "",

                "couple_score": "",

                "business_hours": "",

                "address": "",

                "latitude": "",

                "longitude": "",

                "map_url": "",

                "source": "",

                "remark": "",

                "status": "待采集"

            }

        )


    return pd.DataFrame(data)



# ==================================================
# Dish Template
# ==================================================


def create_dish_template():


    data=[]


    dish_id=1


    for restaurant_id in range(
            1,
            RESTAURANT_COUNT + 1
    ):


        for index in range(1,6):


            data.append(

                {

                    "id":
                        dish_id,


                    "restaurant_id":
                        restaurant_id,


                    "restaurant":
                        "",


                    "name":
                        "",


                    "type":
                        "",


                    "category":
                        "",


                    "tags":
                        "",


                    "description":
                        "",


                    "recommend":
                        ""

                }

            )


            dish_id += 1



    return pd.DataFrame(data)



# ==================================================
# Export
# ==================================================


def main():


    print("="*60)

    print(
        "广州300家真实美食采集模板生成工具 V2.0"
    )

    print("="*60)



    SOURCE_DIR.mkdir(
        exist_ok=True
    )



    restaurants = (
        create_restaurant_template()
    )


    dishes = (
        create_dish_template()
    )



    restaurant_file = (
        SOURCE_DIR /
        "restaurant_source_300.xlsx"
    )


    dish_file = (
        SOURCE_DIR /
        "dishes_source_300.xlsx"
    )



    restaurants.to_excel(

        restaurant_file,

        index=False

    )



    dishes.to_excel(

        dish_file,

        index=False

    )



    print()

    print(
        "餐厅数量:",
        len(restaurants)
    )


    print(
        "菜品数量:",
        len(dishes)
    )


    print()

    print(
        "输出:"
    )

    print(
        restaurant_file
    )

    print(
        dish_file
    )


    print()

    print(
        "更新时间:",
        datetime.now()
    )


    print()

    print(
        "模板生成完成"
    )



if __name__ == "__main__":

    main()