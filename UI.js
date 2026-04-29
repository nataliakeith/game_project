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

});

document.querySelector('#back-button').addEventListener('click', async function() {
    document.querySelector('#tutorial').style.display = 'none';
    document.querySelector('#menu-screen').style.display = 'block';
});

document.querySelector('#continue-button').addEventListener('click', async function() {
    document.querySelector('#lore-screen').style.display = 'none';
    document.querySelector('#gameplay-screen').style.display = 'block';

    const response = await fetch('http://127.0.0.1:5000/current-passenger');
    const data = await response.json();

    showPassenger(data);
});

document.querySelector('#computer-tutorial-button').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/tutorial');
    const data = await response.json();

    document.querySelector('#tutorial-text').innerText = data.tutorial.join('\n');
    document.querySelector('#tutorial').style.display = 'block';
});

document.querySelector('#passport-zoom-button').addEventListener('click', function() {
    document.querySelector('#passport-preview').classList.toggle('zoomed'); //im putting zoom to css, too much struggle to me  :.)
});

document.querySelector('#status-zoom-button').addEventListener('click', function() {
    document.querySelector('#status-container').classList.toggle('zoomed');
});

document.querySelector('#character-peek-button').addEventListener('click', function() {
    document.querySelector('#character-popup').style.display = 'block';
});

document.querySelector('#close-character-popup').addEventListener('click', function() {
    document.querySelector('#character-popup').style.display = 'none';
});

document.querySelector('#popup-ask-age-button').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/age');
    const data = await response.json();

    document.querySelector('#popup-age-question').innerText = data.question;
    document.querySelector('#popup-age-answer').innerText = "Passenger says: " + data.answer;
});

document.querySelector('#popup-ask-ticket-button').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/ticket');
    const ticket = await response.json();

    document.querySelector('#popup-ticket-departure').innerText = "Departure Airport: " + ticket.departure_airport;
    document.querySelector('#popup-ticket-arrival').innerText = "Arrival Airport: " + ticket.arrival_airport;
    document.querySelector('#popup-ticket-flight-date').innerText = "Flight Date: " + ticket.flight_date;
    document.querySelector('#popup-ticket-flight-time').innerText = "Flight Time: " + ticket.flight_time;
    document.querySelector('#popup-ticket-seat').innerText = "Seat: " + ticket.seat;
});
function showPassenger(data) {
    const description = data.description;
    const passport = data.passport;
    const status = data.status;

    document.querySelector('#next-day-button').style.display = 'block';
    document.querySelector('#day-info').innerText = "DAY: " + data.day + " DECEMBER";
    document.querySelector('#character-description-text').innerText = description.description;

    document.querySelector('#passport-surname').innerText = "Surname: " + passport.surname;
    document.querySelector('#passport-given-name').innerText = "Given name: " + passport.given_names;
    document.querySelector('#passport-nationality').innerText = "Nationality: " + passport.nationality;
    document.querySelector('#passport-birth-date').innerText = "Data of birth: " + passport.birth_date;
    document.querySelector('#passport-sex').innerText = "Sex: " + passport.sex;
    document.querySelector('#passport-place-birth').innerText = "Place of birth: " + passport.place_of_birth;
    document.querySelector('#passport-number').innerText = "Passport No: " + passport.passport_number;
    document.querySelector('#passport-country').innerText = "Issuing Country: " + passport.issuing_country;
    document.querySelector('#passport-expiry').innerText = "Expiry Date: " + passport.expiration_date;

    document.querySelector('#energy').innerText = "Energy: " + status.energy;
    document.querySelector('#budget-text').innerText = "Budget: " + status.budget;
    document.querySelector('#reputation-text').innerText = "Reputation: " + status.reputation;
    document.querySelector('#sustainability-text').innerText = "Sustainability: " + status.sustainability;

    document.querySelector('#popup-age-question').innerText = "";
    document.querySelector('#popup-age-answer').innerText = "";

    document.querySelector('#popup-ticket-departure').innerText = "Departure Airport: ";
    document.querySelector('#popup-ticket-arrival').innerText = "Arrival Airport: ";
    document.querySelector('#popup-ticket-flight-date').innerText = "Flight Date: ";
    document.querySelector('#popup-ticket-flight-time').innerText = "Flight Time: ";
    document.querySelector('#popup-ticket-seat').innerText = "Seat: ";

    document.querySelector('#character-popup').style.display = 'none';
}
document.querySelector('#accept-button').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/approve');
    const data = await response.json();

    document.querySelector('#humans-approved').innerText = "Humans approved: " + data.approved_humans;
    document.querySelector('#humans-denied').innerText = "Humans denied: " + data.denied_humans;
    document.querySelector('#aliens-approved').innerText = "Aliens approved: " + data.approved_aliens;
    document.querySelector('#aliens-denied').innerText = "Aliens denied: " + data.denied_aliens;

    if (data.show_backstabber) {
    document.querySelector('#gameplay-screen').style.display = 'none';

    document.querySelector('#backstabber-screen').style.display = 'block';
    document.querySelector('#backstabber-text').innerText = data.backstabber.text;

    document.querySelector('#backstabber-option-1').innerText = data.backstabber.option1;
    document.querySelector('#backstabber-option-2').innerText = data.backstabber.option2;

    return;
}

    if (data.game_finished) {
        document.querySelector('#next-day-button').style.display = 'none';
    }

    if (data.day_finished) {
        document.querySelector('#energy').innerText = "Energy: " + data.status.energy;
        document.querySelector('#budget-text').innerText = "Budget: " + data.status.budget;
        document.querySelector('#reputation-text').innerText = "Reputation: " + data.status.reputation;
        document.querySelector('#sustainability-text').innerText = "Sustainability: " + data.status.sustainability;

        document.querySelector('#gameplay-screen').style.display = 'none';
        document.querySelector('#daily-event').style.display = 'block';

    document.querySelector('#daily-event').innerText = data.event.text;
    document.querySelector('#event-option-1').innerText = data.event.option1;
    document.querySelector('#event-option-2').innerText = data.event.option2;

    document.querySelector('#event-option-1').style.display = 'block';
    document.querySelector('#event-option-2').style.display = 'block';
    } else {
        showPassenger(data.next_passenger);
    }
});

document.querySelector('#deny-button').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/deny');
    const data = await response.json();

    if (data.show_backstabber) {
        document.querySelector('#gameplay-screen').style.displau = 'none';
        document.querySelector('#backstabber-screen').style.display = 'block';
        document.querySelector('#backstabber-text').innerText = data.backstabber.text;
        document.querySelector('#backstabber-option-1').style.display = 'block';
        document.querySelector('#backstabber-option-2').style.display = 'block';
        document.querySelector('#backstabber-option-1').innerText = data.backstabber.option1;
        document.querySelector('#backstabber-option-2').innerText = data.backstabber.option2;


    return;
}
    if (data.game_finished) {
        document.querySelector('#next-day-button').style.display = 'none';
    }

    document.querySelector('#humans-approved').innerText = "Humans approved: " + data.approved_humans;
    document.querySelector('#humans-denied').innerText = "Humans denied: " + data.denied_humans;
    document.querySelector('#aliens-approved').innerText = "Aliens approved: " + data.approved_aliens;
    document.querySelector('#aliens-denied').innerText = "Aliens denied: " + data.denied_aliens;

    if (data.day_finished) {
        document.querySelector('#energy').innerText = "Energy: " + data.status.energy;
        document.querySelector('#budget-text').innerText = "Budget: " + data.status.budget;
        document.querySelector('#reputation-text').innerText = "Reputation: " + data.status.reputation;
        document.querySelector('#sustainability-text').innerText = "Sustainability: " + data.status.sustainability;

        document.querySelector('#gameplay-screen').style.display = 'none';
        document.querySelector('#daily-event').style.display = 'block';

        document.querySelector('#daily-event').innerText = data.event.text;
        document.querySelector('#event-option-1').innerText = data.event.option1;
        document.querySelector('#event-option-2').innerText = data.event.option2;

        document.querySelector('#event-option-1').style.display = 'block';
        document.querySelector('#event-option-2').style.display = 'block';
    } else {
        showPassenger(data.next_passenger);
    }
});

document.querySelector('#boost-button').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/boost');
    const data = await response.json();

    document.querySelector('#boost-box').style.display = 'block';

    document.querySelector('#boost-info').innerText =
        "Boosts available: " + data.boost_days;
});

document.querySelector('#use-boost-button').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/use-boost');
    const data = await response.json();

    if (data.used) {
        document.querySelector('#boost-result').innerText = "Surprise factor: " + data.surprise_factor;
    } else {
        document.querySelector('#boost-result').innerText = "No boosts available.";
    }
});


