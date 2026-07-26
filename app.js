
let foods=[];

let currentMeal="午餐";


//读取数据库

fetch("food.json")

.then(res=>res.json())

.then(data=>{

foods=data;

});



//选择时间

function setMeal(meal){

currentMeal=meal;


document.querySelector(".subtitle")
.innerHTML=
"当前选择："+meal;

}



//抽签

function drawFood(){


let wheel=
document.querySelector(".wheel");


wheel.classList.add("spin");



let timer=setInterval(()=>{


let list=
foods.filter(
item=>item.type===currentMeal
);



let food=
list[
Math.floor(
Math.random()*list.length
)
];



document.getElementById(
"foodResult"
).innerHTML=
food.name;



document.getElementById(
"name"
).innerHTML=
food.name;


document.getElementById(
"type"
).innerHTML=
food.type;


document.getElementById(
"desc"
).innerHTML=
food.desc;



},100);



setTimeout(()=>{


clearInterval(timer);


wheel.classList.remove(
"spin"
);


},2500);



}
