"""
广州真实餐厅数据整理工具

generate_real_restaurant_data.py V2.0

功能:
1. 读取真实餐厅原始数据
2. 标准化字段
3. 输出地理编码输入文件

Input:
source/restaurant_raw_300.xlsx

Output:
source/restaurant_source_300.xlsx


Compatible:
batch_geocode_restaurants.py V2.1
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
    "restaurant_raw_300.xlsx"
)


OUTPUT_FILE = (
    SOURCE_DIR /
    "restaurant_source_300.xlsx"
)



# ==================================================
# Columns
# ==================================================

OUTPUT_COLUMNS = [

    "id",

    "name",

    "district",

    "area",

    "category",

    "price",

    "rating",

    "taste_score",

    "environment_score",

    "couple_score",

    "business_hours",

    "address",

    "latitude",

    "longitude",

    "map_url",

    "navigation_url",

    "source",

    "remark",

    "status"

]



# ==================================================
# Process
# ==================================================


def process_data(df):


    result = pd.DataFrame()



    for col in OUTPUT_COLUMNS:

        if col in df.columns:

            result[col] = df[col]

        else:

            result[col] = ""



    # ID重新编号

    result["id"] = range(
        1,
        len(result)+1
    )



    # 默认状态

    result["status"] = (
        result["status"]
        .replace(
            "",
            "待编码"
        )
    )



    return result



# ==================================================
# Main
# ==================================================


def main():


    print("="*60)

    print(
        "广州真实餐厅数据整理工具 V2.0"
    )

    print("="*60)



    if not INPUT_FILE.exists():

        raise FileNotFoundError(

            f"缺少输入文件:\n{INPUT_FILE}"

        )



    df = pd.read_excel(
        INPUT_FILE
    )



    print()

    print(
        "读取数据:",
        len(df)
    )



    result = process_data(
        df
    )



    result.to_excel(

        OUTPUT_FILE,

        index=False

    )



    print()

    print(
        "输出:",
        OUTPUT_FILE
    )


    print()

    print(
        "餐厅数量:",
        len(result)
    )


    print(
        "更新时间:",
        datetime.now()
    )


    print()

    print(
        "数据整理完成"
    )



if __name__ == "__main__":

    main()