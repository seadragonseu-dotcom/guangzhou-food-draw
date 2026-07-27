/* =====================================================
   Guangzhou Food Draw V2.0
   Application Controller

   功能：
   1. 页面交互
   2. 餐次选择
   3. 情侣模式
   4. 抽签按钮
   5. 收藏功能

===================================================== */



// ==============================
// 全局状态
// ==============================


let coupleMode = false;


let favoriteList = [];





// ==============================
// 页面初始化
// ==============================


document.addEventListener(

    "DOMContentLoaded",

    () => {


        initMealButtons();


        initDrawButtons();


        initCoupleMode();


        initFavorite();


        loadFavorites();


    }

);






// ==============================
// 餐次按钮
// ==============================


function initMealButtons(){



    const buttons =

        document.querySelectorAll(
            ".meal-btn"
        );



    buttons.forEach(button=>{


        button.addEventListener(

            "click",

            ()=>{


                buttons.forEach(btn=>{


                    btn.classList.remove(
                        "active"
                    );


                });



                button.classList.add(
                    "active"
                );



                const meal =

                    button.dataset.meal;



                setMealType(meal);



            }

        );


    });


}







// ==============================
// 抽签按钮
// ==============================


function initDrawButtons(){



    const drawButton =

        document.getElementById(
            "drawButton"
        );



    const againButton =

        document.getElementById(
            "againButton"
        );



    if(drawButton){


        drawButton.addEventListener(

            "click",

            ()=>{


                startDraw();


            }

        );


    }



    if(againButton){


        againButton.addEventListener(

            "click",

            ()=>{


                startDraw();


            }

        );


    }


}







// ==============================
// 情侣模式
// ==============================


function initCoupleMode(){



    const button =

        document.getElementById(
            "coupleMode"
        );



    if(!button){

        return;

    }




    button.addEventListener(

        "click",

        ()=>{


            coupleMode = !coupleMode;



            if(coupleMode){


                button.innerHTML =

                    "❤️ 情侣模式开启";


                button.classList.add(
                    "active"
                );


            }

            else{


                button.innerHTML =

                    "❤️ 情侣模式关闭";


                button.classList.remove(
                    "active"
                );


            }



        }

    );


}







// ==============================
// 收藏功能初始化
// ==============================


function initFavorite(){



    const button =

        document.getElementById(
            "favoriteButton"
        );



    if(!button){

        return;

    }



    button.addEventListener(

        "click",

        ()=>{


            saveCurrentFood();


        }

    );


}







// ==============================
// 保存收藏
// ==============================


function saveCurrentFood(){



    if(!lastResult){


        alert(
            "请先抽签选择美食"
        );


        return;


    }



    const exists =

        favoriteList.some(

            item=>

            item.id === lastResult.id

        );



    if(exists){


        alert(
            "已经收藏过啦 ❤️"
        );


        return;


    }




    favoriteList.push(
        lastResult
    );



    localStorage.setItem(

        "favorites",

        JSON.stringify(
            favoriteList
        )

    );



    const button =

        document.getElementById(
            "favoriteButton"
        );



    if(button){


        button.classList.add(
            "favorite-active"
        );


        button.innerHTML =

            "❤️ 已收藏";


    }



}







// ==============================
// 加载收藏
// ==============================


function loadFavorites(){


    const data =

        localStorage.getItem(
            "favorites"
        );



    if(data){


        try{


            favoriteList =

                JSON.parse(
                    data
                );


        }

        catch(error){


            favoriteList=[];


        }


    }


}







// ==============================
// 获取收藏列表
// 后续页面使用
// ==============================


function getFavorites(){


    return favoriteList;


}







// ==============================
// 情侣模式状态
// 后续算法调用
// ==============================


function isCoupleMode(){


    return coupleMode;


}
