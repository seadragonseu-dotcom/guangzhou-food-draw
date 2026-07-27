"""
广州300家餐厅批量地理编码工具

batch_geocode_restaurants.py V2.1 Stable


Input:
source/restaurant_raw_300.xlsx


Output:
source/restaurant_source_geocoded.xlsx


"""

from pathlib import Path
from datetime import datetime
from urllib.parse import quote

import sys
import time
import requests
import pandas as pd



# ==================================================
# Project Path
# ==================================================

BASE_DIR = Path(__file__).resolve().parent.parent

sys.path.append(
    str(BASE_DIR)
)



SOURCE_DIR = BASE_DIR / "source"



INPUT_FILE = (
    SOURCE_DIR /
    "restaurant_raw_300.xlsx"
)


OUTPUT_FILE = (
    SOURCE_DIR /
    "restaurant_source_geocoded.xlsx"
)


FAILED_FILE = (
    SOURCE_DIR /
    "geocode_failed.xlsx"
)



# ==================================================
# Config
# ==================================================

from config.amap_config import (
    AMAP_KEY
)


AMAP_URL = (
    "https://restapi.amap.com/v3/geocode/geo"
)


REQUEST_TIMEOUT = 10


MAX_RETRY = 3


REQUEST_INTERVAL = 0.3



# ==================================================
# Coordinate
# ==================================================

def has_coordinate(row):

    lat = row.get(
        "latitude"
    )

    lng = row.get(
        "longitude"
    )


    if pd.isna(lat):

        return False


    if pd.isna(lng):

        return False


    if str(lat).strip()=="":
        return False


    if str(lng).strip()=="":
        return False


    return True



# ==================================================
# URL
# ==================================================

def create_map_url(
        lng,
        lat,
        name
):

    return (

        "https://uri.amap.com/marker?"

        f"position={lng},{lat}"

        f"&name={quote(str(name))}"

    )



def create_navigation_url(
        lng,
        lat,
        name
):

    return (

        "https://uri.amap.com/navigation?"

        f"to={lng},{lat},{quote(str(name))}"

        "&mode=car"

    )



# ==================================================
# Amap
# ==================================================

def geocode_address(
        address
):

    if not address:

        return None



    params = {

        "key":
            AMAP_KEY,

        "address":
            address,

        "city":
            "广州",

        "output":
            "json"

    }



    for i in range(MAX_RETRY):


        try:


            r=requests.get(

                AMAP_URL,

                params=params,

                timeout=REQUEST_TIMEOUT

            )


            data=r.json()



            if data.get(
                "status"
            )!="1":

                continue



            items=data.get(
                "geocodes",
                []
            )



            if not items:

                continue



            location=items[0].get(
                "location"
            )



            if location:


                lng,lat=location.split(",")


                return {

                    "longitude":
                        float(lng),

                    "latitude":
                        float(lat)

                }



        except Exception:


            time.sleep(1)



    return None



# ==================================================
# Main
# ==================================================

def main():


    print("="*60)

    print(
        "广州300家餐厅批量地理编码工具 V2.1 Stable"
    )

    print("="*60)



    df=pd.read_excel(
        INPUT_FILE
    )



    # 字段补齐

    for col in [

        "map_url",

        "navigation_url",

        "remark"

    ]:


        if col not in df.columns:

            df[col]=""



        df[col]=df[col].astype(object)



    total=len(df)


    success=0

    existed=0

    failed=[]



    print()

    print(
        "总数量:",
        total
    )



    for index,row in df.iterrows():


        name=str(
            row.get(
                "name",
                ""
            )
        )



        print(
            f"[{index+1}/{total}] {name}"
        )



        if has_coordinate(row):


            existed+=1


            lng=row["longitude"]

            lat=row["latitude"]



        else:


            result=geocode_address(

                row.get(
                    "address",
                    ""
                )

            )


            if result:


                lng=result["longitude"]

                lat=result["latitude"]


                df.loc[index,"longitude"]=lng

                df.loc[index,"latitude"]=lat


                success+=1



            else:


                df.loc[index,"remark"]="编码失败"

                failed.append(row)

                continue



        df.loc[index,"map_url"]=create_map_url(

            lng,

            lat,

            name

        )



        df.loc[index,"navigation_url"]=create_navigation_url(

            lng,

            lat,

            name

        )


        df.loc[index,"remark"]="完成"



        time.sleep(
            REQUEST_INTERVAL
        )



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

    print("="*60)

    print(
        "处理完成"
    )

    print("="*60)


    print(
        "总数量:",
        total
    )


    print(
        "已有坐标:",
        existed
    )


    print(
        "自动成功:",
        success
    )


    print(
        "失败:",
        len(failed)
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



if __name__=="__main__":

    main()