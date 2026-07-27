/* =====================================================
   Guangzhou Food Draw V2.0
   Draw Engine

   功能：
   1. 加载美食数据
   2. 按餐次筛选
   3. 随机抽签
   4. 控制转盘动画
   5. 输出结果

===================================================== */



// ==============================
// 全局变量
// ==============================


let foodDatabase = [];


let currentMeal = "早餐";


let lastResult = null;


let isDrawing = false;




// ==============================
// 加载美食数据库
// ==============================


async function loadFoodDatabase(){


    try{


        const response = await fetch(
            "data/food.json"
        );


        foodDatabase =
            await response.json();



        console.log(
            "Food database loaded:",
            foodDatabase.length
        );


    }

    catch(error){


        console.error(
            "Food database loading failed:",
            error
        );


    }


}






// ==============================
// 设置当前餐次
// ==============================


function setMealType(meal){


    currentMeal = meal;


}







// ==============================
// 获取候选美食
// ==============================


function getAvailableFoods(){


    let list =

        foodDatabase.filter(

            item =>

            item.meal.includes(currentMeal)

        );



    // 如果数据库为空

    if(list.length === 0){


        list = foodDatabase;


    }



    return list;


}







// ==============================
// 随机选择
// ==============================


function randomFood(){


    const foods =

        getAvailableFoods();



    if(
        foods.length === 0
    ){


        return null;


    }



    let result;



    let retry = 0;



    do{


        result =

            foods[
                Math.floor(
                    Math.random()
                    *
                    foods.length
                )
            ];



        retry++;


    }

    while(

        lastResult

        &&

        result.id === lastResult.id

        &&

        retry < 10

    );



    lastResult = result;



    return result;


}







// ==============================
// 开始抽签动画
// ==============================


function startDraw(){



    if(isDrawing){

        return;

    }



    isDrawing = true;



    const wheel =

        document.getElementById(
            "wheel"
        );



    const wheelText =

        document.getElementById(
            "wheelText"
        );



    const drawButton =

        document.getElementById(
            "drawButton"
        );



    if(wheel){


        wheel.classList.add(
            "spinning"
        );


    }



    if(wheelText){


        wheelText.innerHTML =

            "抽签中...";


    }



    if(drawButton){


        drawButton.disabled = true;


    }



    // 快速显示随机过程

    let randomTimer =

        setInterval(()=>{


            const temp =

                randomFood();



            if(temp){


                wheelText.innerHTML =

                    temp.dish ||

                    temp.name;


            }



        },100);






    // 2.5秒后停止

    setTimeout(()=>{


        clearInterval(
            randomTimer
        );



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



    const wheelText =

        document.getElementById(
            "wheelText"
        );



    const drawButton =

        document.getElementById(
            "drawButton"
        );




    if(wheel){


        wheel.classList.remove(
            "spinning"
        );


        wheel.classList.add(
            "stop-spin"
        );


    }




    if(!result){


        return;


    }






    if(wheelText){


        wheelText.innerHTML =

            result.dish ||

            result.name;


    }



    // 输出结果

    updateResult(result);





    setTimeout(()=>{


        if(wheel){

            wheel.classList.remove(
                "stop-spin"
            );

        }


    },1500);




    if(drawButton){


        drawButton.disabled = false;


    }



    isDrawing = false;



}







// ==============================
// 更新推荐卡片
// ==============================


function updateResult(food){



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

            food.dish ||

            food.name;


        name.classList.add(
            "food-highlight"
        );


    }



    if(type){


        type.innerHTML =

            food.category ||

            "广州美食";


    }



    if(district){


        district.innerHTML =

            food.district ||

            "广州";


    }



    if(price){


        price.innerHTML =

            food.price ||

            "待定";


    }



    if(desc){


        desc.innerHTML =

            food.reason ||

            food.desc ||

            "今天推荐这道美食";


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
// 页面初始化
// ==============================


document.addEventListener(

    "DOMContentLoaded",

    ()=>{


        loadFoodDatabase();


    }

);
