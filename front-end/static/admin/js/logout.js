// Logout
document.addEventListener('DOMContentLoaded', function () {
    const logoutButton = document.getElementById('logoutButton');
    logoutButton.addEventListener('click', function (event) {
        event.preventDefault();
        // Remove access and refresh tokens from session storage
        sessionStorage.removeItem('access');
        sessionStorage.removeItem('refresh');
        window.location.href = 'login.html';
    });
});
