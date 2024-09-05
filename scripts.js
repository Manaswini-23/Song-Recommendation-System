document.getElementById('recommendationForm').addEventListener('submit', async function(event) {
    event.preventDefault();
    const genre = document.getElementById('genre').value;
    const mood = document.getElementById('mood').value;
    const response = await fetch('/recommend', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `genre=${genre}&mood=${mood}`
    });
    const data = await response.json();
    const songList = document.getElementById('songList');
    songList.innerHTML = '';
    if (data.success) {
        data.songs.forEach(song => {
            const songItem = document.createElement('div');
            songItem.classList.add('song-item');
            songItem.innerHTML = `
                <span>${song.name} - ${song.artist}</span>
                <iframe src="https://open.spotify.com/embed/track/${song.url.split('/').pop()}" width="300" height="80" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>`;
            songList.appendChild(songItem);
        });
    } else {
        songList.innerHTML = `<p>${data.message}</p>`;
    }
});
