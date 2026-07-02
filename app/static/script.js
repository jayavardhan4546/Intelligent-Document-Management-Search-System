const uploadForm = document.getElementById("uploadForm");
const fileInput = document.getElementById("fileInput");
const uploadStatus = document.getElementById("uploadStatus");

const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");
const searchStatus = document.getElementById("searchStatus");
const resultsDiv = document.getElementById("results");

const documentsDiv = document.getElementById("documents");
const refreshDocsBtn = document.getElementById("refreshDocsBtn");

function setStatus(element, message, type) {
    element.textContent = message;
    element.className = `status ${type}`;
}

uploadForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const file = fileInput.files[0];
    if (!file) {
        setStatus(uploadStatus, "Please select a file first.", "error");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setStatus(uploadStatus, "Uploading and creating embeddings...", "");

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData,
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Upload failed");
        }

        setStatus(
            uploadStatus,
            `Uploaded successfully. Chunks created: ${data.chunks_created}`,
            "success"
        );
        fileInput.value = "";
        loadDocuments();
    } catch (error) {
        setStatus(uploadStatus, error.message, "error");
    }
});

searchForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const query = searchInput.value.trim();
    if (!query) {
        setStatus(searchStatus, "Please enter a search query.", "error");
        return;
    }

    setStatus(searchStatus, "Searching using FAISS...", "");
    resultsDiv.innerHTML = "";

    try {
        const response = await fetch(`/search?query=${encodeURIComponent(query)}&k=5`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Search failed");
        }

        setStatus(searchStatus, `Found ${data.results_count} result(s).`, "success");
        renderResults(data.results);
    } catch (error) {
        setStatus(searchStatus, error.message, "error");
    }
});

refreshDocsBtn.addEventListener("click", loadDocuments);

function renderResults(results) {
    if (!results.length) {
        resultsDiv.className = "results empty";
        resultsDiv.textContent = "No matching results found.";
        return;
    }

    resultsDiv.className = "results";
    resultsDiv.innerHTML = results
        .map(
            (item) => `
            <div class="result-item">
                <div class="result-title">
                    ${escapeHtml(item.filename)}
                    <span class="score">Similarity: ${item.score}</span>
                </div>
                <div class="chunk">${escapeHtml(item.content)}</div>
            </div>
        `
        )
        .join("");
}

async function loadDocuments() {
    try {
        const response = await fetch("/documents");
        const data = await response.json();
        renderDocuments(data.documents || []);
    } catch (error) {
        documentsDiv.textContent = "Could not load documents.";
    }
}

function renderDocuments(documents) {
    if (!documents.length) {
        documentsDiv.className = "documents empty";
        documentsDiv.textContent = "No documents uploaded yet.";
        return;
    }

    documentsDiv.className = "documents";
    documentsDiv.innerHTML = documents
        .map(
            (doc) => `
            <div class="document-item">
                <strong>${escapeHtml(doc.filename)}</strong><br />
                Chunks: ${doc.chunk_count} | Uploaded: ${doc.created_at}
            </div>
        `
        )
        .join("");
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

loadDocuments();
