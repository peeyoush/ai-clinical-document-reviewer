import { useState } from "react";

import {
  analyzeText,
  analyzeImage,
  analyzePdf,
} from "../services/api";

function Analyze() {
  const [mode, setMode] = useState("text");
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);

  const [report, setReport] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleModeChange = (newMode) => {
    setMode(newMode);
    setText("");
    setFile(null);
    setReport(null);
    setError("");
  };

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0] || null;
    setFile(selectedFile);
    setError("");
  };

  const handleAnalyze = async () => {
    setLoading(true);
    setError("");
    setReport(null);

    try {
      let result;

      if (mode === "text") {
        if (!text.trim()) {
          throw new Error("Please enter the clinical document text.");
        }

        result = await analyzeText(text);
      }

      if (mode === "image") {
        if (!file) {
          throw new Error("Please select an image.");
        }

        result = await analyzeImage(file);
      }

      if (mode === "pdf") {
        if (!file) {
          throw new Error("Please select a PDF.");
        }

        result = await analyzePdf(file);
      }

      setReport(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="page analyze-page">
      <div className="analyze-header">
        <h1>Analyze Document</h1>
        <p>
          Enter clinical text or upload a clinical image or PDF to generate a
          structured clinical review.
        </p>
      </div>

      <div className="analyze-box">
        <div className="mode-buttons">
          <button
            type="button"
            className={mode === "text" ? "mode-button active" : "mode-button"}
            onClick={() => handleModeChange("text")}
          >
            Text
          </button>

          <button
            type="button"
            className={mode === "image" ? "mode-button active" : "mode-button"}
            onClick={() => handleModeChange("image")}
          >
            Image
          </button>

          <button
            type="button"
            className={mode === "pdf" ? "mode-button active" : "mode-button"}
            onClick={() => handleModeChange("pdf")}
          >
            PDF
          </button>
        </div>

        {mode === "text" && (
          <div className="input-group">
            <label htmlFor="clinical-text">
              Clinical document text
            </label>

            <textarea
              id="clinical-text"
              className="text-input"
              placeholder="Paste or type the clinical document here..."
              value={text}
              onChange={(event) => setText(event.target.value)}
            />

            <p className="input-help">
              Enter the clinical note exactly as it appears in the document.
            </p>
          </div>
        )}

        {mode === "image" && (
          <div className="input-group">
            <label htmlFor="image-file">
              Clinical image
            </label>

            <label htmlFor="image-file" className="file-box">
              <span>
                {file ? file.name : "Choose a PNG, JPG, JPEG, or WEBP image"}
              </span>

              <span className="file-button">
                Browse
              </span>
            </label>

            <input
              id="image-file"
              type="file"
              accept=".png,.jpg,.jpeg,.webp"
              onChange={handleFileChange}
              hidden
            />
          </div>
        )}

        {mode === "pdf" && (
          <div className="input-group">
            <label htmlFor="pdf-file">
              Clinical PDF
            </label>

            <label htmlFor="pdf-file" className="file-box">
              <span>
                {file ? file.name : "Choose a PDF document"}
              </span>

              <span className="file-button">
                Browse
              </span>
            </label>

            <input
              id="pdf-file"
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              hidden
            />
          </div>
        )}

        <button
          type="button"
          className="analyze-button"
          onClick={handleAnalyze}
          disabled={loading}
        >
          {loading ? "Analyzing..." : "Analyze Document"}
        </button>

        {error && (
          <p className="error">
            {error}
          </p>
        )}
      </div>

      {report && <ClinicalReview report={report} />}
    </section>
  );
}

function ClinicalReview({ report }) {
  return (
    <div className="report">
      <h2>Clinical Review</h2>

      <div className="report-section">
        <h3>Summary</h3>
        <p>{report.report_summary}</p>
      </div>

      <div className="report-section">
        <h3>Patient Information</h3>
        <p>Name: {report.patient_information?.name || "Not documented"}</p>
        <p>Age: {report.patient_information?.age || "Not documented"}</p>
        <p>Gender: {report.patient_information?.gender || "Not documented"}</p>
        <p>MRN: {report.patient_information?.mrn || "Not documented"}</p>
      </div>

      <ReportListSection title="Symptoms" items={report.symptoms} />
      <ReportListSection title="Diagnoses" items={report.diagnoses} />
      <ReportListSection title="Medications" items={report.medications} />

      <div className="report-section">
        <h3>Vitals</h3>
        <p>
          Blood Pressure:{" "}
          {report.vitals?.blood_pressure || "Not documented"}
        </p>
        <p>
          Heart Rate:{" "}
          {report.vitals?.heart_rate || "Not documented"}
        </p>
        <p>
          Temperature:{" "}
          {report.vitals?.temperature || "Not documented"}
        </p>
        <p>
          Respiratory Rate:{" "}
          {report.vitals?.respiratory_rate || "Not documented"}
        </p>
        <p>
          Oxygen Saturation:{" "}
          {report.vitals?.oxygen_saturation || "Not documented"}
        </p>
      </div>

      <ReportListSection title="Allergies" items={report.allergies} />
      <ReportListSection
        title="Clinical Observations"
        items={report.clinical_observations}
      />
      <ReportListSection
        title="Clinical Concerns"
        items={report.clinical_concerns}
      />
      <ReportListSection
        title="Missing Information"
        items={report.missing_information}
      />
      <ReportListSection
        title="Potential Inconsistencies"
        items={report.potential_inconsistencies}
      />
      <ReportListSection
        title="Requires Review"
        items={report.requires_review}
      />
    </div>
  );
}

function ReportListSection({ title, items = [] }) {
  return (
    <div className="report-section">
      <h3>{title}</h3>

      {!items.length ? (
        <p>None documented.</p>
      ) : (
        <ul>
          {items.map((item, index) => (
            <li key={`${item}-${index}`}>{item}</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default Analyze;