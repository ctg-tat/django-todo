function text_decoration(checkBoxEl) {
    let label;

    if (checkBoxEl.checked) {
        label = checkBoxEl.nextElementSibling

        label.classList.add('task-done')
    } else {
        label = checkBoxEl.nextElementSibling

        label.classList.remove('task-done')
    }
}

function showForm(itemElem) {
    itemElem.style.display = 'none'

    let divParent = itemElem.parentNode
    let formElem = divParent.querySelector('#form-add-todo');
    formElem.style.display = 'block'

    let inputElem = formElem.querySelector('#input-add-todo');
    inputElem.focus()
    inputElem.addEventListener('blur', function () {
        itemElem.style.display = 'flex'
        formElem.style.display = 'none'
        inputElem.value = ''
    })
}

function getCSRFToken() {
    let csrfCookie = document.cookie.match(/csrftoken=([\w-]+)/);
    return csrfCookie ? csrfCookie[1] : null;
}

function insertCSRFToken(form) {
    let csrfToken = getCSRFToken();

    if (csrfToken) {
        let csrfInput = document.createElement('input');
        csrfInput.type = 'hidden';
        csrfInput.name = 'csrfmiddlewaretoken';
        csrfInput.value = csrfToken;

        form.appendChild(csrfInput);
    }
}

// Функция для выполнения асинхронного запроса
function createTodo(form) {

    let formData = new FormData(form)

    $.ajax({
        url: form.action,
        type: form.method,
        data: formData,
        contentType: false,
        processData: false,
        success: function (response) {
            let name = formData.get('name')
            let div = `<div class="field"><input type="checkbox" id="checkbox-${response.id}" onchange="text_decoration(this)"><label for="checkbox-${response.id}">${name}</label> </div>`
            let parent = form.parentNode
            parent.insertAdjacentHTML('afterbegin', div);

            form.childNodes[3].value = ''
        },
        error: function (error) {
            console.error(error);
        }
    });

    return false;
}