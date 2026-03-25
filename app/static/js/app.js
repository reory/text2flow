let currentUrl = null; // Track the previous URL

async function generate() {
    const text = document.getElementById("diagram-text").value;

    const response = await fetch("/api/render", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
    });

    if (response.ok) {
        const blob = await response.blob();
        
        // Clean up the old URL to save memory
        if (currentUrl) URL.revokeObjectURL(currentUrl);
        
        currentUrl = URL.createObjectURL(blob);
        document.getElementById("preview-img").src = currentUrl;
    } else {
        alert("Failed to render. Check your syntax (A -> B)");
    }
}
