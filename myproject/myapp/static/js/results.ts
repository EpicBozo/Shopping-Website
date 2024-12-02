/* TODO: 
make the dropdown button active
why does shi not work
*/

document.addEventListener('DOMContentLoaded',(event) => {
    //Getting elements

    const filter_button = document.getElementById("filter_button") as HTMLFormElement;
    const dropdown_content = document.querySelector(".dropdown_content") as HTMLElement;
    const low_to_high_button = document.getElementById("low-to-high") as HTMLFormElement;
    const high_to_low_button = document.getElementById("high-to-low") as HTMLFormElement;
    const sort_by_input = document.getElementById("sort-by") as HTMLFormElement;
    const sort_form = document.getElementById("sort-by-form") as HTMLFormElement;


    //Filter dropdown handeling

    if (filter_button && dropdown_content) {
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

    //Handeling the hidden input field
    if(low_to_high_button && high_to_low_button && sort_by_input && sort_form){
    low_to_high_button.addEventListener("click", function(){
        sort_by_input.value = "low-to-high";
        sort_form.submit();
    });

    high_to_low_button.addEventListener("click", function(){
        sort_by_input.value = "high-to-low";
        sort_form.submit();
    });
    }
}
});
