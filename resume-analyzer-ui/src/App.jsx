import { useState, useEffect } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [role, setRole] = useState("");
  const [roles, setRoles] = useState([]);
  const [filteredRoles, setFilteredRoles] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [visitorCount, setVisitorCount] = useState(null);

  const [errorMessage, setErrorMessage] = useState("");   // INLINE ERROR
  const [isRoleValid, setIsRoleValid] = useState(true);   // VALIDATION FLAG

  // Visitor counter
  useEffect(() => {
    fetch("http://localhost:8000/visitor-count/increment")
      .then(res => res.json())
      .then(data => setVisitorCount(data.count))
      .catch(() => {});
  }, []);

  // Fetch available roles
  useEffect(() => {
    fetch("http://localhost:8000/roles")
      .then(res => res.json())
      .then(data => setRoles(data.roles))
      .catch(() => console.error("Error loading roles"));
  }, []);

  // Auto-suggestion logic + closest match
  const handleRoleChange = (e) => {
    const value = e.target.value;
    setRole(value);
    setErrorMessage("");

    if (value.trim() === "") {
      setFilteredRoles([]);
      setIsRoleValid(false);
      return;
    }

    const suggestions = roles.filter((r) =>
      r.toLowerCase().includes(value.toLowerCase())
    );

    setFilteredRoles(suggestions);

    // Check if valid role
    const valid = roles.includes(value.toLowerCase());
    setIsRoleValid(valid);

    // Auto-suggest closest valid role
    if (!valid && suggestions.length > 0) {
      setErrorMessage(`Did you mean: ${suggestions[0]} ?`);
    }
  };

  const selectRole = (r) => {
    setRole(r);
    setFilteredRoles([]);
    setErrorMessage("");
    setIsRoleValid(true);
  };

  const analyzeResume = async () => {
    if (!file || !role) {
      setErrorMessage("Please upload a resume and select a valid role.");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        `http://localhost:8000/analyze?target_role=${encodeURIComponent(role)}`,
        {
          method: "POST",
          headers: { "X-API-Key": "ra_7Kx92mLpQwZf4Nn8TyH3RsBc" },
          body: formData
        }
      );

      if (!response.ok) {
        const errorData = await response.json();

        setErrorMessage(
          `❌ ${errorData.error}\nAvailable roles: ${errorData.available_roles.join(", ")}`
        );

        setLoading(false);
        return;
      }

      const data = await response.json();
      setResult(data);

    } catch {
      setErrorMessage("Error analyzing resume");
    }

    setLoading(false);
  };

  return (
    <div className="page">
      <div className="container">
        <h1 className="title">Resume Analyzer</h1>

        {visitorCount !== null && (
          <p className="visitor-label">Visitor Count: {visitorCount}</p>
        )}

        <div className="card">
          <label>Target Role</label>

          {/* AUTOCOMPLETE INPUT */}
          <input
            type="text"
            placeholder="Start typing a role..."
            value={role}
            onChange={handleRoleChange}
            className={`border p-2 rounded w-full ${!isRoleValid ? "border-red-500" : ""}`}
          />

          {/* INLINE ERROR BOX */}
          {errorMessage && (
            <div className="bg-red-100 text-red-700 p-2 rounded mt-2">
              {errorMessage}
            </div>
          )}

          {/* SUGGESTION LIST */}
          {filteredRoles.length > 0 && (
            <ul className="suggestions-list">
              {filteredRoles.map((r) => (
                <li
                  key={r}
                  onClick={() => selectRole(r)}
                  className="suggestion-item"
                >
                  {r}
                </li>
              ))}
            </ul>
          )}

          <label>Upload Resume (PDF or DOCX)</label>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
          />

          {/* DISABLE BUTTON IF ROLE INVALID */}
          <button
            onClick={analyzeResume}
            disabled={loading || !isRoleValid}
            className={`${(!isRoleValid ? "opacity-50 cursor-not-allowed" : "")}`}
          >
            {loading ? "Analyzing..." : "Analyze Resume"}
          </button>
        </div>

        {result && (
          <div className="result-card">
            <h2>Analysis Result</h2>

            <div className="score-grid">
              <div className="score-box">
                <h4>ATS Score</h4>
                <p>{result.ats_score}</p>
              </div>
              <div className="score-box">
                <h4>Role Match</h4>
                <p>{result.role_match_score}</p>
              </div>
              <div className="score-box">
                <h4>Readability</h4>
                <p>{result.readability_score}</p>
              </div>
            </div>

            <h3>Missing Keywords</h3>
            <div className="tags">
              {result.missing_keywords.map((kw, i) => (
                <span key={i} className="tag">{kw}</span>
              ))}
            </div>

            <h3>Recommendations</h3>
            <ul>
              {result.recommendations.map((rec, i) => (
                <li key={i}>{rec}</li>
              ))}
            </ul>

            <h3>Extracted Sections</h3>
            <pre className="sections">
              {JSON.stringify(result.sections, null, 2)}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;