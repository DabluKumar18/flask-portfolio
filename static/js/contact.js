function submitContactForm() {

    const successMsg = document.getElementById("successMsg");
    const sendBtn = document.getElementById("sendBtn");
    const btnText = document.getElementById("btnText");
    const spinner = document.getElementById("spinner");

    if (!successMsg || !sendBtn || !btnText || !spinner) {
        console.error("Missing HTML IDs");
        return;
    }

    // Button loading state ON
    btnText.innerText = "Sending...";
    spinner.style.display = "inline-block";
    sendBtn.disabled = true;

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const phone = document.getElementById("phone").value;
    const message = document.getElementById("message").value;

    fetch("/api/contact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, phone, message })
    })
    .then(res => res.json())
    .then(data => {
        successMsg.style.display = "block";
        successMsg.innerText = "✅ Message sent successfully!";
        document.getElementById("contactForm").reset();
    })
    .catch(() => {
        successMsg.style.display = "block";
        successMsg.innerText = "❌ Something went wrong!";
    })
    .finally(() => {
        // Button loading state OFF
        btnText.innerText = "Send Message";
        spinner.style.display = "none";
        sendBtn.disabled = false;

        setTimeout(() => {
            successMsg.style.display = "none";
        }, 4000);
    });
}

function toggleMenu() {
    document.getElementById("navMenu").classList.toggle("show");
}

