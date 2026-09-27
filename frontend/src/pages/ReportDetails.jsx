import { useEffect, useState } from "react";
import { Link, useParams } from "react-router";

import { getReport } from "../services/api";

function ReportDetails() {
  const { id } = useParams();

  const [record, setRecord] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadReport = async () => {
      try {
        const data = await getReport(id);
        setRecord(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadReport();
  }, [id]);

  if (loading) {
    return (
      <section className="page">
        <p>Loading report...</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className="page">
        <p className="error">{error}</p>
      </section>
    );
  }

  const report = record.report;

  return (
    <section className="page">
      <Link to="/reports">← Back to Reports</Link>

    <h1>
    {report.patient_information?.name || "Unknown Patient"}
    </h1>

    <p className="report-subtitle">Clinical Report</p>

      <div className="report-section">
        <h3>Source</h3>
        <p>{record.source_type}</p>

        {record.original_filename && (
          <p>File: {record.original_filename}</p>
        )}

        <p>
          Created: {new Date(record.created_at).toLocaleString()}
        </p>
      </div>

      <div className="report-section">
        <h3>Summary</h3>
        <p>{report.report_summary}</p>
      </div>

      <div className="report-section">
        <h3>Patient Information</h3>
        <p>Name: {report.patient_information?.name || "Not documented"}</p>
        <p>Age: {report.patient_information?.age || "Not documented"}</p>
        <p>
          Gender: {report.patient_information?.gender || "Not documented"}
        </p>
        <p>
          MRN: {report.patient_information?.mrn || "Not documented"}
        </p>
      </div>

      <ReportListSection
        title="Symptoms"
        items={report.symptoms}
      />

      <ReportListSection
        title="Diagnoses"
        items={report.diagnoses}
      />

      <ReportListSection
        title="Medications"
        items={report.medications}
      />

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

      <ReportListSection
        title="Allergies"
        items={report.allergies}
      />

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

      <div className="report-section">
        <h3>Extracted Document Text</h3>
        <pre className="extracted-text">
          {record.extracted_text || "No extracted text available."}
        </pre>
      </div>
    </section>
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

export default ReportDetails;