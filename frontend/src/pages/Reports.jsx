import { useEffect, useState } from "react";
import { Link } from "react-router";

import { getReports } from "../services/api";

function Reports() {
  const [reports, setReports] = useState([]);
  const [searchName, setSearchName] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const data = await getReports();
        setReports(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchReports();
  }, []);

  const loadReports = async (name = "") => {
    setLoading(true);
    setError("");

    try {
      const data = await getReports(name);
      setReports(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = async (event) => {
    event.preventDefault();
    await loadReports(searchName);
  };

  const handleClear = async () => {
    setSearchName("");
    await loadReports();
  };

  return (
    <section className="page">
      <h1>Reports</h1>

      <form className="report-search" onSubmit={handleSearch}>
        <input
          type="text"
          placeholder="Search by patient name"
          value={searchName}
          onChange={(event) => setSearchName(event.target.value)}
        />

        <button type="submit" className="mode-button">
          Search
        </button>

        <button
          type="button"
          className="mode-button"
          onClick={handleClear}
        >
          Clear
        </button>
      </form>

      {loading && <p>Loading reports...</p>}

      {error && <p className="error">{error}</p>}

      {!loading && !error && reports.length === 0 && (
        <p>No reports found.</p>
      )}

      {!loading && !error && reports.length > 0 && (
        <div className="reports-list">
          {reports.map((item) => (
            <Link
              key={item.id}
              to={`/reports/${item.id}`}
              className="report-item"
            >
              <div>
                <h2>
                  {item.report?.patient_information?.name ||
                    "Unknown Patient"}
                </h2>

                <p>Source: {item.source_type}</p>

                {item.original_filename && (
                  <p>File: {item.original_filename}</p>
                )}

                <p>
                  Created:{" "}
                  {new Date(item.created_at).toLocaleString()}
                </p>
              </div>
            </Link>
          ))}
        </div>
      )}
    </section>
  );
}

export default Reports;