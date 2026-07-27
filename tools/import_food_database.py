"""
广州美食数据库导入工具 V2.3

功能:
1. 读取真实广州美食数据库 Excel
2. 校验数据库结构
3. 转换 JSON 数据
4. 支持地图字段

Input:
source/guangzhou_food_real_database.xlsx

Output:
data/
    restaurants.json
    dishes.json
    food.json
    tags.json

Python:
3.12+
"""


from pathlib import Path
from datetime import datetime
import json


import pandas as pd



# =====================================================
# Project Path
# =====================================================


BASE_DIR = Path(__file__).resolve().parent.parent



# 真实数据库

DATABASE_FILE = (

    BASE_DIR

    /

    "source"

    /

    "guangzhou_food_real_database.xlsx"

)



# JSON输出目录

DATA_DIR = (

    BASE_DIR

    /

    "data"

)


DATA_DIR.mkdir(
    exist_ok=True
)



# =====================================================
# Excel Sheet
# =====================================================


SHEET_RESTAURANTS = "restaurants"

SHEET_DISHES = "dishes"

SHEET_RELATION = "food_relation"




# =====================================================
# Required Columns
# =====================================================


RESTAURANT_COLUMNS = [

    "id",

    "name",

    "district",

    "category",

    "price",

    "rating",

    "couple_score",

    "taste_score",

    "environment_score",

    "business_hours",

    "address",

    "latitude",

    "longitude",

    "map_url"

]



DISH_COLUMNS = [

    "id",

    "name",

    "meal",

    "category",

    "type",

    "tags",

    "description"

]



RELATION_COLUMNS = [

    "id",

    "restaurant_id",

    "dish_id",

    "meal",

    "tags",

    "reason"

]





# =====================================================
# Load Excel
# =====================================================


def load_database():

    """
    读取Excel数据库
    """

    if not DATABASE_FILE.exists():

        raise FileNotFoundError(

            f"数据库不存在: {DATABASE_FILE}"

        )


    excel = pd.ExcelFile(
        DATABASE_FILE
    )


    restaurants = pd.read_excel(

        excel,

        sheet_name=SHEET_RESTAURANTS

    )


    dishes = pd.read_excel(

        excel,

        sheet_name=SHEET_DISHES

    )


    relations = pd.read_excel(

        excel,

        sheet_name=SHEET_RELATION

    )


    return (

        restaurants,

        dishes,

        relations

    )




# =====================================================
# Validate Sheet
# =====================================================


def validate_columns(
        dataframe,
        required,
        sheet_name
):


    missing = [

        col

        for col in required

        if col not in dataframe.columns

    ]


    if missing:

        raise ValueError(

            f"{sheet_name} 缺少字段: {missing}"

        )


    print(

        f"{sheet_name} 字段检查通过"

    )





# =====================================================
# Data Cleaning
# =====================================================


def clean_value(value):

    """
    清理Excel空值
    """

    if pd.isna(value):

        return ""


    return value





# =====================================================
# Convert Restaurants
# =====================================================


def convert_restaurants(df):


    result = []


    for _, row in df.iterrows():


        result.append({

            "id":

                int(
                    row["id"]
                ),


            "name":

                clean_value(
                    row["name"]
                ),


            "district":

                clean_value(
                    row["district"]
                ),


            "category":

                clean_value(
                    row["category"]
                ),


            "price":

                int(
                    row["price"]
                ),


            "rating":

                float(
                    row["rating"]
                ),


            "couple_score":

                int(
                    row["couple_score"]
                ),


            "taste_score":

                int(
                    row["taste_score"]
                ),


            "environment_score":

                int(
                    row["environment_score"]
                ),


            "business_hours":

                clean_value(
                    row["business_hours"]
                ),


            "address":

                clean_value(
                    row["address"]
                ),


            "latitude":

                clean_value(
                    row["latitude"]
                ),


            "longitude":

                clean_value(
                    row["longitude"]
                ),


            "map_url":

                clean_value(
                    row["map_url"]
                )

        })


    return result





# =====================================================
# Convert Dishes
# =====================================================


def convert_dishes(df):


    result = []


    for _, row in df.iterrows():


        result.append({

            "id":

                int(
                    row["id"]
                ),


            "name":

                clean_value(
                    row["name"]
                ),


            "meal":

                clean_value(
                    row["meal"]
                ),


            "category":

                clean_value(
                    row["category"]
                ),


            "type":

                clean_value(
                    row["type"]
                ),


            "tags":

                clean_value(
                    row["tags"]
                ),


            "description":

                clean_value(
                    row["description"]
                )

        })


    return result




# =====================================================
# Convert Relations
# =====================================================


def convert_relations(df):


    result=[]


    for _, row in df.iterrows():


        result.append({

            "id":

                int(
                    row["id"]
                ),


            "restaurant_id":

                int(
                    row["restaurant_id"]
                ),


            "dish_id":

                int(
                    row["dish_id"]
                ),


            "meal":

                clean_value(
                    row["meal"]
                ),


            "tags":

                clean_value(
                    row["tags"]
                ),


            "reason":

                clean_value(
                    row["reason"]
                )

        })


    return result

# =====================================================
# Save JSON
# =====================================================


def save_json(
        filename,
        data
):
    """
    保存JSON文件
    """

    output = (

        DATA_DIR

        /

        filename

    )


    with open(

        output,

        "w",

        encoding="utf-8"

    ) as f:


        json.dump(

            data,

            f,

            ensure_ascii=False,

            indent=4

        )


    print(

        f"✅ {filename}: {len(data)}"

    )




# =====================================================
# Generate Tags
# =====================================================


def generate_tags(
        relations
):

    """
    提取标签库
    """

    tags = set()


    for item in relations:


        value = item.get(
            "tags",
            ""
        )


        if not value:

            continue



        for tag in value.replace(
            "|",
            ","
        ).split(","):


            tag = tag.strip()


            if tag:

                tags.add(tag)



    return sorted(
        list(tags)
    )




# =====================================================
# Database Statistics
# =====================================================


def print_statistics(
        dishes
):


    meal_count = {}


    for item in dishes:


        meal = item.get(
            "meal",
            "未知"
        )


        meal_count[meal] = (

            meal_count.get(
                meal,
                0
            )

            +

            1

        )



    print()

    print(
        "数据库统计:"
    )


    for meal,count in meal_count.items():

        print(

            f"{meal}: {count}"

        )


    print(

        f"总数据: {len(dishes)}"

    )




# =====================================================
# Main
# =====================================================


def main():


    print(
        "=" * 50
    )


    print(
        "广州美食数据库导入工具 V2.3"
    )


    print(
        "=" * 50
    )



    print()


    print(
        "数据库:"
    )


    print(
        DATABASE_FILE
    )



    print()



    # -------------------------------
    # Load Excel
    # -------------------------------


    (
        restaurants_df,

        dishes_df,

        relations_df

    ) = load_database()



    # -------------------------------
    # Validate
    # -------------------------------


    validate_columns(

        restaurants_df,

        RESTAURANT_COLUMNS,

        SHEET_RESTAURANTS

    )


    validate_columns(

        dishes_df,

        DISH_COLUMNS,

        SHEET_DISHES

    )


    validate_columns(

        relations_df,

        RELATION_COLUMNS,

        SHEET_RELATION

    )



    print()



    # -------------------------------
    # Convert
    # -------------------------------


    restaurants = convert_restaurants(

        restaurants_df

    )


    dishes = convert_dishes(

        dishes_df

    )


    relations = convert_relations(

        relations_df

    )



    # -------------------------------
    # Save JSON
    # -------------------------------


    save_json(

        "restaurants.json",

        restaurants

    )


    save_json(

        "dishes.json",

        dishes

    )


    save_json(

        "food.json",

        relations

    )



    tags = generate_tags(

        relations

    )


    save_json(

        "tags.json",

        tags

    )



    # -------------------------------
    # Statistics
    # -------------------------------


    print_statistics(

        dishes

    )



    print()


    print(
        "🎉 数据库导入完成"
    )


    print(

        "更新时间:",

        datetime.now()

    )




# =====================================================
# Entry
# =====================================================


if __name__ == "__main__":

    main()