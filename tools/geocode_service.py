"""
广州美食地址自动地理编码工具 V1.2 Stable

功能:
1. Excel地址批量转换经纬度
2. 高德Geocoding API
3. 自动生成地图链接
4. 支持已有坐标
5. 输出失败清单
6. 支持300+餐厅批处理


输入:

source/
└── restaurant_source.xlsx


输出:

source/
├── restaurant_source_geocoded.xlsx
└── geocode_failed.xlsx


Python:
3.12+
"""


from pathlib import Path
import sys
import time


import pandas as pd
import requests



# =====================================================
# Project Path
# =====================================================


BASE_DIR = Path(__file__).resolve().parent.parent


sys.path.append(
    str(BASE_DIR)
)



from config.amap_config import (

    AMAP_KEY,

    AMAP_GEOCODE_URL,

    REQUEST_TIMEOUT,

    REQUEST_INTERVAL,

    MAX_RETRY

)



# =====================================================
# File Path
# =====================================================


SOURCE_DIR = BASE_DIR / "source"



INPUT_FILE = (
    SOURCE_DIR /
    "restaurant_source.xlsx"
)



OUTPUT_FILE = (
    SOURCE_DIR /
    "restaurant_source_geocoded.xlsx"
)



FAILED_FILE = (
    SOURCE_DIR /
    "geocode_failed.xlsx"
)




# =====================================================
# 地址解析
# =====================================================


def geocode_address(address: str):

    """
    高德地址解析

    Returns:

    latitude,
    longitude,
    message

    """


    if not address:

        return (
            None,
            None,
            "地址为空"
        )



    params = {

        "key": AMAP_KEY,

        "address": address,

        "output": "JSON"

    }



    for retry in range(MAX_RETRY):

        try:


            response = requests.get(

                AMAP_GEOCODE_URL,

                params=params,

                timeout=REQUEST_TIMEOUT

            )



            data = response.json()



            if data.get("status") != "1":


                return (

                    None,

                    None,

                    data.get(
                        "info",
                        "API失败"
                    )

                )



            geocodes = data.get(
                "geocodes",
                []
            )



            if not geocodes:


                return (

                    None,

                    None,

                    "未找到地址"

                )



            location = (

                geocodes[0]

                ["location"]

            )



            lng, lat = location.split(",")



            return (

                float(lat),

                float(lng),

                "自动编码成功"

            )



        except Exception as e:



            if retry == MAX_RETRY - 1:


                return (

                    None,

                    None,

                    str(e)

                )


            time.sleep(1)



    return (

        None,

        None,

        "未知错误"

    )





# =====================================================
# 高德地图链接
# =====================================================


def create_map_url(
    latitude,
    longitude,
    name=""
):
    """
    创建高德地图餐厅定位链接
    """

    from urllib.parse import quote

    url = (
        "https://uri.amap.com/marker?"
        f"position={longitude},{latitude}"
    )

    if name:
        url += (
            f"&name={quote(name)}"
        )

    return url

def create_navigation_url(
    latitude,
    longitude,
    name=""
):
    """
    创建高德地图导航链接
    """

    from urllib.parse import quote


    destination = (
        f"{longitude},{latitude}"
    )


    url = (
        "https://uri.amap.com/navigation?"
        f"to={destination}"
    )


    if name:

        url += (
            f"&name={quote(name)}"
        )


    return url




# =====================================================
# Excel处理
# =====================================================


def process():



    print("=" * 50)

    print(
        "广州美食地址自动地理编码工具 V1.2 Stable"
    )

    print("=" * 50)



    if not INPUT_FILE.exists():

        raise FileNotFoundError(

            f"未找到文件: {INPUT_FILE}"

        )



    df = pd.read_excel(

        INPUT_FILE

    )



    # -----------------------------
    # 强制文本字段
    # -----------------------------


    text_columns = [

        "name",

        "address",

        "map_url",

        "source",

        "remark"

    ]



    for col in text_columns:


        if col in df.columns:


            df[col] = (

                df[col]

                .fillna("")

                .astype(str)

            )



    # -----------------------------
    # 初始化字段
    # -----------------------------


    for col in [

        "latitude",

        "longitude"

    ]:


        if col not in df.columns:

            df[col] = None

    for col in [
        "map_url",
        "navigation_url",
        "remark"
    ]:


        if col not in df.columns:

            df[col] = ""



        df[col] = df[col].astype(object)



    total = len(df)



    auto_success = 0

    existing_coordinate = 0

    failed = []



    print(

        f"总数量:{total}"

    )



    print()



    # =================================================
    # Loop
    # =================================================


    for index,row in df.iterrows():



        name = str(

            row.get(

                "name",

                ""

            )

        ).strip()



        address = str(

            row.get(

                "address",

                ""

            )

        ).strip()



        # 空数据跳过

        if (

            not name

            or

            not address

        ):


            continue




        latitude = row.get(

            "latitude",

            ""

        )


        longitude = row.get(

            "longitude",

            ""

        )



        # ---------------------------------
        # 已有坐标
        # ---------------------------------


        if (

            str(latitude)

            not in [

                "",

                "nan",

                "None"

            ]

            and

            str(longitude)

            not in [

                "",

                "nan",

                "None"

            ]

        ):
            df.at[
                index,
                "navigation_url"
            ] = create_navigation_url(
                latitude,
                longitude,
                name
            )


            df.at[

                index,

                "remark"

            ] = (

                "已有坐标"

            )



            existing_coordinate += 1



            continue




        print(

            f"[{index+1}/{total}] {name}"

        )



        lat,lng,msg = geocode_address(

            address

        )



        if lat is not None:



            df.at[

                index,

                "latitude"

            ] = lat



            df.at[

                index,

                "longitude"

            ] = lng



            df.at[

                index,

                "map_url"

            ] = create_map_url(

                lat,

                lng

            )



            df.at[

                index,

                "remark"

            ] = msg



            auto_success += 1



        else:



            df.at[

                index,

                "remark"

            ] = msg



            failed.append(row)



        time.sleep(

            REQUEST_INTERVAL

        )




    # =================================================
    # 输出
    # =================================================


    df.to_excel(

        OUTPUT_FILE,

        index=False

    )



    if failed:


        pd.DataFrame(

            failed

        ).to_excel(

            FAILED_FILE,

            index=False

        )



    print()

    print("=" * 50)

    print(

        "处理完成"

    )

    print("=" * 50)



    print(

        f"已有坐标:{existing_coordinate}"

    )


    print(

        f"自动编码成功:{auto_success}"

    )


    print(

        f"失败:{len(failed)}"

    )



    completed = (

        existing_coordinate

        +

        auto_success

    )



    rate = (

        completed / total * 100

        if total

        else 0

    )



    print(

        f"完成率:{rate:.1f}%"

    )



    print()


    print(

        "输出:",

        OUTPUT_FILE

    )



    if failed:


        print(

            "失败清单:",

            FAILED_FILE

        )





# =====================================================
# Main
# =====================================================


if __name__ == "__main__":


    process()