// Login to back end API
document.addEventListener('DOMContentLoaded', function() {
    const loginButton = document.getElementById('loginButton');
    loginButton.addEventListener('click', function(event) {
        event.preventDefault();
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const loginData = {
            email: email,
            password: password
        };
        fetch('http://127.0.0.1:8000/api/user/login/', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(loginData)
        }).then(response => {
            if (!response.ok) {
                throw new Error('Login failed');
            }
            return response.json();
        }).then(data => {
            // Store access and refresh tokens in session storage
            sessionStorage.setItem('access', data.access);
            sessionStorage.setItem('refresh', data.refresh);
            // Redirect to the admin dashboard
            window.location.href = 'dashboard.html';
        }).catch(error => {
            console.error('Error:', error);
            alert('Login failed. Please check your credentials and try again.');
        });
    });
});
