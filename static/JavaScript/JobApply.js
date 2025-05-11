
// const selectedJobTitle = localStorage.getItem("selectedJobTitle");
// if (selectedJobTitle) {
//     document.getElementById("jobTitle").value = selectedJobTitle;
// }
// async function ApplyJob(event) {
//   event.preventDefault(); // Prevent page reload

//   const formData = new FormData(); // Use FormData for file uploads

//   formData.append("job_title", document.getElementById("jobTitle").value);
//   formData.append("first_name", document.getElementById("firstName").value);
//   formData.append("last_name", document.getElementById("lastName").value);
//   formData.append("email", document.getElementById("email").value);
//   formData.append("mobile", document.getElementById("mobile").value);
//   formData.append("current_employee", document.querySelector('input[name="employed"]:checked').value);

//   // Ensure resume is selected and appended
//   const resumeFile = document.getElementById("resume").files[0];
//   if (resumeFile) {
//       formData.append("resume", resumeFile);
//   } else {
//       alert("No resume selected");
//   }

//   // If user is employed, send additional details
//   if (document.querySelector('input[name="employed"]:checked').value === "yes") {
//       formData.append("company_name", document.getElementById("companyName").value);
//       formData.append("company_location", document.getElementById("companyLocation").value);
//       formData.append("current_ctc", document.getElementById("currentCTC").value);
//       formData.append("expected_ctc", document.getElementById("expectedCTC").value);
//       formData.append("notice_period", document.getElementById("noticePeriod").value);
//   }

//   // Log FormData content manually
//   let formDataObject = {};
//   formData.forEach((value, key) => {
//       if (value instanceof File) {
//           formDataObject[key] = value.name; // Show only the file name, or metadata if needed
//       } else {
//           formDataObject[key] = value;
//       }
//   });
//   alert("Form Data:", formData); // Debugging, replace with actual form submission logic


//   try {
//       const response = await fetch("http://127.0.0.1:8000/applyJob", {
//           method: "POST",
//           body: formData,
//       });

//       const data = await response.json();
//       if (response.ok) {
//         console.log("Success:", data);
//         alert("Application Submitted Successfully!");
//         window.location.href ="/dashboard"
//     } else {
//         alert(result.msg || "Something went wrong");
//     }
      
   
//   } catch (error) {
//       console.error("Error:", error);
//       alert("Failed to Submit Application");
//   }
// }
