let increaseFontSizeButton = document.querySelector("#increase-font-size");
increaseFontSizeButton.addEventListener('click', increaseFontSize);
increaseFontSizeButton.style.cursor = "pointer";

let decreaseFontSizeButton = document.querySelector("#decrease-font-size");
decreaseFontSizeButton.addEventListener('click', decreaseFontSize);
decreaseFontSizeButton.style.cursor = "pointer";

const maxFontSize = 20;
const minFontSize = 7;
const changeFontSizeValue = 1

function increaseFontSize() {
    let bodyStyle = window.getComputedStyle(document.body, null).getPropertyValue('font-size');
    let currentBodySize = parseFloat(bodyStyle)
    if (currentBodySize < maxFontSize) {
        document.body.style.fontSize = (currentBodySize + changeFontSizeValue) + 'px';
        changeFontSizeForTagNames("#question-title-in-lists", "increase")
    }

}

function decreaseFontSize() {
    let bodyStyle = window.getComputedStyle(document.body, null).getPropertyValue('font-size');
    let currentBodySize = parseFloat(bodyStyle)
    if (currentBodySize > minFontSize) {
        document.body.style.fontSize = (currentBodySize - changeFontSizeValue) + 'px';
        changeFontSizeForTagNames("#question-title-in-lists", "decrease")
    }

}

function changeFontSizeForTagNames(tagName, operation) {
    let allElements = document.querySelectorAll(tagName)
    allElements.forEach(element => {
        let elementStyle = window.getComputedStyle(element, null).getPropertyValue('font-size');
        let currentElementSize = parseFloat(elementStyle);
        if (operation == "decrease") {
            element.style.fontSize = (currentElementSize - changeFontSizeValue) + 'px';
        } else if (operation == "increase"){
            element.style.fontSize = (currentElementSize + changeFontSizeValue) + 'px';
        }
    })
}