let button_menu = document.querySelector("#menu")
let pages = document.querySelector("#pages")


function showMenu() {

    button_menu.addEventListener("click", function () {

        if (pages.classList.contains("hidden")) {
            pages.classList.remove("hidden")
        }
        else {
            pages.classList.add("hidden")
        }
    })


    window.onscroll = () => {
        pages.classList.add("hidden")
    }
}

showMenu()