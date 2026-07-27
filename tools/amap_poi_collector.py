"""
广州餐厅高德POI采集工具

amap_poi_collector.py V1.0

功能:
1. 高德POI关键词搜索
2. 自动分页
3. 自动去重
4. 输出Excel

Output:
source/restaurant_raw_amap.xlsx

"""


from pathlib import Path
import sys
import requests
import pandas as pd
import time



# ==================================================
# Project Path
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(
    str(BASE_DIR)
)


SOURCE_DIR = BASE_DIR / "source"


OUTPUT_FILE = (
    SOURCE_DIR /
    "restaurant_raw_amap.xlsx"
)



# ==================================================
# Config
# ==================================================

from config.amap_config import (
    AMAP_KEY
)



AMAP_POI_URL = (

    "https://restapi.amap.com/v5/place/text"

)



CITY = "广州"



KEYWORDS = [

    "粤菜",

    "早茶",

    "广州菜",

    "茶餐厅",

    "甜品",

    "小吃",

    "火锅",

    "烧腊",

    "潮汕菜"

]



PAGE_SIZE = 25


MAX_PAGE = 5



REQUEST_INTERVAL = 0.5



# ==================================================
# POI Search
# ==================================================


def search_poi(keyword,page):


    params = {

        "key":
            AMAP_KEY,

        "keywords":
            keyword,

        "city":
            CITY,

        "citylimit":
            "true",

        "page_size":
            PAGE_SIZE,

        "page_num":
            page,

        "output":
            "json"

    }



    response = requests.get(

        AMAP_POI_URL,

        params=params,

        timeout=10

    )


    data=response.json()


    if data.get("status")!="1":

        return []



    pois=data.get(
        "pois",
        []
    )


    return pois



# ==================================================
# Parse
# ==================================================


def parse_poi(
        poi,
        keyword
):


    location = poi.get(
        "location",
        ""
    )


    longitude=""

    latitude=""


    if location:

        lng,lat=location.split(",")

        longitude=lng

        latitude=lat



    return {

        "name":
            poi.get(
                "name",
                ""
            ),


        "address":
            poi.get(
                "address",
                ""
            ),


        "district":
            poi.get(
                "adname",
                ""
            ),


        "category":
            poi.get(
                "type",
                ""
            ),


        "longitude":
            longitude,


        "latitude":
            latitude,


        "tel":
            poi.get(
                "tel",
                ""
            ),


        "type":
            poi.get(
                "typecode",
                ""
            ),


        "keyword":
            keyword,


        "source":
            "AMAP POI"

    }



# ==================================================
# Main
# ==================================================


def main():


    print("="*60)

    print(
        "广州餐厅高德POI采集工具 V1.0"
    )

    print("="*60)



    SOURCE_DIR.mkdir(
        exist_ok=True
    )



    records=[]


    seen=set()



    for keyword in KEYWORDS:


        print()

        print(
            "搜索:",
            keyword
        )


        for page in range(
            1,
            MAX_PAGE+1
        ):


            print(
                f"第{page}页"
            )


            pois=search_poi(
                keyword,
                page
            )



            if not pois:

                break



            for poi in pois:


                name=poi.get(
                    "name",
                    ""
                )


                if not name:

                    continue



                # 去重

                if name in seen:

                    continue



                seen.add(
                    name
                )


                records.append(

                    parse_poi(

                        poi,

                        keyword

                    )

                )



            time.sleep(
                REQUEST_INTERVAL
            )



    df=pd.DataFrame(
        records
    )


    df.insert(
        0,
        "id",
        range(
            1,
            len(df)+1
        )
    )



    df.to_excel(

        OUTPUT_FILE,

        index=False

    )



    print()

    print("="*60)

    print(
        "采集完成"
    )

    print("="*60)



    print(
        "餐厅数量:",
        len(df)
    )


    print(
        "输出:",
        OUTPUT_FILE
    )



if __name__=="__main__":

    main()