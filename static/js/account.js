function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

function populateUserData() {
    const token = getCookie('token');
    if (!token) {
        console.error('No token found in cookies');
        return;
    }
    fetch('/api/user', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(data => {
            if (data && data.username) {
                document.getElementById('username').value = data.username; // Set the username in the input field
            } else {
                console.error('Error: No username found in the response');
                alert('Failed to load user data.');
            }
        })
        .catch(error => {
            console.error('Error fetching user data:', error);
            alert('An error occurred while fetching user data.');
        });
}


function submitForm(e) {
    e.preventDefault(); // Prevent form submission
    const username = document.getElementById('username').value;

    const token = getCookie('token');
    if (!token) {
        console.error('No token found in cookies');
        return;
    }

    fetch('/api/user/', {
        method: 'UPDATE',
        headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username }),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // alert('Profile updated successfully!');
                console.log('Profile updated successfully!')
            } else {
                alert('Error updating profile: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while updating the profile.');
        });
};



function deleteProfile() {
    if (confirm('Are you sure you want to delete your profile? This action cannot be undone.')) {
        const token = getCookie('token');
        if (!token) {
            console.error('No token found in cookies');
            return;
        }
        fetch('/api/user/', {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // alert('Profile deleted successfully.');
                    console.log('Profile deleted successfully.')
                    window.location.href = '/'; // Redirect to home page
                } else {
                    alert('Error deleting profile: ' + data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while deleting the profile.');
            });
    }
};

async function main() {
    populateUserData()
    document.getElementById('deleteProfileButton').addEventListener('click', deleteProfile)
    document.getElementById('logoutButton').addEventListener('click', () => { window.location.href = '/logout/' })
    addEventListener("submit", submitForm);
}

document.addEventListener('DOMContentLoaded', main);