/*
 * does the same as <dialog> but supports more browsers
 */
function findParentPopup(event)
{
    if (!event)
        return null;

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
    CloseAllPopups();

    var element = findPopupElement(id, event);
    if (element) {
        const callback_name = element.getAttribute("data-popup-open-callback");
        if (callback_name) {
            window[callback_name].call(element);
        }
        element.classList.add("popup-show");
    }
}

function ClosePopup(id)
{
    var element = findPopupElement(id, event);
    if (element) {
        const callback_name = element.getAttribute("data-popup-close-callback");
        if (callback_name) {
            window[callback_name].call(element);
        }

        element.classList.remove("popup-show");
    }
}

function CloseAllPopups()
{
    var open_popups = document.getElementsByClassName("popup-show");
    for (const c of open_popups)
    {
        ClosePopup(c.id);
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
    for (const c of popup_elements)
    {
        c.addEventListener("click", PopupOnclick);
    }
  }, false
);
