const $ = (id) => document.getElementById(id);
let molecularViewer = null;
let currentStructure = null;

function showResult(target, data) {
  const node = $(target);
  node.classList.remove("muted");
  const pre = document.createElement("pre");
  pre.textContent = typeof data === "string" ? data : JSON.stringify(data, null, 2);
  node.replaceChildren(pre);
}

async function api(url, options = {}) {
  const response = await fetch(url, options);
  const payload = await response.json();
  if (!response.ok) throw new Error(payload.detail || "Request failed");
  return payload;
}

function showError(target, error) {
  showResult(target, {error: error.message});
}

function setStructureStatus(message, isError = false) {
  const status = $("structure-status");
  status.textContent = message;
  status.classList.toggle("error-text", isError);
}

function selectedStructureStyle() {
  const selected = $("structure-style").value;
  if (selected === "stick") return {stick: {}};
  if (selected === "sphere") return {sphere: {scale: 0.32}};
  return {cartoon: {color: "spectrum"}};
}

function applyStructureStyle() {
  if (!molecularViewer || !currentStructure) return;
  molecularViewer.setStyle({}, selectedStructureStyle());
  molecularViewer.render();
}

function resetStructureView() {
  if (!molecularViewer || !currentStructure) return;
  molecularViewer.zoomTo();
  molecularViewer.render();
}

async function checkHealth() {
  try {
    await api("/api/health");
    $("api-status").textContent = "online";
  } catch {
    $("api-status").textContent = "offline";
  }
}

$("search-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  showResult("search-results", "Searching NCBI…");
  try {
    const data = await api("/api/ncbi/search", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        database: $("database").value,
        term: $("search-term").value,
        limit: 10
      })
    });
    showResult("search-results", data);
  } catch (error) {
    showError("search-results", error);
  }
});

$("sequence-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  showResult("sequence-results", "Analyzing sequence…");
  try {
    const data = await api("/api/analyze/sequence", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        sequence: $("sequence-input").value,
        molecule: $("molecule").value
      })
    });
    showResult("sequence-results", data);
  } catch (error) {
    showError("sequence-results", error);
  }
});

$("upload-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const file = $("bio-file").files[0];
  if (!file) return;
  showResult("file-results", "Parsing biological file…");
  try {
    const form = new FormData();
    form.append("file", file);
    const data = await api("/api/files/analyze", {method: "POST", body: form});
    showResult("file-results", data);
  } catch (error) {
    showError("file-results", error);
  }
});

$("structure-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const pdbId = $("pdb-id").value.trim().toUpperCase();
  if (!/^[A-Z0-9]{4}$/.test(pdbId)) {
    setStructureStatus("Enter a valid four-character PDB identifier.", true);
    return;
  }

  setStructureStatus("Retrieving coordinate file from the RCSB PDB archive…");
  $("structure-viewer").replaceChildren();
  currentStructure = null;
  molecularViewer = null;

  try {
    const data = await api("/api/structures/rcsb/" + encodeURIComponent(pdbId));
    if (!window.$3Dmol || typeof window.$3Dmol.createViewer !== "function") {
      throw new Error("The 3Dmol.js viewer library did not load. Check the browser connection and reload the page.");
    }

    const viewerElement = $("structure-viewer");
    molecularViewer = window.$3Dmol.createViewer(viewerElement, {
      backgroundColor: "#0a1216",
      antialias: true
    });
    molecularViewer.addModel(data.structure_data, "cif");
    currentStructure = data;
    applyStructureStyle();
    molecularViewer.zoomTo();
    molecularViewer.render();
    molecularViewer.resize();

    setStructureStatus(
      "Loaded " + data.pdb_id + " · " + data.format.toUpperCase() +
      " · Source: " + data.source + ". " + data.interpretation_note
    );
  } catch (error) {
    $("structure-viewer").innerHTML = '<div class="viewer-placeholder">Structure could not be loaded.</div>';
    setStructureStatus(error.message, true);
    molecularViewer = null;
    currentStructure = null;
  }
});

$("structure-style").addEventListener("change", applyStructureStyle);
$("structure-reset").addEventListener("click", resetStructureView);

checkHealth();
