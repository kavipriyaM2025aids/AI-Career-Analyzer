function login() {
  let username = document.getElementById("username").value;
  let password = document.getElementById("password").value;

  fetch("http://127.0.0.1:5000/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({username, password})
  })
  .then(res => res.json())
  .then(data => {
    if(data.status === "success"){
      window.location.href = "/dashboard";
    } else {
      alert("Invalid login");
    }
  });
}
<i class="fas fa-user"></i>
function analyzeCareer() {
  let career = document.getElementById("career").value;
  let skills = document.getElementById("skills").value;

  fetch("http://127.0.0.1:5000/analyze-career", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({career, skills})
  })
  .then(res => res.json())
  .then(data => {
    document.getElementById("match").innerText = data.match + "%";
    document.getElementById("salary").innerText = data.salary;

    // show skills
    document.getElementById("matched").innerText = data.matched_skills.join(", ");
    document.getElementById("missing").innerText = data.missing_skills.join(", ");
  });
}
function uploadResume() {
    let fileInput = document.getElementById("resumeFile");
    let file = fileInput.files[0];

    let formData = new FormData();
    formData.append("file", file);

    fetch("/analyze-resume", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("resumeResult").innerHTML =
            JSON.stringify(data);
    });
}