'use strict';

document.querySelector('#start-button').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/intro');
    const data = await response.json();

    document.querySelector('#intro-lore').innerText = data.lore.join('\n');
    document.querySelector('#menu-screen').style.display = 'none';
    document.querySelector('#lore-screen').style.display = 'flex';
});

document.querySelector('#tutorial-button').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/tutorial');
    const data = await response.json();

    document.querySelector('#tutorial-text').innerText = data.tutorial.join('\n');
    document.querySelector('#menu-screen').style.display = 'none';
    document.querySelector('#tutorial').style.display = 'flex';

});

document.querySelector('#back-button').addEventListener('click', async function() {
    document.querySelector('#tutorial').style.display = 'none';

    if (document.querySelector('#gameplay-screen').style.display === 'block') {
        document.querySelector('#gameplay-screen').style.display = 'block';
    } else {
        document.querySelector('#menu-screen').style.display = 'flex';
    }
});
document.querySelector('#continue-button').addEventListener('click', async function() {
    document.querySelector('#lore-screen').style.display = 'none';
    document.querySelector('#gameplay-screen').style.display = 'block';

    const response = await fetch('http://127.0.0.1:5000/current-passenger');
    const data = await response.json();

    loadPassengerScreen(data);
});

document.querySelector('#computer-tutorial-button').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/tutorial');
    const data = await response.json();

    alert(data.tutorial.join('\n'));
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

    document.querySelector('#character-popup-text').innerText =
    data.question + "\nPassenger says: " + data.answer;
});

document.querySelector('#popup-ask-ticket-button').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/ticket');
    const ticket = await response.json();

    document.querySelector('#character-popup-text').innerText =
    "Departure Airport: " + ticket.departure_airport + "\n" +
    "Arrival Airport: " + ticket.arrival_airport + "\n" +
    "Flight Date: " + ticket.flight_date + "\n" +
    "Flight Time: " + ticket.flight_time + "\n" +
    "Seat: " + ticket.seat;
});
function loadPassengerScreen(data) {
    if (data.game_finished) {
        showEnding(data);
        return;
    }

    if (data.is_backstabber) {
        document.querySelector('#gameplay-screen').style.display = 'none';
        document.querySelector('#daily-event').style.display = 'none';
        document.querySelector('#day-summary').style.display = 'none';
        document.querySelector('#ending-screen').style.display = 'none';

        document.querySelector('#backstabber-screen').style.display = 'block';

        document.querySelector('#backstabber-text').innerText = data.backstabber.text;
        document.querySelector('#backstabber-option-1').innerText = data.backstabber.option1;
        document.querySelector('#backstabber-option-2').innerText = data.backstabber.option2;

        document.querySelector('#backstabber-result').innerText = "";
        document.querySelector('#backstabber-option-1').style.display = 'block';
        document.querySelector('#backstabber-option-2').style.display = 'block';
        document.querySelector('#backstabber-boost-options').style.display = 'none';

        return;
    }

    document.querySelector('#backstabber-screen').style.display = 'none';
    document.querySelector('#daily-event').style.display = 'none';
    document.querySelector('#day-summary').style.display = 'none';
    document.querySelector('#ending-screen').style.display = 'none';

    document.querySelector('#gameplay-screen').style.display = 'block';

    showPassenger(data);
}
function showPassenger(data) {
    const description = data.description;
    const passport = data.passport;
    const status = data.status;

    const passengerId = data.passenger_id;
    const isAlien = data.species === "alien";

    const passengerForSprite = {
    id: passengerId,
    true_species: isAlien ? 0 : 1
};

const spritePath = SpriteManager.getSprite(passengerForSprite, "def");
const fallback = SpriteManager.getFallback("def");

SpriteManager.loadSprite(
    document.querySelector('#character-popup-image'),
    spritePath,
    fallback
);


    document.querySelector('#day-info').innerText = "DAY: " + data.day + " DECEMBER";

    document.querySelector('#character-description-text').innerText = description.description;

    document.querySelector('#passport-surname').innerText = "Surname: " + passport.surname;
    document.querySelector('#passport-given-name').innerText = "Given name: " + passport.given_names;
    document.querySelector('#passport-nationality').innerText = "Nationality: " + passport.nationality;
    document.querySelector('#passport-birth-date').innerText = "Date of birth: " + passport.birth_date;
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

    handleDecisionResult(data);
});
function handleDecisionResult(data) {
    if (data.game_finished) { //Tapiwa, this is for handling most decisions but backstabebr and events
        showEnding(data);
        return;
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

        if (data.show_event) {
            document.querySelector('#daily-event').style.display = 'block';
            document.querySelector('#event-text').innerText = data.event.text;

            document.querySelector('#event-option-1').innerText = data.event.option1;
            document.querySelector('#event-option-2').innerText = data.event.option2;

            document.querySelector('#event-option-1').style.display = 'block';
            document.querySelector('#event-option-2').style.display = 'block';
            document.querySelector('#event-response-text').innerText = "";
            document.querySelector('#event-continue-button').style.display = 'none';
        } else {
            document.querySelector('#day-summary').style.display = 'block';
            document.querySelector('#next-day-button').style.display = 'block';
        }

        return;
    }

    loadPassengerScreen(data.next_passenger);
}

document.querySelector('#deny-button').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/deny');
    const data = await response.json();

    handleDecisionResult(data);
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

document.querySelector('#next-day-button').addEventListener('click', async function() {
    document.querySelector('#day-summary').style.display = 'none';
    const response = await fetch('http://127.0.0.1:5000/current-passenger');
    const data = await response.json();

    if (data.game_finished) {
        showEnding(data);
        return;
    }

    document.querySelector('#gameplay-screen').style.display = 'block';
    loadPassengerScreen(data);
});
document.querySelector('#event-option-1').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/daily-event/1');
    const data = await response.json();

    showEventResult(data);
});

document.querySelector('#event-option-2').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/daily-event/2');
    const data = await response.json();

    showEventResult(data);
});

function showEventResult(data) {
    if (data.game_finished) {
        showEnding(data);
        return;
    }

    document.querySelector('#event-response-text').innerText = data.message;

    document.querySelector('#energy').innerText = "Energy: " + data.status.energy;
    document.querySelector('#budget-text').innerText = "Budget: " + data.status.budget;
    document.querySelector('#reputation-text').innerText = "Reputation: " + data.status.reputation;
    document.querySelector('#sustainability-text').innerText = "Sustainability: " + data.status.sustainability;

    document.querySelector('#event-option-1').style.display = 'none';
    document.querySelector('#event-option-2').style.display = 'none';

    document.querySelector('#event-continue-button').style.display = 'block';
}

document.querySelector('#backstabber-option-1').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/backstabber/1');
    const data = await response.json();

    document.querySelector('#backstabber-result').innerText = data.message;

    if (data.needs_boost_choice) {
        document.querySelector('#backstabber-boost-options').style.display = 'flex';
    } else {
        showBackstabberResult(data);
    }
});

document.querySelector('#backstabber-option-2').addEventListener('click', async function() {
    const response = await fetch('http://127.0.0.1:5000/backstabber/2');
    const data = await response.json();

    showBackstabberResult(data);
});

document.querySelector('#backstabber-boost-1').addEventListener('click', function() {
    chooseBackstabberBoost(1);
});
document.querySelector('#backstabber-boost-2').addEventListener('click', function() {
    chooseBackstabberBoost(2);
});
document.querySelector('#backstabber-boost-3').addEventListener('click', function() {
    chooseBackstabberBoost(3);
});
document.querySelector('#backstabber-boost-4').addEventListener('click', function() {
    chooseBackstabberBoost(4);
});
document.querySelector('#backstabber-boost-5').addEventListener('click', function() {
    chooseBackstabberBoost(5);
});

async function chooseBackstabberBoost(boostChoice) {
    const response = await fetch('http://127.0.0.1:5000/backstabber/1/' + boostChoice);
    const data = await response.json();

    showBackstabberResult(data);
}

function showBackstabberResult(data) {
    document.querySelector('#backstabber-result').innerText = data.message;

    document.querySelector('#energy').innerText = "Energy: " + data.status.energy;
    document.querySelector('#budget-text').innerText = "Budget: " + data.status.budget;
    document.querySelector('#reputation-text').innerText = "Reputation: " + data.status.reputation;
    document.querySelector('#sustainability-text').innerText = "Sustainability: " + data.status.sustainability;

    document.querySelector('#backstabber-boost-options').style.display = 'none';
    document.querySelector('#backstabber-option-1').style.display = 'none';
    document.querySelector('#backstabber-option-2').style.display = 'none';


    document.querySelector('#backstabber-screen').style.display = 'none';
    handleDecisionResult(data);
}

document.querySelector('#event-continue-button').addEventListener('click', async function() {
    document.querySelector('#daily-event').style.display = 'none';

    const response = await fetch('http://127.0.0.1:5000/current-passenger');
    const data = await response.json();

    if (data.game_finished) {
        showEnding(data);
        return;
}

    document.querySelector('#gameplay-screen').style.display = 'block';
    loadPassengerScreen(data);
});
function showEnding(data) {
  document.querySelector('#gameplay-screen').style.display = 'none';
  document.querySelector('#daily-event').style.display = 'none';
  document.querySelector('#event-option-1').style.display = 'none';
  document.querySelector('#event-option-2').style.display = 'none';
  document.querySelector('#event-response-text').style.display = 'none';
  document.querySelector('#event-continue-button').style.display = 'none';
  document.querySelector('#day-summary').style.display = 'none';
  document.querySelector('#backstabber-screen').style.display = 'none';

  document.querySelector('#ending-screen').style.display = 'block';
  document.querySelector('#ending-title').innerText = data.ending.title;
  document.querySelector('#ending-message').innerText = data.ending.message;
}