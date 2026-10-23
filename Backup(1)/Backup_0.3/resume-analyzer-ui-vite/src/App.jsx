import { useState, useEffect } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [role, setRole] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [visitorCount, setVisitorCount] = useState(null);

  // Visitor counter — increments once per visit
  useEffect(() => {
    fetch("http://localhost:8000/visitor-count/increment")
      .then(res => res.json())
      .then(data => setVisitorCount(data.count))
      .catch(() => {});
  }, []);

  const analyzeResume = async () => {
    if (!file || !role) {
      alert("Please upload a resume and enter a target role");
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
          headers: { "X-API-Key": "demo-key-123" },
          body: formData
        }
      );

      const data = await response.json();
      setResult(data);
    } catch {
      alert("Error analyzing resume");
    }

    setLoading(false);
  };

  return (
    <div className="page">
      <div className="container">
        <h1 className="title">Resume Analyzer</h1>

        {visitorCount !== null && (
          <p className="visitor-label">
            Visitor Count: {visitorCount}
          </p>
        )}

        <div className="card">
          <label>Target Role</label>
          <input
            type="text"
            placeholder="e.g., software developer"
            value={role}
            onChange={(e) => setRole(e.target.value)}
          />

          <label>Upload Resume (PDF or DOCX)</label>
          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
          />

          <button onClick={analyzeResume} disabled={loading}>
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