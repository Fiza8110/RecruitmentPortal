async function login(event) {
    try {
        event.preventDefault();

        var email = document.getElementById('email').value;
        var password = document.getElementById('password').value;

        const formData = new FormData();
        formData.append("username", email);
        formData.append("password", password);

        console.log("Form Data:", email, password);

        // ✅ Assign fetch result to `response`
        const response = await fetch("/login", {
            method: "POST",
            body: formData,
        });

        console.log("Raw Response:", response);

        const responseText = await response.text();
        console.log("Response Text:", responseText);

        const result = JSON.parse(responseText);
        console.log("Parsed Response:", result);

        if (response.ok) {
            localStorage.setItem("access_token", result.access_token);
            localStorage.setItem("username", result.username);
            localStorage.setItem("email", result.email);
            localStorage.setItem("role", result.role);

            if (result.role === "user") {
                window.location.href = "/dashboard";
            } else {
                window.location.href = "/hrDashboard";
            }
        } else {
            alert(result.msg || "Invalid credentials!");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong! Please try again.");
    }
}
