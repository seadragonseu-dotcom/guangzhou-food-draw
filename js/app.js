/* =====================================================
   Guangzhou Food Draw V2.0

   Application Controller V2.1

   功能：
   1. 页面交互
   2. 餐次选择
   3. 情侣模式
   4. 收藏系统
   5. 用户偏好保存

===================================================== */



// ==============================
// 用户状态
// ==============================


let userPreference = {


    coupleMode:false,


    maxPrice:null,


    district:null


};



let favoriteList = [];






// 当前推荐结果

let currentFood = null;






// ==============================
// 页面初始化
// ==============================


document.addEventListener(

    "DOMContentLoaded",

    ()=>{


        loadUserPreference();


        loadFavorites();


        initMealButtons();


        initDrawButtons();


        initCoupleMode();


        initFavoriteButton();


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



                setMealType(

                    button.dataset.meal

                );


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



    updateCoupleButton(button);



    button.addEventListener(

        "click",

        ()=>{


            userPreference.coupleMode =

                !userPreference.coupleMode;



            saveUserPreference();



            updateCoupleButton(button);



        }

    );


}





function updateCoupleButton(button){



    if(
        userPreference.coupleMode
    ){


        button.innerHTML =

            "❤️ 情侣模式开启";


        button.classList.add(
            "active"
        );


    }

    else{


        button.innerHTML =

            "❤️ 情侣模式";


        button.classList.remove(
            "active"
        );


    }


}







// ==============================
// 提供给draw.js调用
// ==============================


function isCoupleMode(){


    return userPreference.coupleMode;


}







// ==============================
// 收藏功能
// ==============================


function initFavoriteButton(){



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


            addFavorite();


        }

    );


}







function addFavorite(){



    if(!lastResult){


        alert(
            "请先抽签"
        );


        return;

    }




    const exist =

        favoriteList.some(

            item=>

            item.id === lastResult.id

        );



    if(exist){


        alert(
            "已经收藏"
        );


        return;

    }




    favoriteList.push(

        lastResult

    );



    saveFavorites();



    const button =

        document.getElementById(
            "favoriteButton"
        );



    if(button){


        button.innerHTML =

            "❤️ 已收藏";


        button.classList.add(
            "favorite-active"
        );


    }



}








// ==============================
// 收藏存储
// ==============================


function saveFavorites(){



    localStorage.setItem(

        "favorites",

        JSON.stringify(
            favoriteList
        )

    );


}





function loadFavorites(){



    const data =

        localStorage.getItem(
            "favorites"
        );



    if(data){


        favoriteList =

            JSON.parse(
                data
            );


    }



}






function getFavorites(){


    return favoriteList;


}







// ==============================
// 用户偏好
// ==============================


function saveUserPreference(){



    localStorage.setItem(

        "userPreference",

        JSON.stringify(
            userPreference
        )

    );


}





function loadUserPreference(){



    const data =

        localStorage.getItem(
            "userPreference"
        );



    if(data){


        userPreference =

            JSON.parse(
                data
            );


    }



}








// ==============================
// 预算筛选接口
// 后续UI调用
// ==============================


function setMaxPrice(price){


    userPreference.maxPrice = price;


    saveUserPreference();


}







// ==============================
// 区域筛选接口
// ==============================


function setDistrict(district){


    userPreference.district = district;


    saveUserPreference();


}







function getPreference(){


    return userPreference;


}