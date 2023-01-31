let profile = document.querySelector("#profile")

let modal = document.querySelector("#modal")
let close_modal = document.querySelector("#button-close-modal")

let button_avatar = document.querySelector("#button-avatar")
let button_background = document.querySelector("#button-background")
let button_bio = document.querySelector("#button-bio")

let form_avatar = document.querySelector("#form-avatar")
let form_background = document.querySelector("#form-background")
let form_bio = document.querySelector("#form-bio")


function modalAvatar() {
    button_avatar.addEventListener("click", function () {
        if (modal.classList.contains("hidden")) {

            modal.classList.remove("hidden")
            form_avatar.classList.remove("hidden")
            profile.classList.add("blur-sm")
        }
    })
}


function modalBackground() {
    button_background.addEventListener("click", function () {
        if (modal.classList.contains("hidden")) {

            modal.classList.remove("hidden")
            form_background.classList.remove("hidden")
            profile.classList.add("blur-sm")
        }
    })
}

function modalBio() {
    button_bio.addEventListener("click", function () {
        if (modal.classList.contains("hidden")) {

            modal.classList.remove("hidden")
            form_bio.classList.remove("hidden")
            profile.classList.add("blur-sm")
        }
    })
}


function closeModal() {
    close_modal.addEventListener("click", function () {
        if (!modal.classList.contains("hidden")) {

            form_avatar.classList.add("hidden")
            form_background.classList.add("hidden")
            form_bio.classList.add("hidden")
            modal.classList.add("hidden")
            profile.classList.remove("blur-sm")
        }
    })
}


modalAvatar()
modalBackground()
modalBio()
closeModal()