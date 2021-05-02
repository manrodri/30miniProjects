function playSound(e) {
    const key = document.querySelector(`.key[data-key="${e.keyCode}"]`);
    key.classList.add('playing');
    const audio = document.querySelector(`audio[data-key="${e.keyCode}"]`);
    if (!audio) return;
    audio.currentTime = 0;  // rewind to the start
    audio.play();
}

const keys = document.querySelectorAll('.key')
keys.forEach(key => {
    key.addEventListener('transitionend', removeTransition)
});

function removeTransition(e) {
    if (e.propertyName !== 'transform') return; // return if it's not a transform event
    this.classList.remove('playing');
}

window.addEventListener('keydown', playSound)