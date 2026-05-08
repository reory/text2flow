let currentBlob = null;
let currentFormat = null;

async function generate() {
    const text = document.getElementById("diagram-text").value;
    const format = document.getElementById("format-select").value;
    
    if (!text.trim()) {
        updateStatus("⚠ Please enter some text", "warning");
        return;
    }

    updateStatus("⏳ Rendering...", "loading");

    try {
        const response = await fetch("/api/render", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, format })
        });

        if (response.ok) {
            const blob = await response.blob();
            currentBlob = blob;
            currentFormat = format;
            
            // Display based on format
            const preview = document.getElementById("preview");
            
            if (format === "svg") {
                const svgText = await blob.text();
                preview.innerHTML = svgText;
                updateStatus("✓ Rendered as SVG (scalable)", "success");
            } else if (format === "png") {
                const url = URL.createObjectURL(blob);
                preview.innerHTML = `<img src="${url}" class="preview-image" />`;
                updateStatus("✓ Rendered as PNG", "success");
            } else if (format === "pdf") {
                preview.innerHTML = '<p class="preview-placeholder">PDF generated (use download to view)</p>';
                updateStatus("✓ Generated as PDF", "success");
            }
        } else {
            const errorText = await response.text();
            updateStatus(`❌ ${errorText}`, "error");
        }
    } catch (error) {
        updateStatus(`❌ Error: ${error.message}`, "error");
    }
}

async function downloadDiagram(format) {
    const text = document.getElementById("diagram-text").value;
    
    if (!text.trim()) {
        alert("Please enter some text first");
        return;
    }

    updateStatus("⏳ Exporting...", "loading");

    try {
        const response = await fetch("/api/render", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ text, format })
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            a.download = `flowchart.${format}`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            updateStatus(`✓ Downloaded as ${format.toUpperCase()}`, "success");
        } else {
            const errorText = await response.text();
            alert(`Failed to export: ${errorText}`);
            updateStatus("❌ Export failed", "error");
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
        updateStatus("❌ Error", "error");
    }
}

function clearInput() {
    document.getElementById("diagram-text").value = "";
    document.getElementById("preview").innerHTML = '<p class="preview-placeholder">Diagram will appear here</p>';
    updateStatus("Cleared", "info");
}

function updateStatus(message, type = "info") {
    const status = document.getElementById("status");
    status.textContent = message;
    status.className = `status status-${type}`;
}
