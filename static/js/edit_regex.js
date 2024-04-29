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

//Function to update the regexPattern
// async function updateRegexPattern() {
//     try {
//         // Get the updated regexPattern from the input field
//         const updatedPattern = document.getElementById('regexPattern').value;

//         // Send the updated pattern to the server Flask
//         const response = await fetch('/update_regex_pattern', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify({ regexPattern: updatedPattern })
//         });

//         if (response.ok) {
//             console.log('Updated regexPattern:', updatedPattern);
            
//             // Optionally, you can update the regexPattern in regex.js here
//         } else {
//             console.error('Failed to update the regexPattern');
//         }

//     } catch (error) {
//         console.error('Error:', error);
//     }
// }

// Execute the fetchRegexPattern function when the DOM is loaded
document.addEventListener('DOMContentLoaded', fetchRegexPattern);

// Add event listener to the save button
// document.getElementById('saveButton').addEventListener('click', updateRegexPattern);



