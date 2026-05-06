export async function getDialogue(passengerId, type) {

    const responses = {
        age: [
            "I'm old enough to be here.",
            "Why does that matter?",
            "None of your business."
        ],
        ticket: [
            "Here you go.",
            "Take a look.",
            "Happy now?"
        ],
        idle: [
            "I don't have all day...",
            "You done yet?",
            "Hello? Anyone home?"
        ],
        approve: ["Thanks.", "Finally.", "About time."],
        deny: ["What?!", "This is ridiculous!", "You're making a mistake."],
        surprise: ["...How did you know that?", "Wait, what?"]
    };

    // For now we use random.We'll add character specifics as we go!
    return responses[type][Math.floor(Math.random() * responses[type].length)];
}

export function showDialogue(text, expression = "def") {
    const box = document.getElementById('dialogue-box');
    box.textContent = `"${text}"`;
    box.style.display = 'block';
    setTimeout(() => { box.style.display = 'none'; }, 2800);
}