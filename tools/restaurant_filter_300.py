"""
广州300家餐厅筛选工具

restaurant_filter_300.py
V1.4.4 Final Frozen Stable


Input:
source/restaurant_raw_amap.xlsx


Output:
source/restaurant_raw_300.xlsx


Frozen Logic:

1. Keep AMAP POI order
2. Clean invalid data
3. Normalize brand
4. Max 3 restaurants per brand
5. Fill remaining records to 300


No:
- area optimization
- score ranking
- category weighting
"""


from pathlib import Path
from datetime import datetime

import pandas as pd



# ==================================================
# Path
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_DIR = BASE_DIR / "source"


INPUT_FILE = (
    SOURCE_DIR /
    "restaurant_raw_amap.xlsx"
)


OUTPUT_FILE = (
    SOURCE_DIR /
    "restaurant_raw_300.xlsx"
)



# ==================================================
# Config
# ==================================================

TARGET_COUNT = 300

MAX_BRAND_COUNT = 3



# ==================================================
# Brand
# ==================================================

def normalize_brand(name):

    name = str(name).strip()


    for sep in [

        "(",
        "（",
        "·",
        "-"

    ]:

        if sep in name:

            name = name.split(sep)[0]


    return name.strip()



# ==================================================
# Clean
# ==================================================

def clean_data(df):

    df = df.copy()


    # name

    df = df[
        df["name"].notna()
    ]


    df = df[
        ~df["name"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(
            [
                "",
                "nan",
                "none"
            ]
        )
    ]



    # address

    df = df[
        df["address"].notna()
    ]


    df = df[
        ~df["address"]
        .astype(str)
        .str.strip()
        .str.lower()
        .isin(
            [
                "",
                "nan",
                "none"
            ]
        )
    ]



    # coordinate

    if "longitude" in df.columns:

        df = df[
            df["longitude"].notna()
        ]


    if "latitude" in df.columns:

        df = df[
            df["latitude"].notna()
        ]



    # duplicate

    df = df.drop_duplicates(

        subset=[

            "name",

            "address"

        ]

    )



    df = df.reset_index(
        drop=True
    )


    df["brand"] = (
        df["name"]
        .apply(normalize_brand)
    )


    return df



# ==================================================
# Brand Limit
# ==================================================

def limit_brand(df):


    selected_rows = []

    brand_count = {}



    # 第一轮：
    # 每品牌最多3家


    for _, row in df.iterrows():


        brand = row["brand"]


        count = brand_count.get(

            brand,

            0

        )


        if count >= MAX_BRAND_COUNT:

            continue



        selected_rows.append(
            row
        )


        brand_count[brand] = count + 1



        if len(selected_rows) >= TARGET_COUNT:

            break



    selected = pd.DataFrame(
        selected_rows
    )



    # 第二轮补足

    if len(selected) < TARGET_COUNT:


        remain = TARGET_COUNT - len(selected)


        selected_names = set(

            selected["name"].tolist()

        )


        extra = df[

            ~df["name"]

            .isin(selected_names)

        ]



        selected = pd.concat(

            [

                selected,

                extra.head(remain)

            ],

            ignore_index=True

        )



    return selected.reset_index(
        drop=True
    )



# ==================================================
# Format
# ==================================================

def format_output(df):


    result = pd.DataFrame()



    result["id"] = range(

        1,

        len(df)+1

    )


    fields = [

        "name",

        "district",

        "address",

        "category",

        "longitude",

        "latitude"

    ]



    for field in fields:


        if field in df.columns:

            result[field] = df[field]

        else:

            result[field] = ""



    result["area"] = ""

    result["price"] = ""

    result["rating"] = ""

    result["taste_score"] = ""

    result["environment_score"] = ""

    result["couple_score"] = ""

    result["business_hours"] = ""

    result["map_url"] = ""

    result["navigation_url"] = ""

    result["source"] = "AMAP POI"

    result["remark"] = ""

    result["status"] = "待处理"



    return result.fillna("")



# ==================================================
# Main
# ==================================================

def main():


    print("=" * 60)

    print(
        "广州餐厅300家筛选工具 V1.4.4 Final Frozen Stable"
    )

    print("=" * 60)



    df = pd.read_excel(
        INPUT_FILE
    )



    print()

    print(
        "原始数量:",
        len(df)
    )



    df = clean_data(df)



    print(
        "清洗后:",
        len(df)
    )



    df = limit_brand(df)



    print(
        "品牌限制后:",
        len(df)
    )



    result = format_output(df)



    # 只做空值安全检查，不删除有效记录

    result["name"] = (

        result["name"]

        .astype(str)

        .str.strip()

    )



    if len(result) < TARGET_COUNT:

        print(
            "警告: 数据不足300条"
        )



    result = result.head(
        TARGET_COUNT
    )



    result.to_excel(

        OUTPUT_FILE,

        index=False

    )



    print()

    print(
        "最终数量:",
        len(result)
    )


    print(
        "空名称:",
        (
            result["name"]
            .eq("")
        )
        .sum()
    )


    print()

    print(
        "输出:",
        OUTPUT_FILE
    )


    print(
        "更新时间:",
        datetime.now()
    )



if __name__ == "__main__":

    main()