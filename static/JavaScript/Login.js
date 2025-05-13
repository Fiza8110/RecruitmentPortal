async function login(event) {
    //event is passed in from the form submission.

    try {
        // alert("submit");
        event.preventDefault();//prevents default behaviour
        //Retrieves the values entered by the user in the input fields with IDs email and password.
        var email = document.getElementById('email').value;
        var password = document.getElementById('password').value;
        // alert(email + password); // Check if this executes

        const formData = new FormData();
        formData.append("username", email);
        formData.append("password", password);

        console.log("Form Data:", email, password); // Check data before sending
        //Sends a POST request to the backend /login endpoint.
        const response = await fetch("http://127.0.0.1:8000/login", {//Waits for the response from the server.
            method: "POST",
            body: formData,
        });

        console.log("Raw Response:", response); // Log response object
        //This waits for the HTTP response body to be read as plain text.
        const responseText = await response.text(); // Get raw response text
        console.log("Response Text:", responseText); 
        //This line parses the string (responseText) into a JavaScript object.
        const result = JSON.parse(responseText); // Try parsing it
        console.log("Parsed Response:", result); // Log parsed response

        if (response.ok) {
            //Stores important user information in localStorage 
            localStorage.setItem("access_token", result.access_token);
            localStorage.setItem("username", result.username);
            localStorage.setItem("email", result.email);
            localStorage.setItem("role", result.role);

           //Redirects the user to different pages depending on their role
            if (result.role == "user") {
                window.location.href = "/dashboard";
            } else {
                 
                window.location.href = "/hrDashboard";

            }
        } else {
            alert(result.msg || "Invalid credentials!");
        }
        //Catches any runtime errors 
    } catch (error) {
        console.error("Error:", error);
        alert("Something went wrong! Please try again.");
    }
}
