const API_BASE_URL = "http://127.0.0.1:8000/api";

export async function analyzeText(text) {
  const response = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text }),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Text analysis failed.");
  }

  return response.json();
}

export async function analyzeImage(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/analyze/image`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Image analysis failed.");
  }

  return response.json();
}

export async function analyzePdf(file) {
  const formData = new FormData();

  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/analyze/pdf`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "PDF analysis failed.");
  }

  return response.json();
}

export async function getReports(patientName = "") {
  const params = new URLSearchParams();

  if (patientName.trim()) {
    params.set("patient_name", patientName.trim());
  }

  const query = params.toString();
  const url = query
    ? `${API_BASE_URL}/reports?${query}`
    : `${API_BASE_URL}/reports`;

  const response = await fetch(url);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to fetch reports.");
  }

  return response.json();
}
export async function getReport(id) {
  const response = await fetch(`${API_BASE_URL}/reports/${id}`);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Failed to fetch report.");
  }

  return response.json();
}