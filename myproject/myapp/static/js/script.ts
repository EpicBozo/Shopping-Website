const categories_button = document.getElementById("dropdown_button") as HTMLFormElement;
const dropdownContent = document.querySelector(".dropdown_content") as HTMLFormElement;

if(categories_button && dropdownContent){
categories_button.addEventListener("click", function(){
    if (categories_button.classList.contains("off")){
        categories_button.classList.remove("off");
        categories_button.classList.add("on");
    } else {
        categories_button.classList.remove("on");
        categories_button.classList.add("off");
    }

    if (categories_button.classList.contains("on")){
        dropdownContent.style.display = "block";
    } else {
        dropdownContent.style.display = "none";
    }
    
});
}
