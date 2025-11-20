const dropArea = document.getElementById("drop-area");
const fileElem = document.getElementById("fileElem");
const convertBtn = document.getElementById("convertBtn");
const uploadForm = document.getElementById("uploadForm");

const notification = document.getElementById("notification");
const progressContainer = document.getElementById("progressContainer");
const progressBar = document.getElementById("progressBar");

const resultSection = document.getElementById("result");
const extractedText = document.getElementById("extractedText");
const copyBtn = document.getElementById("copyBtn");
const clearBtn = document.getElementById("clearBtn");

// New elements for preview
const imagePreviewContainer = document.getElementById("image-preview-container");
const imagePreview = document.getElementById("image-preview");


// --- Event Listeners ---

// Click to open file dialog
dropArea.addEventListener("click", () => fileElem.click());

// Drag events
dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropArea.style.borderColor = "#0070f3"; // Visual feedback on hover
});
dropArea.addEventListener("dragleave", () => {
    dropArea.style.borderColor = "#2a3a5d";
});
dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.style.borderColor = "#2a3a5d";
    fileElem.files = e.dataTransfer.files;
    handleFileSelection();
});

// Manual file selection
fileElem.addEventListener("change", handleFileSelection);


// --- Functions ---

function handleFileSelection() {
    toggleConvert();
    if (fileElem.files && fileElem.files.length > 0) {
        // Show image preview
        const file = fileElem.files[0];
        if (file.type.startsWith('image/')) {
            const reader = new FileReader();
            reader.onload = (e) => {
                imagePreview.src = e.target.result;
                imagePreviewContainer.style.display = "block";
                dropArea.style.display = "none"; // Hide drop area when file is selected
            };
            reader.readAsDataURL(file);
        } else {
            // Handle non-image file selection (based on server check)
            showNotification("Please select an image file.", "error");
            imagePreviewContainer.style.display = "none";
            imagePreview.src = "#";
        }
    } else {
        // No file selected, reset UI
        imagePreviewContainer.style.display = "none";
        imagePreview.src = "#";
        dropArea.style.display = "flex";
    }
}

function toggleConvert() {
    // Disable button if no file is selected
    convertBtn.disabled = !(fileElem.files && fileElem.files.length > 0);
}

// Notification helper
function showNotification(message, type = "success") {
    notification.textContent = message;
    notification.className = `notification ${type} show`;
    setTimeout(() => {
        notification.classList.remove("show");
    }, 3000); // Increased visibility time
}

// Auto-resize textarea to content
function autoresizeTextarea(el) {
    el.style.height = "auto";
    // Added a more reasonable max height and minimum height
    el.style.height = Math.max(160, Math.min(el.scrollHeight, 600)) + "px";
}

// Intercept form submit to use XHR (for progress)
uploadForm.addEventListener("submit", (e) => {
    e.preventDefault();
    if (!(fileElem.files && fileElem.files.length > 0)) {
        showNotification("Please upload an image first.", "error");
        return;
    }

    // Clear previous results
    resultSection.style.display = "none";
    extractedText.value = "";

    const formData = new FormData(uploadForm);

    // Show progress bar and reset
    progressContainer.style.display = "block";
    progressBar.style.width = "0%";
    progressBar.textContent = "0%";
    convertBtn.disabled = true; // Disable button during processing

    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/upload", true);
    xhr.responseType = "text";

    // Upload progress (mainly for large files)
    xhr.upload.onprogress = (event) => {
        if (event.lengthComputable) {
            const percent = Math.round((event.loaded / event.total) * 100);
            progressBar.style.width = percent + "%";
            progressBar.textContent = percent + "%";
        }
    };

    // Total progress (Upload + Server Processing)
    xhr.onprogress = (event) => {
        // This event fires for the download (response) phase, which can be seen as
        // server processing time since the response is small (text).
        if (event.lengthComputable) {
            const uploadPercent = 100; // Assume upload is done
            // The total is usually not computable for streaming text response
            // For simple visual, we can 'park' the bar at 95% during server process
            progressBar.style.width = "95%";
            progressBar.textContent = "Processing...";
        }
    };


    xhr.onload = () => {
        progressContainer.style.display = "none";
        convertBtn.disabled = false; // Re-enable button after response

        if (xhr.status >= 200 && xhr.status < 300) {
            const text = xhr.response || "";
            extractedText.value = text.trim() || "(No text detected)";
            autoresizeTextarea(extractedText);
            resultSection.style.display = "block";
            showNotification("Image processed successfully!", "success");
        } else {
            const errorMessage = xhr.responseText || "Conversion failed.";
            showNotification(errorMessage, "error");
        }
    };

    xhr.onerror = () => {
        progressContainer.style.display = "none";
        convertBtn.disabled = false;
        showNotification("Network error. Please try again.", "error");
    };

    xhr.send(formData);
});

// Copy and clear actions
copyBtn.addEventListener("click", async () => {
    try {
        await navigator.clipboard.writeText(extractedText.value || "");
        showNotification("Copied to clipboard!", "success");
    } catch {
        showNotification("Copy failed. Please copy manually.", "error");
    }
});

clearBtn.addEventListener("click", () => {
    // A full page reload is a simple and effective way to reset the UI state
    // For a smoother reset, you could hide/clear all elements manually instead
    window.location.reload();
});