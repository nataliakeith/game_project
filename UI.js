'use strict';

document.querySelector('#start-button').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/intro');
    const data = await response.json();

    document.querySelector('#intro-lore').innerText = data.lore.join('\n');
    document.querySelector('#menu-screen').style.display = 'none';
    document.querySelector('#lore-screen').style.display = 'block';
});

document.querySelector('#tutorial-button').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/tutorial');
    const data = await response.json();

    document.querySelector('#tutorial-text').innerText = data.tutorial.join('\n');
    document.querySelector('#menu-screen').style.display = 'none';
    document.querySelector('#tutorial').style.display = 'block';

})

document.querySelector('#back-button').addEventListener('click', async function() {
    document.querySelector('#tutorial').style.display = 'none';
    document.querySelector('#menu-screen').style.display = 'block';
})

document.querySelector('#continue-button').addEventListener('click', async function() {
    document.querySelector('#lore-screen').style.display ='none';
    document.querySelector('#gameplay-screen').style.display = 'block';
})

