
document.addEventListener('DOMContentLoaded', function (event) {
    //Getting elements
    var filter_button = document.getElementById("filter_button");
    var dropdown_content = document.querySelector(".dropdown_content");
    var low_to_high_button = document.getElementById("low-to-high");
    var high_to_low_button = document.getElementById("high-to-low");
    var sort_by_input = document.getElementById("sort-by");
    var sort_form = document.getElementById("sort-by-form");
    var product = document.querySelectorAll(".product");
    var grid_view = document.getElementById("grid");
    var list_view = document.getElementById("list");
    //Filter dropdown handeling

        filter_button.addEventListener("click", function () {
            if (filter_button.classList.contains("off")) {
                filter_button.classList.remove("off");
                filter_button.classList.add("on");
            }
            else {
                filter_button.classList.remove("on");
                filter_button.classList.add("off");
            }
            if (filter_button.classList.contains("on")) {
                dropdown_content.style.display = "block";
            }
            else {
                dropdown_content.style.display = "none";
            }
        });
        //Handeling the hidden input field
        
        low_to_high_button.addEventListener("click", function () {
            sort_by_input.value = "low-to-high";
            sort_form.submit();
            });
        high_to_low_button.addEventListener("click", function () {
            sort_by_input.value = "high-to-low";
            sort_form.submit();
            });

        //Handeling the product cards
        grid_view.addEventListener("click", function () {
            if(grid_view.classList.contains("off")){
                grid_view.classList.remove("off");
                grid_view.classList.add("on");
                list_view.classList.remove("on");
                list_view.classList.add("off");
                for (var i = 0; i < product.length; i++) {
                    product[i].style.width = "15%";
                }
                   
            }
        });

        list_view.addEventListener("click", function () {
            if(list_view.classList.contains("off")){
                list_view.classList.remove("off");
                list_view.classList.add("on");
                grid_view.classList.remove("on");
                grid_view.classList.add("off");
                for (var i = 0; i < product.length; i++) {
                    product[i].style.width = "80%";
                }
            }
        });
});
