function search(e) {
    if (e !== "") {
        let texts = document.querySelectorAll(".searched");
        console.log(typeof texts);
        console.log(texts);
        let escaped_e = escapeRegex(e);
        let re = new RegExp(escaped_e, "ig"); // search for all instances case insensitive
        texts.forEach(text => {text.innerHTML = text.innerHTML.replaceAll(re, `<mark>${e}</mark>`);
        })
    }
}

function escapeRegex(string) {
    return string.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
}