document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("signupForm");

  form.addEventListener("submit", async (event) => {
      event.preventDefault();

      const formData = new FormData(form);

      try {
          const response = await fetch("/register", {
              method: "POST",
              body: formData,
          });

          const result = await response.json();
          if (response.ok) {
              alert(result.success_msg);
              window.location.href = "/login";  // Redirect after success
          } else {
              alert(result.msg);
          }
      } catch (error) {
          console.error("Error:", error);
      }
  });
});
