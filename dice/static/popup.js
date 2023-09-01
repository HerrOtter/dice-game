
function findParentPopup(event)
{
    var target = event.target
    while (target && !target.classList.contains("popup"))
    {
        target = target.parentElement;
    }

    return target;
}

function findPopupElement(id, event)
{
    var element;
    if (id) 
    {
        element = document.getElementById(id);
    }
    else
    {
        element = findParentPopup(event);
    }
    return element;
}

function OpenPopup(id)
{
    var element = findPopupElement(id, event);
    if (element) {
        element.classList.add("popup-show");
    }
}

function ClosePopup(id)
{
    var element = findPopupElement(id, event);
    if (element) {
        element.classList.remove("popup-show");
    }
}

function PopupOnclick()
{
    if (event.target.classList.contains("popup"))
        ClosePopup();
}

window.addEventListener('load', 
  () => { 
    var popup_elements = document.getElementsByClassName("popup");
    for (const c of popup_elements) {
        c.addEventListener("click", PopupOnclick);
    }
  }, false
);
