async function login(event) {
    try {
        // alert("submit");
        event.preventDefault();

        var email = document.getElementById('email').value;
        var password = document.getElementById('password').value;
        // alert(email + password); // Check if this executes

        const formData = new FormData();
        formData.append("username", email);
        formData.append("password", password);

        console.log("Form Data:", email, password); // Check data before sending

        const response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            body: formData,
        });

        console.log("Raw Response:", response); // Log response object

        const responseText = await response.text(); // Get raw response text
        console.log("Response Text:", responseText); 

        const result = JSON.parse(responseText); // Try parsing it
        console.log("Parsed Response:", result); // Log parsed response

        if (response.ok) {
            localStorage.setItem("access_token", result.access_token);
            localStorage.setItem("username", result.username);
            localStorage.setItem("email", result.email);
            localStorage.setItem("role", result.role);

            // showAlert("Login successful!");
            // alert("Role: " + result.role);

            if (result.role == "user") {
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
