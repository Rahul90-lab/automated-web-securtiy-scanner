function startScan() {
    const url = document.getElementById('urlInput').value;
    if (!url) {
        alert("Please enter a URL!");
        return;
    }

    document.getElementById('loading').classList.remove("d-none");
    document.getElementById('results').innerHTML = "";

    fetch('/scan', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('loading').classList.add("d-none");

        document.getElementById('results').innerHTML = `
            <table class="table table-bordered">
                <tr><th>Scanned URL</th><td>${data.url}</td></tr>
                <tr><th>SQL Injection</th><td>${data["SQL Injection"].join(", ") || "None"}</td></tr>
                <tr><th>XSS</th><td>${data["XSS"].join(", ") || "None"}</td></tr>
                <tr><th>CSRF</th><td>${data["CSRF"].join(", ") || "None"}</td></tr>
                <tr><th>Open Redirect</th><td>${data["Open Redirect"].join(", ") || "None"}</td></tr>
            </table>
        `;
    });
}

function downloadReport(format) {
    window.location.href = `/download/${format}`;
}

function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
}
