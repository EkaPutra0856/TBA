// Ambil nilai variabel dari nfa.js
import { nfa as originalNfa, startStateNFA as originalStartStates, acceptingStatesNFA as originalAcceptingStates } from '../js/no5/nfa.js';

async function fetchNfaValues() {
    try {
        // Gunakan nilai yang diimpor dari nfa.js
        const nfa = originalNfa;
        const startStateNFA = originalStartStates;
        const acceptingStatesNFA = originalAcceptingStates;

        // Set nilai variabel ke dalam elemen input
        document.getElementById('nfa').value = JSON.stringify(nfa);
        document.getElementById('startStates').value = JSON.stringify(startStateNFA);
        document.getElementById('acceptingStates').value = JSON.stringify(acceptingStatesNFA);
    } catch (error) {
        console.error('Terjadi kesalahan:', error);
    }
}

document.addEventListener('DOMContentLoaded', () => {
    // Panggil fungsi fetchNfaValues saat DOM telah dimuat
    fetchNfaValues();

    // Tangani peristiwa klik pada tombol "Simpan"
    document.getElementById('saveButton').addEventListener('click', () => {
        // Mengambil nilai dari inputan pengguna
        const nfaInput = JSON.parse(document.getElementById('nfa').value);
        const startStatesInput = JSON.parse(document.getElementById('startStates').value);
        const acceptingStatesInput = JSON.parse(document.getElementById('acceptingStates').value);

        // Simpan inputan pengguna ke dalam variabel yang sesuai di dalam file nfa.js
        //updateNfaValues(nfaInput, startStatesInput, acceptingStatesInput);
    });
});

async function updateNfaValues(nfaInput, startStatesInput, acceptingStatesInput) {
    try {
        // Mengirim data ke server
        const response = await fetch('/update_nfa', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nfa: nfaInput, startStates: startStatesInput, acceptingStates: acceptingStatesInput })
        });

        if (response.ok) {
            // Berhasil
            console.log('Nilai NFA berhasil diperbarui di server.');
            // Mengarahkan kembali ke halaman index.html setelah menyimpan
            window.location.href = 'index.html'; // Ganti dengan nama file index.html yang sesuai
        } else {
            // Gagal
            console.error('Gagal memperbarui nilai NFA di server.');
        }
    } catch (error) {
        console.error('Terjadi kesalahan:', error);
    }
}
