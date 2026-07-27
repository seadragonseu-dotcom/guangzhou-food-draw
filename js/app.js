/**
 * 广州美食抽签系统
 *
 * app.js V2.4 Navigation Binding Stable
 */


let currentMealType =
    "早餐";



// =================================
// Init
// =================================


document.addEventListener(

"DOMContentLoaded",

function(){


    initMealButtons();


    initDrawButton();


    initNavigationButton();


    initMapButton();


});




// =================================
// Meal
// =================================


function initMealButtons(){


    const buttons =
        document.querySelectorAll(
            ".meal-btn"
        );


    buttons.forEach(

        button=>{


            button.addEventListener(

                "click",

                function(){


                    buttons.forEach(

                        item=>{

                            item.classList.remove(
                                "active"
                            );

                        }

                    );



                    button.classList.add(
                        "active"
                    );



                    currentMealType =
                        button.dataset.meal;



                    if(
                        window.setMealType
                    ){

                        window.setMealType(
                            currentMealType
                        );

                    }


                }

            );


        }

    );


}




// =================================
// Draw Button
// =================================


function initDrawButton(){


    const button =
        document.getElementById(
            "drawButton"
        );


    if(button){


        button.onclick =
            function(){


                if(
                    window.startDraw
                ){

                    window.startDraw();

                }


            };


    }

}




// =================================
// Navigation Button
// =================================


function initNavigationButton(){


    const button =
        document.getElementById(
            "navigationButton"
        );


    if(button){


        button.onclick =
            function(){


                if(
                    window.navigateFood
                ){

                    window.navigateFood();

                }


            };


    }

}




// =================================
// Map Button
// =================================


function initMapButton(){


    const button =
        document.getElementById(
            "mapButton"
        );


    if(button){


        button.onclick =
            function(){


                if(
                    window.openMap
                ){

                    window.openMap();

                }


            };


    }

}




// =================================
// Getter
// =================================


window.getCurrentMeal =
function(){

    return currentMealType;

};