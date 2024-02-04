class AdviceApp {
    constructor() {
        this.adviceLink = document.getElementById('advice-link');
        this.videosLink = document.getElementById('videos-link');
        this.adviceList = document.getElementById('advice-list');
        this.addEventListeners();
    }

    addEventListeners() {
        this.adviceLink.addEventListener('click', (e) => this.fetchAdvice(e));
        this.videosLink.addEventListener('click', (e) => this.showVideos(e));
    }

    fetchAdvice(e) {
        e.preventDefault();
        fetch('/advice')
            .then(response => response.json())
            .then(data => {
                this.adviceList.innerHTML = '';
                data.forEach(item => {
                    const div = document.createElement('div');
                    div.className = 'advice-item';
                    div.textContent = `Topic ${item.index}: ${item.advice}`;
                    this.adviceList.appendChild(div);
                });
            })
            .catch(error => console.error('Error:', error));
    }

    showVideos(e) {
        e.preventDefault();
        // This page is empty in version 1
    }

    onSignIn(googleUser) {
        var id_token = googleUser.getAuthResponse().id_token;
        // Send the ID token to your server with a POST request
        fetch('/token_sign_in', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({token: id_token})
        }).then(function(response) {
            // Handle response from your backend
            console.log(response);
        });
    }
}

new AdviceApp();

    
function handleCredentialResponse(response) {
    const responsePayload = jwt_decode(response.credential);

    var id_token = response.credential;
        // Send the ID token to your server with a POST request
        fetch('/verify_token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({token: id_token})
        }).then(function(response) {
            // Handle response from your backend
            console.log(response);
        });

    console.log("ID: " + responsePayload.sub);
    console.log('Full Name: ' + responsePayload.name);
    console.log('Given Name: ' + responsePayload.given_name);
    console.log('Family Name: ' + responsePayload.family_name);
    console.log("Image URL: " + responsePayload.picture);
    console.log("Email: " + responsePayload.email);
}