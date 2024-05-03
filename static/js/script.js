import {  dfa, startState, acceptingStates } from '../js/no5/dfa.js';
import { nfa, acceptingStatesNFA, startStateNFA } from '../js/no5/nfa.js'; // Pastikan impor ini ada
import { enfa, startStateENFA, acceptingStatesENFA } from '../js/no5/enfa.js';
import { regexPattern } from '../js/no5/regex.js';

// Function to test DFA
function testDFA(inputString) {
  let currentState = startState; // Menggunakan start state dari dfa.js
  for (const char of inputString) {
    currentState = dfa[currentState][char];
    if (!currentState) return false;
  }
  return acceptingStates.includes(currentState); // Menggunakan accepting states dari dfa.js
}
// Function to test NFA
function testNFA(inputString) {
  let currentStates = [startStateNFA]; // Menggunakan start state dari nfa.js
  for (const char of inputString) {
    let nextStates = [];
    for (const state of currentStates) {
      const transitions = nfa[state][char] || []; // Pastikan untuk menangani transisi yang mungkin tidak ada
      nextStates.push(...transitions);
    }
    currentStates = [...new Set(nextStates)]; // Hapus duplikat dari nextStates
  }
  return currentStates.some(state => acceptingStatesNFA.includes(state)); // Menggunakan accepting states dari nfa.js
}

// Function to test ε-NFA
function testENFA(inputString) {
  let currentStates = [startStateENFA]; // Menggunakan start state dari enfa.js
  let epsilonClosure = []; // Simpan keadaan dalam epsilon-closure
  
  // Fungsi untuk menambahkan keadaan dalam epsilon-closure
  function addToEpsilonClosure(states) {
    states.forEach(state => {
      if (!epsilonClosure.includes(state)) {
        epsilonClosure.push(state);
        const epsilonTransitions = enfa[state][''] || []; // Transisi epsilon
        addToEpsilonClosure(epsilonTransitions);
      }
    });
  }

  // Fungsi untuk menambahkan ke state penolakan
  function addToRejectState() {
    currentStates = ['REJECT_STATE'];
  }
  
  // Inisialisasi epsilon-closure dari start state
  addToEpsilonClosure([startStateENFA]);
  currentStates.push(...epsilonClosure);
  epsilonClosure = []; // Kosongkan epsilon-closure
  
  for (const char of inputString) {
    let nextStates = [];
    for (const state of currentStates) {
      const transitions = enfa[state][char] || []; // Pastikan untuk menangani transisi yang mungkin tidak ada
      nextStates.push(...transitions);
    }
    // Tambahkan keadaan dalam epsilon-closure dari setiap keadaan pada nextStates
    addToEpsilonClosure(nextStates);
    currentStates = [...new Set(epsilonClosure)]; // Hapus duplikat dari epsilon-closure
    epsilonClosure = []; // Kosongkan epsilon-closure

    // Jika tidak ada transisi eksplisit, tambahkan ke state penolakan
    if (nextStates.length === 0) {
      addToRejectState();
      break; // Berhenti jika sudah ditambahkan ke state penolakan
    }
  }
  // Uji keadaan yang dicapai apakah ada di accepting states
  const isAccepted = currentStates.some(state => acceptingStatesENFA.includes(state)); // Menggunakan accepting states dari enfa.js

  // Jika input string selesai dibaca dan masih ada di state penolakan, maka reject
  if (currentStates.includes('REJECT_STATE')) {
    return false;
  }

  return isAccepted;
}





// // Function to test Regular Expression
// function testRegex(inputString, regexPattern) {
//   const regex = new RegExp(regexPattern);
//   return regex.test(inputString);
// }

function testRegex(inputString, regexPattern) {
  if (inputString.match(regexPattern)) {
      if (inputString.match(regexPattern)[0] == inputString) {
          return true;
      } else {
          return false;
      }
  } else {
      return false;
  }
}


// Handle form submission
const form = document.getElementById('testForm');
form.addEventListener('submit', function(event) {
  event.preventDefault();
  const selectType = document.getElementById('selectType').value;
  const inputString = document.getElementById('inputString').value;
  let result;

  switch(selectType) {
    case 'dfa':
      result = testDFA(inputString) ? 'accepted' : 'rejected';
      break;
    case 'nfa':
      result = testNFA(inputString) ? 'accepted' : 'rejected';
      break;
    case 'enfa':
      result = testENFA(inputString) ? 'accepted' : 'rejected';
      break;
    case 'regex':
      result = testRegex(inputString, regexPattern) ? 'accepted' : 'rejected';
      break;
    default:
      result = 'Tidak Valid, Pilih Jenis Automata';
  }

  const resultDiv = document.getElementById('result');
  resultDiv.textContent = `Input "${inputString}" ${result}`;
  
  // Mengatur warna latar belakang berdasarkan apakah input diterima atau ditolak
  if (result === 'accepted') {
    resultDiv.style.backgroundColor = '#90ee90'; // Warna hijau untuk input yang diterima
  } else {
    resultDiv.style.backgroundColor = '#ffcccc'; // Warna merah untuk input yang ditolak
  }
  
});

// Function to set the selected type
document.getElementById('dfaBtn').addEventListener('click', function() {
  document.getElementById('selectType').value = 'dfa';
});

document.getElementById('nfaBtn').addEventListener('click', function() {
  document.getElementById('selectType').value = 'nfa';
});

document.getElementById('enfaBtn').addEventListener('click', function() {
  document.getElementById('selectType').value = 'enfa';
});

document.getElementById('regexBtn').addEventListener('click', function() {
  document.getElementById('selectType').value = 'regex';
});



// script.js

// script.js
document.addEventListener("DOMContentLoaded", function() {
  const buttons = document.querySelectorAll('#selectButtons button');
  const regexPatternLabel = document.getElementById('regexPatternLabel');
  const regexPatternInput = document.getElementById('regexPattern');

  buttons.forEach(button => {
      button.addEventListener('click', function() {
          const buttonId = this.id;
          const imageId = buttonId.replace('Btn', 'Image');
          const image = document.getElementById(imageId);

          const allImages = document.querySelectorAll('.image');
          allImages.forEach(img => {
              img.style.display = 'none';
          });

          if (image) {
              image.style.display = 'block';
          }

          console.log("Button clicked with ID:", buttonId);

          // Menampilkan elemen label dan input jika tombol dengan ID 'regexBtn' diklik
          if (buttonId === 'regexBtn') {
              regexPatternLabel.style.display = 'block';
              regexPatternInput.style.display = 'block';
              regexPatternInput.focus();
          } else {
              // Sembunyikan elemen label dan input jika tombol lainnya diklik
              regexPatternLabel.style.display = 'none';
              regexPatternInput.style.display = 'none';
          }
      });
  });

  buttons.forEach(button => {
      button.addEventListener('click', () => {
          buttons.forEach(btn => btn.classList.remove('active'));
          button.classList.add('active');
      });
  });
});

// Sembunyikan tombol "Edit" secara default
const editButton1 = document.querySelector('.editButton1');
const editButton2 = document.querySelector('.editButton2');
const editButton3 = document.querySelector('.editButton3');
const editButton4 = document.querySelector('.editButton4');

editButton1.style.display = 'none';
editButton2.style.display = 'none';
editButton3.style.display = 'none';
editButton4.style.display = 'none';

// Tambahkan event listener ke tombol "DFA"
document.getElementById('dfaBtn').addEventListener('click', function() {
  // Menampilkan tombol "Edit" ketika tombol "DFA" diklik
  editButton1.style.display = 'block';
  editButton2.style.display = 'none';
  editButton3.style.display = 'none';
  editButton4.style.display = 'none';

});

// Tambahkan event listener ke tombol "NFA"
document.getElementById('nfaBtn').addEventListener('click', function() {
  // Menyembunyikan tombol "Edit" ketika tombol "NFA" diklik
  editButton1.style.display = 'none';
  editButton2.style.display = 'block';
  editButton3.style.display = 'none';
  editButton4.style.display = 'none';
});

// Tambahkan event listener ke tombol "e-NFA"
document.getElementById('enfaBtn').addEventListener('click', function() {
  // Menyembunyikan tombol "Edit" ketika tombol "e-NFA" diklik
  editButton1.style.display = 'none';
  editButton2.style.display = 'none';
  editButton3.style.display = 'block';
  editButton4.style.display = 'none';
});

// Tambahkan event listener ke tombol "Regex"
document.getElementById('regexBtn').addEventListener('click', function() {
  // Menyembunyikan tombol "Edit" ketika tombol "Regex" diklik
  editButton1.style.display = 'none';
  editButton2.style.display = 'none';
  editButton3.style.display = 'none';
  editButton4.style.display = 'block';
});

// Tambahkan event listener untuk menangkap klik pada tombol "Edit"
editButton1.addEventListener('click', () => {
  // Pindahkan halaman ke laman edit DFA
  window.location.href = 'edit_dfa'; // Ganti dengan URL laman edit DFA yang sesuai
});

editButton2.addEventListener('click', () => {
  // Pindahkan halaman ke laman edit DFA
  window.location.href = 'edit_nfa'; // Ganti dengan URL laman edit DFA yang sesuai
});

editButton3.addEventListener('click', () => {
  // Pindahkan halaman ke laman edit DFA
  window.location.href = 'edit_enfa'; // Ganti dengan URL laman edit DFA yang sesuai
});

editButton4.addEventListener('click', () => {
  // Pindahkan halaman ke laman edit DFA
  window.location.href = 'edit_regex'; // Ganti dengan URL laman edit DFA yang sesuai
});

//string regex yang tampil
document.getElementById('regexBtn').addEventListener('click', function() {
  document.getElementById('selectType').value = 'regex';

  // Menyembunyikan semua input teks dan label
  const allInputsAndLabels = document.querySelectorAll('label[for="regexPattern"], input#regexPattern');
  allInputsAndLabels.forEach(element => {
    element.style.display = 'none';
  });

  // Menampilkan input teks dan label untuk Regex
  const regexPatternLabel = document.querySelector('label[for="regexPattern"]');
  const regexPatternInput = document.getElementById('regexPattern');
  if (regexPatternLabel && regexPatternInput) {
    regexPatternLabel.style.display = 'block';
    regexPatternInput.style.display = 'block';
  }
});
