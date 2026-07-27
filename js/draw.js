/**
 * 广州吃什么抽签系统
 *
 * draw.js
 *
 * V3.6.1 Bug Fix Frozen
 */


let foodDatabase = [];

let currentFood = null;

let isLoaded = false;



// =================================
// Load food database
// =================================

async function loadFoodDatabase(){


    try{


        const response =
            await fetch(
                "data/food.json"
            );


        foodDatabase =
            await response.json();


        isLoaded = true;


        console.log(
            "Food database loaded:",
            foodDatabase.length
        );


    }
    catch(error){

        console.error(
            "food.json load failed:",
            error
        );

    }

}




// =================================
// Draw
// =================================

function drawFood(){


    if(!isLoaded){

        alert(
            "数据库加载中"
        );

        return;

    }



    const index =
        Math.floor(
            Math.random()
            *
            foodDatabase.length
        );



    currentFood =
        foodDatabase[index];



    renderFood(
        currentFood
    );


}




// =================================
// Render
// =================================

function renderFood(food){



    setText(
        "foodName",
        food.name
    );



    setText(
        "foodType",
        food.category
    );



    setText(
        "foodDistrict",
        "📍 "
        +
        food.district
    );



    setText(
        "foodPrice",
        "💰 "
        +
        food.price
    );



    setText(
        "foodRating",
        food.rating
    );



    setText(
        "foodCoupleScore",
        food.couple_score
    );



    setText(
        "foodHours",
        food.business_hours
    );



    setText(
        "foodDescription",
        food.reason
    );


}




function setText(
    id,
    value
){


    const element =
        document.getElementById(
            id
        );


    if(element){

        element.innerText =
            value || "-";

    }

}



// =================================
// Navigation
// =================================

function navigateFood(){


    if(
        !currentFood
        ||
        !currentFood.navigation_url
    ){

        alert(
            "暂无导航地址"
        );

        return;

    }



    window.open(

        currentFood.navigation_url,

        "_blank"

    );

}



// =================================
// Map
// =================================

function openMap(){


    if(
        !currentFood
    ){

        return;

    }



    const url =

        "https://uri.amap.com/marker?position="
        +
        currentFood.longitude
        +
        ","
        +
        currentFood.latitude;



    window.open(
        url,
        "_blank"
    );

}



// =================================
// Expose
// =================================


window.startDraw =
    drawFood;


window.navigateFood =
    navigateFood;


window.openMap =
    openMap;




// =================================
// Init
// =================================


document.addEventListener(

    "DOMContentLoaded",

    function(){

        loadFoodDatabase();

    }

);