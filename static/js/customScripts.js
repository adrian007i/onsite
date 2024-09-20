const getFormData = (selector) => Object.fromEntries(new FormData(document.querySelector(selector)));

const setErrors = (errors, server, form_id) => {
    const form = document.getElementById(form_id);

    for (err in errors) {

        try {
            const element = form.querySelector(`#${err}`);
            element.querySelector("div").innerText = errors[err];
            element.querySelector("input").classList.remove("is-invalid");

            if (server)
                element.querySelector("input").classList.add("is-invalid");

        } catch (e) { }
    }
}

const pending = (element, text, pending) => {
    const submit_btn = document.getElementsByClassName(element)[0];
    submit_btn.innerText = text;
    submit_btn.disabled = pending;
}

function passwordToggle(form) {
    var x = document.getElementById(form).querySelector("#password").querySelector("input");

    if (x.type === "password") {
        x.type = "text";
    } else {
        x.type = "password";
    }
}

const debounce = (func, wait = 0) => {
    let timeoutID = null;

    return (...args) => {
        clearTimeout(timeoutID);
        timeoutID = setTimeout(() => {
            func(...args);
        }, wait);
    };
};
 
const dropDownSearch = (e, endpoint) => {
    let val = e.value.toLowerCase().trim();
    const dropdown = e.parentElement.querySelector(".dropdown>ul");

    let items = "";

    if (val.length > 2) {
        fetch(`/${endpoint}?query=${e.value}`)
            .then(res => res.json())
            .then(res => {

                res.data.forEach(item => {
                    items += `<li><button type="button" class="dropdown-item" onclick="selectDropItem(this, ${item.id},'${item.name}')">${item.name}</button></li>`;
                });
                dropdown.innerHTML = items;
            });
    }
}

const debouncedOnInput = debounce(dropDownSearch, 400);


const selectDropItem = (e, id, name) => { 
    let root = e.parentElement.parentElement.parentElement.parentElement;
    let hidden = root.querySelector("input[type='hidden']").value = id;
    let text = root.querySelector("input[type='text']").value = name;

    e.parentElement.parentElement.classList.remove("show");   
    e.parentElement.parentElement.innerHTML = e.parentElement.outerHTML;

}

const focusDrop = (e) => {
    const dropdown = e.parentElement.querySelector(".dropdown>ul");
    dropdown.innerHTML = "";
    dropdown.classList.add("show"); 

    e.value = ""; 
    e.parentElement.querySelector("input[type='hidden']").value = "";  
}

const blurDrop = (e_id) => {   
    
    const element = document.getElementById(e_id);
    const hidden_value = element.querySelector("input[type='hidden']").value; 

    if (!hidden_value){
        element.querySelector(".dropdown>ul").classList.remove("show"); 
        element.querySelector("input[type='hidden']").value = "";
        element.querySelector("input[type='text']").value = "";
    }
}