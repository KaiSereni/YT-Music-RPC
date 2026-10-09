let lastSong = "";
let checksSinceLastSend = 0;
const RESEND_INTERVAL = 10; // Resend after this many DOM checks

setInterval(() => {
    const titleEl = document.querySelector('yt-formatted-string.title.ytmusic-player-bar');
    const artistEl = document.querySelector('span.subtitle.ytmusic-player-bar');
    const progressEl = document.querySelector('#progress-bar');

    if (titleEl && artistEl && progressEl) {
        const title = titleEl.innerText;
        const artist = artistEl.innerText.split(' • ')[0]; 
        const progress = progressEl.getAttribute('value') || progressEl.value || 0; // In seconds
        const img = document.querySelector("#song-image img").src;
        const total = progressEl.getAttribute('aria-valuemax');
        const videoEl = document.querySelector('video');
        const paused = videoEl ? videoEl.paused : true;
        const href = window.location.href;

        checksSinceLastSend++;

        console.log("Paused: " + paused);

        // Send update if the song changes OR every RESEND_INTERVAL checks
        if (title !== lastSong || checksSinceLastSend >= RESEND_INTERVAL) {
            fetch('http://localhost:3232', {
                method: 'POST',
                body: JSON.stringify({ title, artist, progress, img, total, paused, href })
            }).catch(err => {}); 
            lastSong = title;
            checksSinceLastSend = 0;
        }
    }
}, 3000); // Checks DOM every 3 seconds