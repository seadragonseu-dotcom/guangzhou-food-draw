/*
=====================================================

Guangzhou Food Draw V2.0

Smart Draw Engine V3.1 Stable

功能：
1. 数据加载
2. 数据关联
3. 智能筛选
4. 推荐评分
5. 随机抽签
6. 情侣模式
7. 推荐结果展示

=====================================================
*/


// =====================================================
// 数据
// =====================================================


let foodRelations = [];

let restaurants = [];

let dishes = [];


// 当前餐次

let currentMeal = "早餐";


// 最后结果

let lastResult = null;


// 动画状态

let isDrawing = false;


// 数据加载状态

let databaseReady = false;


// 当前动画结果

let drawingResult = null;






// =====================================================
// 加载数据库
// =====================================================


async function loadFoodDatabase(){


    try{


        const [

            foodData,

            restaurantData,

            dishData


        ] = await Promise.all([


            fetch(
                "data/food.json"
            )
            .then(
                r=>r.json()
            ),



            fetch(
                "data/restaurants.json"
            )
            .then(
                r=>r.json()
            ),



            fetch(
                "data/dishes.json"
            )
            .then(
                r=>r.json()
            )


        ]);



        foodRelations =
            foodData;


        restaurants =
            restaurantData;


        dishes =
            dishData;



        databaseReady = true;



        console.log(
            "Smart database loaded"
        );

        console.log(
            "Food:",
            foodRelations.length
        );


    }


    catch(error){


        console.error(

            "Database load failed:",

            error

        );


        databaseReady = false;


    }


}







// =====================================================
// 餐次设置
// =====================================================


function setMealType(meal){


    currentMeal = meal;


}







// =====================================================
// 数据合并
// =====================================================


function buildFoodList(){


    return foodRelations.map(item=>{


        const restaurant =

            restaurants.find(

                r=>

                r.id === item.restaurant_id

            );



        const dish =

            dishes.find(

                d=>

                d.id === item.dish_id

            );



        if(
            !restaurant ||
            !dish
        ){

            return null;

        }



        return {


            id:item.id,


            restaurant_id:
                restaurant.id,


            restaurant:
                restaurant.name,


            dish:
                dish.name,


            meal:
                dish.meal,


            district:
                restaurant.district,


            category:
                restaurant.category,


            price:
                restaurant.price,


            rating:
                restaurant.rating,


            couple_score:
                restaurant.couple_score || 0,


            tags:
                item.tags || [],


            reason:
                item.reason || "推荐美食",


            business_hours:
                restaurant.business_hours,


            latitude:
                restaurant.latitude,


            longitude:
                restaurant.longitude,


            address:
                restaurant.address


        };


    })

    .filter(

        item=>item

    );


}








// =====================================================
// 推荐评分
// =====================================================


function calculateScore(food){


    let score = 0;



    // 评分 30%

    score +=

        (
            food.rating / 5
        )

        *

        30;





    // 情侣指数 30%

    if(food.couple_score){


        score +=

            (
                food.couple_score / 5
            )

            *

            30;


    }






    const preference =

        getPreference

        ?

        getPreference()

        :

        {};





    // 预算 20%

    if(
        preference.maxPrice
    ){


        if(
            food.price <=
            preference.maxPrice
        ){

            score +=20;

        }


    }

    else{


        score +=10;


    }






    // 标签 20%

    if(

        preference.tags

        &&

        preference.tags.length

        &&

        food.tags.length

    ){


        const match =

            food.tags.filter(

                t=>

                preference.tags.includes(t)

            );



        score +=

            (
                match.length /
                preference.tags.length
            )

            *

            20;


    }

    else{


        score +=10;


    }



    return score;


}







// =====================================================
// 获取智能推荐池
// =====================================================


function getSmartPool(){


    let foods =

        buildFoodList();



    // 餐次过滤

    foods =

        foods.filter(

            food=>

            food.meal.includes(
                currentMeal
            )

        );






    const preference =

        getPreference

        ?

        getPreference()

        :

        {};







    // 情侣模式

    if(

        preference.coupleMode

    ){


        foods =

            foods.filter(

                food=>

                food.couple_score >=4

            );


    }






    // 区域

    if(

        preference.district

    ){


        foods =

            foods.filter(

                food=>

                food.district ===
                preference.district

            );


    }






    // 评分

    foods.forEach(

        food=>{


            food.score =

                calculateScore(food);


        }

    );





    // 排序

    foods.sort(

        (a,b)=>

        b.score-a.score

    );



    return foods;


}







// =====================================================
// 智能随机
// =====================================================


function randomFood(){


    const pool =

        getSmartPool();



    if(

        pool.length===0

    ){

        return null;

    }




    const top =

        pool.slice(

            0,

            Math.min(

                10,

                pool.length

            )

        );



    let result;



    do{


        result =

            top[

                Math.floor(

                    Math.random()

                    *

                    top.length

                )

            ];



    }

    while(

        lastResult

        &&

        result.id === lastResult.id

    );



    return result;


}








// =====================================================
// 开始抽签
// =====================================================


function startDraw(){


    if(isDrawing){

        return;

    }



    if(!databaseReady){


        alert(

            "美食数据库正在加载，请稍后"

        );


        return;


    }




    drawingResult =

        randomFood();



    if(!drawingResult){


        alert(

            "暂无符合条件的美食"

        );


        return;


    }




    isDrawing = true;



    const wheel =

        document.getElementById(
            "wheel"
        );


    const text =

        document.getElementById(
            "wheelText"
        );



    if(wheel){


        wheel.classList.add(

            "spinning"

        );


    }




    let timer =

        setInterval(()=>{


            const temp =

                randomFood();



            if(

                temp

                &&

                text

            ){


                text.innerHTML =

                    temp.dish;


            }


        },100);







    setTimeout(()=>{


        clearInterval(timer);


        finishDraw();


    },2500);



}







// =====================================================
// 完成抽签
// =====================================================


function finishDraw(){



    const result =

        drawingResult;



    if(result){


        lastResult = result;


        updateResult(

            result

        );


    }





    const wheel =

        document.getElementById(
            "wheel"
        );



    if(wheel){


        wheel.classList.remove(

            "spinning"

        );


        wheel.classList.add(

            "stop-spin"

        );


    }





    isDrawing = false;



}







// =====================================================
// 更新页面
// =====================================================


function updateResult(food){


    const map = {


        foodName:
            food.restaurant
            +
            "<br>"
            +
            food.dish,


        foodType:
            food.category,


        foodDistrict:
            food.district,


        foodPrice:
            "¥"+food.price,


        foodRating:
            food.rating,


        foodCoupleScore:
            food.couple_score
            +
            "/5",


        foodHours:
            food.business_hours
            ||
            "-",


        foodDescription:
            food.reason


    };





    Object.keys(map).forEach(id=>{


        const element =

            document.getElementById(id);



        if(element){


            element.innerHTML =

                map[id];


        }


    });







    const mapButton =

        document.getElementById(
            "mapButton"
        );



    if(mapButton){


        mapButton.onclick = ()=>{


            if(

                food.latitude

                &&

                food.longitude

            ){


                window.open(

                    "https://www.google.com/maps?q="

                    +

                    food.latitude

                    +

                    ","

                    +

                    food.longitude


                );


            }


        };


    }


}







// =====================================================
// 页面启动
// =====================================================


document.addEventListener(

    "DOMContentLoaded",

    ()=>{


        loadFoodDatabase();


    }

);






// =====================================================
// 提供接口
// =====================================================


function getLastResult(){


    return lastResult;


}