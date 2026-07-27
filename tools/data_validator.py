"""
Guangzhou Food Draw V2.0

Excel Data Validator V2.1

功能:
1. 校验餐厅Excel
2. 校验菜品Excel
3. 检查重复ID
4. 检查字段完整性
5. 检查关联关系
6. 输出校验报告

Python:
3.12+

依赖:
pandas
openpyxl
"""

from pathlib import Path
from typing import List, Tuple
from datetime import datetime

import pandas as pd

# =====================================================
# 路径配置
# =====================================================


BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_DIR = BASE_DIR / "source"

OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(
    exist_ok=True
)

RESTAURANT_FILE = (
        SOURCE_DIR /
        "restaurants_source.xlsx"
)

DISH_FILE = (
        SOURCE_DIR /
        "dishes_source.xlsx"
)

REPORT_FILE = (
        OUTPUT_DIR /
        "validation_report.txt"
)


# =====================================================
# 通用检查
# =====================================================


def check_file_exists(
        file_path: Path
):
    """
    检查文件是否存在
    """

    if not file_path.exists():
        raise FileNotFoundError(
            f"文件不存在: {file_path}"
        )


def check_required_columns(
        df: pd.DataFrame,
        required: List[str],
        name: str
) -> List[str]:
    """
    检查必填字段
    """

    errors = []

    for column in required:

        if column not in df.columns:
            errors.append(
                f"{name} 缺少字段: {column}"
            )

    return errors


def check_duplicate_id(
        df: pd.DataFrame,
        column: str,
        name: str
) -> List[str]:
    """
    检查重复ID
    """

    errors = []

    duplicate = df[
        df[column]
        .duplicated(False)
    ]

    if not duplicate.empty:
        ids = (
            duplicate[column]
            .tolist()
        )

        errors.append(
            f"{name}存在重复ID: {ids}"
        )

    return errors


# =====================================================
# 餐厅数据检查
# =====================================================


def validate_restaurants(
) -> Tuple[pd.DataFrame, List[str]]:
    """
    校验餐厅数据
    """

    errors = []

    check_file_exists(
        RESTAURANT_FILE
    )

    df = pd.read_excel(
        RESTAURANT_FILE
    )

    required = [

        "restaurant_id",

        "name",

        "district",

        "category",

        "price",

        "rating",

        "couple_score"

    ]

    errors += check_required_columns(
        df,
        required,
        "restaurants"
    )

    if errors:
        return df, errors

    # 数据类型转换

    df["restaurant_id"] = (
        pd.to_numeric(
            df["restaurant_id"],
            errors="coerce"
        )
    )

    if df["restaurant_id"].isna().any():
        errors.append(
            "restaurant_id存在非法值"
        )

    df["rating"] = (
        pd.to_numeric(
            df["rating"],
            errors="coerce"
        )
    )

    df["couple_score"] = (
        pd.to_numeric(
            df["couple_score"],
            errors="coerce"
        )
    )

    # 空值检查

    for column in required:

        if df[column].isna().any():
            errors.append(
                f"{column}存在空值"
            )

    # ID检查

    errors += check_duplicate_id(
        df,
        "restaurant_id",
        "restaurants"
    )

    # 评分检查

    invalid_rating = df[
        (df["rating"] < 0)
        |
        (df["rating"] > 5)
        ]

    if not invalid_rating.empty:
        errors.append(
            "rating必须在0-5范围"
        )

    # 情侣评分检查

    invalid_couple = df[
        (df["couple_score"] < 1)
        |
        (df["couple_score"] > 5)
        ]

    if not invalid_couple.empty:
        errors.append(
            "couple_score必须在1-5范围"
        )

    return df, errors


# =====================================================
# 菜品数据检查
# =====================================================


def validate_dishes(
        restaurant_ids: set
) -> Tuple[pd.DataFrame, List[str]]:
    """
    校验菜品数据
    """

    errors = []

    check_file_exists(
        DISH_FILE
    )

    df = pd.read_excel(
        DISH_FILE
    )

    required = [

        "dish_id",

        "restaurant_id",

        "dish_name",

        "meal_type"

    ]

    errors += check_required_columns(
        df,
        required,
        "dishes"
    )

    if errors:
        return df, errors

    df["dish_id"] = (
        pd.to_numeric(
            df["dish_id"],
            errors="coerce"
        )
    )

    df["restaurant_id"] = (
        pd.to_numeric(
            df["restaurant_id"],
            errors="coerce"
        )
    )

    errors += check_duplicate_id(
        df,
        "dish_id",
        "dishes"
    )

    # 外键检查

    invalid_relation = (

        ~df["restaurant_id"]
        .isin(
            restaurant_ids
        )

    )

    if invalid_relation.any():
        ids = (
            df.loc[
                invalid_relation,
                "restaurant_id"
            ]
            .tolist()
        )

        errors.append(
            f"不存在restaurant_id: {ids}"
        )

    # 餐次检查

    valid_meal = {

        "早餐",

        "午餐",

        "晚餐"

    }

    invalid_meal = (

        ~df["meal_type"]
        .isin(valid_meal)

    )

    if invalid_meal.any():
        errors.append(
            "meal_type只能为早餐/午餐/晚餐"
        )

    return df, errors


# =====================================================
# 报告生成
# =====================================================


def write_report(
        messages: List[str]
):
    """
    输出校验报告
    """

    with open(
            REPORT_FILE,
            "w",
            encoding="utf-8"
    ) as file:

        file.write(
            "广州美食数据库校验报告\n"
        )

        file.write(
            "=" * 40
            +
            "\n"
        )

        file.write(
            f"时间: {datetime.now()}\n\n"
        )

        if messages:

            file.write(
                "发现问题:\n\n"
            )

            for msg in messages:
                file.write(
                    "❌ "
                    +
                    msg
                    +
                    "\n"
                )


        else:

            file.write(
                "✅ 所有数据校验通过\n"
            )


# =====================================================
# 主程序
# =====================================================


def main():
    print(
        "=" * 50
    )

    print(
        "广州美食数据库校验工具 V2.1"
    )

    print(
        "=" * 50
    )

    errors = []

    try:

        restaurant_df, restaurant_errors = (
            validate_restaurants()
        )

        errors += restaurant_errors

        if not restaurant_errors:

            print(
                "✅ restaurants_source.xlsx 校验通过"
            )

            restaurant_ids = set(

                restaurant_df[
                    "restaurant_id"
                ]
                .astype(int)

            )

            _, dish_errors = validate_dishes(
                restaurant_ids
            )

            errors += dish_errors

            if not dish_errors:
                print(
                    "✅ dishes_source.xlsx 校验通过"
                )



    except Exception as e:

        errors.append(
            str(e)
        )

    # 统计

    if not errors:

        print("\n🎉 所有数据校验通过")


    else:

        print("\n发现错误:")

        for error in errors:
            print(
                "❌",
                error
            )

    write_report(
        errors
    )

    print(
        f"\n报告文件: {REPORT_FILE}"
    )


if __name__ == "__main__":
    main()