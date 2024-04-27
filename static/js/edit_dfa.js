// Ambil nilai variabel dari dfa.js
import { dfa as originalDfa, startState as originalStartState, acceptingStates as originalAcceptingStates } from '../js/no5/dfa.js';

async function fetchDfaValues() {
    try {
        // Gunakan nilai yang diimpor dari dfa.js
        const dfa = originalDfa;
        const startState = originalStartState;
        const acceptingStates = originalAcceptingStates;

        // Set nilai variabel ke dalam elemen input
        document.getElementById('dfa').value = JSON.stringify(dfa);
        document.getElementById('startState').value = startState;
        document.getElementById('acceptingStates').value = JSON.stringify(acceptingStates);
    } catch (error) {
        console.error('Terjadi kesalahan:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Panggil fungsi fetchDfaValues saat DOM telah dimuat
    fetchDfaValues();

    // Tangani peristiwa klik pada tombol "Simpan"
    document.getElementById('saveButton').addEventListener('click', () => {
        // Mengambil nilai dari inputan pengguna
        const dfaInput = JSON.parse(document.getElementById('dfa').value);
        const startStateInput = document.getElementById('startState').value;
        const acceptingStatesInput = JSON.parse(document.getElementById('acceptingStates').value);

        // Simpan inputan pengguna ke dalam variabel yang sesuai di dalam file dfa.js
        //updateDfaValues(dfaInput, startStateInput, acceptingStatesInput);
    });
});

async function updateDfaValues(dfaInput, startStateInput, acceptingStatesInput) {
    try {
        // Mengirim data ke server
        const response = await fetch('/update_dfa', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ dfa: dfaInput, startState: startStateInput, acceptingStates: acceptingStatesInput })
        });

        if (response.ok) {
            // Berhasil
            console.log('Nilai DFA berhasil diperbarui di server.');
            // Mengarahkan kembali ke halaman index.html setelah menyimpan
            window.location.href = 'index.html'; // Ganti dengan nama file index.html yang sesuai
        } else {
            // Gagal
            console.error('Gagal memperbarui nilai DFA di server.');
        }
    } catch (error) {
        console.error('Terjadi kesalahan:', error);
    }
}
