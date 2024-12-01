/* TODO: 
make the dropdown button active
*/

const filter_button = document.getElementById("dropdown_button")
const dropdown_content = document.querySelector(".dropdown_content")

filter_button.addEventListener("click", function(){
    if (filter_button.classList.contains("off")){
        filter_button.classList.remove("off");
        filter_button.classList.add("on");
    } else {
        filter_button.classList.remove("on");
        filter_button.classList.add("off");
    }

    if (filter_button.classList.contains("on")){
        dropdown_content.style.display = "block";
    } else {
        dropdown_content.style.display = "none";
    }
});

