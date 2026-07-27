"""
广州美食 JSON 导出工具

Version:
Sprint 3 Part 1.5.12.1
export_json.py V1.2 Metadata Complete Stable

Input:
source/restaurant_source_geocoded.xlsx

Output:
data/food.json
"""


from pathlib import Path
from datetime import datetime
import json

import pandas as pd


# ==================================================
# Path Configuration
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent


INPUT_FILE = (
    BASE_DIR
    /
    "source"
    /
    "restaurant_source_geocoded.xlsx"
)


OUTPUT_FILE = (
    BASE_DIR
    /
    "data"
    /
    "food.json"
)



# ==================================================
# Metadata Generator
# ==================================================

def generate_metadata(row: dict) -> dict:
    """
    Generate front-end display metadata.
    """

    name = (
        str(row.get("name"))
        if row.get("name")
        else ""
    )


    category = (
        str(row.get("category"))
        if row.get("category")
        else "特色餐饮"
    )


    return {

        # 价格区间
        "price":
            "¥50-100",


        # 推荐评分
        "rating":
            4.5,


        # 情侣指数
        "couple_score":
            80,


        # 营业时间
        "business_hours":
            "11:00-22:00",


        # 推荐理由
        "reason":
            (
                f"{name}，"
                f"{category}特色餐厅，"
                "广州本地美食推荐，"
                "适合朋友聚餐和日常用餐"
            )
    }



# ==================================================
# Safe Convert
# ==================================================

def safe_value(value):
    """
    Convert pandas NaN to None.
    """

    if pd.isna(value):
        return None

    return value



# ==================================================
# Main
# ==================================================

def main():

    print("=" * 60)

    print(
        "广州美食JSON导出工具 V1.2 Metadata Complete Stable"
    )

    print("=" * 60)



    # -----------------------------
    # Read Excel
    # -----------------------------

    if not INPUT_FILE.exists():

        raise FileNotFoundError(
            f"文件不存在: {INPUT_FILE}"
        )


    df = pd.read_excel(
        INPUT_FILE
    )


    print(
        f"\n读取数量: {len(df)}"
    )



    records = []



    # -----------------------------
    # Convert
    # -----------------------------

    for _, row in df.iterrows():


        item = {}


        export_fields = [

            "id",
            "name",
            "district",
            "address",
            "category",
            "longitude",
            "latitude",
            "navigation_url",
            "source"

        ]


        for field in export_fields:

            if field in df.columns:

                item[field] = safe_value(
                    row[field]
                )



        # Add metadata

        item.update(
            generate_metadata(
                row.to_dict()
            )
        )



        records.append(
            item
        )



    # -----------------------------
    # Remove invalid data
    # -----------------------------

    records = [

        item

        for item in records

        if item.get("name")

    ]


    print(
        f"有效数量: {len(records)}"
    )



    # -----------------------------
    # Export JSON
    # -----------------------------

    OUTPUT_FILE.parent.mkdir(
        exist_ok=True
    )


    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(

            records,

            f,

            ensure_ascii=False,

            indent=4

        )



    print(
        "\nJSON输出:"
    )

    print(
        OUTPUT_FILE
    )


    print(
        "\n更新时间:",
        datetime.now()
    )



# ==================================================
# Entry
# ==================================================

if __name__ == "__main__":

    main()