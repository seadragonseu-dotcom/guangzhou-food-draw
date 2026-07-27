/* =====================================================
   Guangzhou Food Draw V2.0

   Draw Engine V2.1

   功能：
   1. 加载静态数据库
   2. 数据关联
   3. 餐次筛选
   4. 随机推荐
   5. 情侣模式支持
   6. 转盘动画控制

===================================================== */



// ==============================
// 数据缓存
// ==============================


let foodRelations = [];

let restaurants = [];

let dishes = [];

let tags = [];



// ==============================
// 状态
// ==============================


let currentMeal = "早餐";

let lastResult = null;

let isDrawing = false;






// ==============================
// 加载数据库
// ==============================


async function loadFoodDatabase(){


    try{


        const [

            foodData,

            restaurantData,

            dishData,

            tagData


        ] = await Promise.all([


            fetch(
                "data/food.json"
            ).then(
                r=>r.json()
            ),


            fetch(
                "data/restaurants.json"
            ).then(
                r=>r.json()
            ),


            fetch(
                "data/dishes.json"
            ).then(
                r=>r.json()
            ),


            fetch(
                "data/tags.json"
            ).then(
                r=>r.json()
            )


        ]);



        foodRelations = foodData;

        restaurants = restaurantData;

        dishes = dishData;

        tags = tagData;



        console.log(
            "Database loaded:",
            {
                food:
                    foodRelations.length,

                restaurants:
                    restaurants.length,

                dishes:
                    dishes.length
            }
        );


    }

    catch(error){


        console.error(
            "Database load failed:",
            error
        );


    }


}







// ==============================
// 数据关联
// ==============================


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


            restaurant:


                restaurant.name,


            dish:


                dish.name,



            meal:


                dish.meal,



            district:


                restaurant.district,



            area:


                restaurant.area,



            category:


                restaurant.category,



            price:


                restaurant.price,



            rating:


                restaurant.rating,



            couple_score:


                restaurant.couple_score,



            tags:


                item.tags,



            reason:


                item.reason


        };


    })

    .filter(

        item=>item!==null

    );


}







// ==============================
// 设置餐次
// ==============================


function setMealType(meal){


    currentMeal = meal;


}








// ==============================
// 获取推荐池
// ==============================


function getAvailableFoods(){



    let list =


        buildFoodList();



    list =

        list.filter(

            item =>

            item.meal.includes(
                currentMeal
            )

        );



    return list;


}







// ==============================
// 随机推荐
// ==============================


function randomFood(){



    let foods =

        getAvailableFoods();



    if(
        foods.length===0
    ){

        return null;

    }



    // 情侣模式

    if(
        typeof isCoupleMode ===
        "function"

        &&

        isCoupleMode()

    ){


        const coupleFoods =

            foods.filter(

                item=>

                item.couple_score>=4

            );



        if(
            coupleFoods.length>0
        ){

            foods = coupleFoods;

        }


    }






    let result;


    let count=0;



    do{


        result =

            foods[

                Math.floor(

                    Math.random()

                    *

                    foods.length

                )

            ];


        count++;


    }

    while(


        lastResult

        &&

        result.id === lastResult.id

        &&

        count < 10


    );



    lastResult = result;



    return result;


}








// ==============================
// 开始抽签
// ==============================


function startDraw(){



    if(isDrawing){

        return;

    }



    isDrawing=true;



    const wheel =

        document.getElementById(
            "wheel"
        );



    const text =

        document.getElementById(
            "wheelText"
        );



    const button =

        document.getElementById(
            "drawButton"
        );



    if(wheel){

        wheel.classList.add(
            "spinning"
        );

    }



    if(button){

        button.disabled=true;

    }



    let timer =

        setInterval(()=>{


            let temp =

                randomFood();



            if(temp && text){


                text.innerHTML =

                    temp.dish;


            }



        },100);






    setTimeout(()=>{


        clearInterval(timer);


        finishDraw();


    },2500);



}







// ==============================
// 完成抽签
// ==============================


function finishDraw(){



    const result =

        randomFood();




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



    updateResult(result);




    setTimeout(()=>{


        if(wheel){

            wheel.classList.remove(
                "stop-spin"
            );

        }


    },1500);




    const button =

        document.getElementById(
            "drawButton"
        );


    if(button){

        button.disabled=false;

    }



    isDrawing=false;


}







// ==============================
// 更新页面结果
// ==============================


function updateResult(food){



    if(!food){

        return;

    }




    const name =

        document.getElementById(
            "foodName"
        );



    const type =

        document.getElementById(
            "foodType"
        );



    const district =

        document.getElementById(
            "foodDistrict"
        );



    const price =

        document.getElementById(
            "foodPrice"
        );



    const desc =

        document.getElementById(
            "foodDescription"
        );





    if(name){

        name.innerHTML =

            food.restaurant

            +

            " · "

            +

            food.dish;

    }




    if(type){

        type.innerHTML =

            food.category;

    }




    if(district){

        district.innerHTML =

            food.district;

    }




    if(price){

        price.innerHTML =

            "¥"

            +

            food.price;

    }




    if(desc){

        desc.innerHTML =

            food.reason;

    }



    const card =

        document.querySelector(
            ".result-card"
        );



    if(card){


        card.classList.remove(
            "show"
        );



        setTimeout(()=>{


            card.classList.add(
                "show"
            );


        },50);


    }



}







// ==============================
// 初始化
// ==============================


document.addEventListener(

    "DOMContentLoaded",

    ()=>{


        loadFoodDatabase();


    }

);