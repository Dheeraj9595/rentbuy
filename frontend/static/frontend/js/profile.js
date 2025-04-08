<script>
    const tokenUrl = "http://localhost:8000/api/token/";
    const profileUrl = "http://localhost:8000/profile/";

    const username = "dheeraj"; // Ideally get this from a login form
    const password = "Dheeraj*95"; // NEVER hardcode in real apps

    let token = localStorage.getItem("access_token");

    function getCSRFToken() {
        let csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
        return csrfToken ? csrfToken.split('=')[1] : '';
    }

    async function fetchToken() {
        try {
            const response = await fetch(tokenUrl, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                token = data.access;
                localStorage.setItem("access_token", token);
                console.log("Token refreshed!");
            } else {
                console.error("Token fetch failed");
            }
        } catch (error) {
            console.error("Error fetching token", error);
        }
    }

    async function fetchProfile() {
        if (!token) {
            await fetchToken();
        }

        try {
            const response = await fetch(profileUrl, {
                headers: {
                    'Authorization': `Bearer {token}`
                }
            });

            if (!response.ok) {
                // Token might be expired, refresh and try again
                await fetchToken();
                return await fetchProfile();
            }

            const data = await response.json();
            document.getElementById("username").value = data.username;
            document.getElementById("email").value = data.email;
            document.getElementById("first_name").value = data.first_name || "";
            document.getElementById("last_name").value = data.last_name || "";

        } catch (error) {
            document.getElementById("message").textContent = "Error fetching profile.";
            console.error(error);
        }
    }

    async function updateProfile() {
        const updatedData = {
            email: document.getElementById("email").value,
            first_name: document.getElementById("first_name").value,
            last_name: document.getElementById("last_name").value
        };

        try {
            const response = await fetch(profileUrl, {
                method: "PATCH",
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify(updatedData)
            });

            const responseData = await response.json();

            if (response.ok) {
                document.getElementById("message").textContent = "Profile updated successfully!";
            } else {
                document.getElementById("message").textContent = responseData.detail || "Failed to update profile.";
            }
        } catch (error) {
            document.getElementById("message").textContent = "Error updating profile.";
            console.error(error);
        }
    }

    fetchProfile();
</script>
