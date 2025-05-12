document.addEventListener("DOMContentLoaded", () => {
    const start_button = document.getElementById('start-button');
    start_button.addEventListener('click', start_session);
});

const livekit_url = 'ws://localhost:7880';

async function start_session() {
    const username = document.getElementById('username').value.trim();
    if (!username) {
        alert("Please enter a username.");
        return;
    }

    if (!window.livekit) {
        alert("LiveKit is not loaded. Please check your configuration.");
        return;
    }
    
    const { connect, Room, LocalParticipant } = window.livekit;
    const room = new Room();
    await room.connect(livekit_url, token);
}
// const token_url = '/videoconference/get-livekit-token/?identity=${encodeURIComponent(username)}$room=ma_salle';

// try {
//     const response = await fetch(token_url);
//     const data = await response.json();
//     const token = data.token;

//     await connect(room, livekit_url, token);

//     const local_tracks = await livekit.createLocalTracks();
//     await room.localParticipant.publishTracks(local_tracks);

//     const video_container = document.getElementById('videos');

//     //Afficher la video
//     local_tracks.forEach(track => {
//         if (track.kind === 'video') {
//             const elem = track.attach();
//             video_container.appendChild(elem);
//         }
//     });

//     //Afficher la vidéo des autres participants
//     room.on('trackSubscribed', (track, publication, participant) => {
//         const elem = track.attach();
//         video_container.appendChild(elem);
//     });
// } catch (error) {
//     console.error("Error connecting to LiveKit:", error);
//     alert("Failed to connect to the video conference. Please try again later.");
// }
