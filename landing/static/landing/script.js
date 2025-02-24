/* Landingpage intro text type effect */

const texts = [
    "Train employees to spot phishing emails.",
    "Enhance organization's cybersecurity awareness.",
    "Run realistic phishing simulations with ease.",
    "Create custom templates for tailored campaigns.",
    "Track user behavior and improve resilience."
];
let textIndex = 0;
let charIndex = 0;
const typingElement = document.getElementById('typing-text');

function type() {
    if (charIndex < texts[textIndex].length) {
        typingElement.textContent += texts[textIndex].charAt(charIndex);
        charIndex++;
        setTimeout(type, 50);
    } else {
        setTimeout(erase, 2000);
    }
}

function erase() {
    if (charIndex > 0) {
        typingElement.textContent = texts[textIndex].substring(0, charIndex - 1);
        charIndex--;
        setTimeout(erase, 30);
    } else {
        textIndex = (textIndex + 1) % texts.length;
        setTimeout(type, 500);
    }
}

document.addEventListener('DOMContentLoaded', type);