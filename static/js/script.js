function enable_dark(lightbtn, darkbtn, page) {
    if (lightbtn.classList.contains('hidden')) {
        page.classList.toggle('dark')
        darkbtn.classList.toggle('hidden');
        lightbtn.classList.toggle('hidden');
    }
}

function disable_dark(lightbtn, darkbtn, page) {
    if (darkbtn.classList.contains('hidden')) {
        page.classList.toggle('dark')
        lightbtn.classList.toggle('hidden');
        darkbtn.classList.toggle('hidden');
    }
}

window.onload = () => {
    var darkmode_btn = document.getElementById('dark-indicator')
    var lightmode_btn = document.getElementById('light-indicator')
    var base_page = document.getElementById('the-page')

    // --- configure dark-mode
    if (darkmode_btn && lightmode_btn) {
        darkmode_btn.addEventListener('click', () => {
            enable_dark(lightmode_btn, darkmode_btn, base_page);
        });
        //--
        lightmode_btn.addEventListener('click', () => {
            disable_dark(lightmode_btn, darkmode_btn, base_page);
        });
    }
}
