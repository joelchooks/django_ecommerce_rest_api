var fadeTarget = document.getElementById('msg')

function fadeOutEffect() {
    var fadeEffect = setInterval(function () {
        if (!fadeTarget.style.opacity) {
            fadeTarget.style.opacity = 1;
        }
        if (fadeTarget.style.opacity > 0) {
            fadeTarget.style.opacity -= 0.1;
        } else {
            clearInterval(fadeEffect);
        }

    }, 500);

}

// fadeOutEffect()

setTimeout(()=>{
    fadeTarget.classList.add('not-visible')
}, 4000)