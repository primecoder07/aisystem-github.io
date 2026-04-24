async function submitData() {

    let file = document.getElementById("resume").files[0];
    let q1 = document.getElementById("q1").value;
    let q2 = document.getElementById("q2").value;

    if (!file) {
        alert("Please upload your resume!");
        return;
    }

    let formData = new FormData();
    formData.append("resume", file);
    formData.append("q1", q1);
    formData.append("q2", q2);

    let response = await fetch("/analyze", {
        method: "POST",
        body: formData
    });

    let data = await response.json();

    document.getElementById("result").innerHTML = `
        <h3>Recommended Career: ${data.career}</h3>
        <p>${data.reason}</p>
    `;
}
