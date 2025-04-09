        const tokenUrl = "http://localhost:8000/api/token/";
        const profileUrl = "http://localhost:8000/profile/"
        const token = getToken()

        let accessToken = null;

        async function loginUser() {
            const username = document.getElementById("username").value;
            const password = document.getElementById("password").value;

            try {
                const response = await fetch("http://localhost:8000/api/token/", {
                    method: "POST",
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ username, password })
                });

                const data = await response.json();

                if (response.ok) {
                    accessToken = data.access;
                    localStorage.setItem("accessToken", accessToken); // store in localStorage
                    document.getElementById("login-message").textContent = "Login successful!";
                    fetchProfile();  // auto-fetch profile
                } else {
                    document.getElementById("login-message").textContent = data.detail || "Login failed.";
                }
            } catch (error) {
                console.error("Login error:", error);
                document.getElementById("login-message").textContent = "Login error.";
            }
        }

        function getToken() {
            return localStorage.getItem("accessToken");
        }

        function getCSRFToken() {
            let csrfToken = document.cookie.split('; ').find(row => row.startsWith('csrftoken='));
            return csrfToken ? csrfToken.split('=')[1] : '';
        }
        async function fetchProfile() {
            try {
                const token = await getToken();
                const response = await fetch(profileUrl, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (!response.ok) throw new Error("Failed to fetch profile");

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

            const csrf = await getCSRFToken();
            const token = await getToken();

            const messageElement = document.getElementById("message");

            if (!token) {
                messageElement.textContent = "Token not found. Please login again.";
                messageElement.className = "error"; // optional: add error styling
                console.error("Token is undefined");
                return;
            }

            try {
                const response = await fetch(profileUrl, {
                    method: "PATCH",
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrf
                    },
                    body: JSON.stringify(updatedData)
                });

                const responseData = await response.json();

                if (response.ok) {
                    messageElement.textContent = "Profile updated successfully!";
                    messageElement.className = "success";

                    // Auto-hide after 5 seconds
                    setTimeout(() => {
                        messageElement.textContent = "";
                        messageElement.className = "";
                    }, 5000);
                } else {
                    messageElement.textContent = responseData.detail || "Failed to update profile.";
                    messageElement.className = "error";
                }
            } catch (error) {
                messageElement.textContent = "Error updating profile.";
                messageElement.className = "error";
                console.error(error);
            }
        }


        fetchProfile();