// Import regexPattern from regex.js
import { regexPattern } from './no5/regex.js';

// Function to fetch and display the current regexPattern
async function fetchRegexPattern() {
    try {
        // Display the current regexPattern in the input field
        document.getElementById('regexPattern').value = regexPattern;
    } catch (error) {
        console.error('Error:', error);
    }
}


// Execute the fetchRegexPattern function when the DOM is loaded
document.addEventListener('DOMContentLoaded', fetchRegexPattern);



