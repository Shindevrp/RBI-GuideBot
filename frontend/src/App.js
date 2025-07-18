import React, { useState } from 'react';
import './App.css';

function App() {
  const [query, setQuery] = useState('');
  const [response, setResponse] = useState(null);
  const [sources, setSources] = useState([]);
  const [chartUrl, setChartUrl] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResponse(null);
    setSources([]);
    setChartUrl(null);
    try {
      const formData = new FormData();
      formData.append('query', query);
      const res = await fetch('/ask', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      setResponse(data.answer);
      setSources(data.sources);
      setChartUrl(data.chart);
    } catch (err) {
      setResponse('Error fetching response.');
    }
    setLoading(false);
  };

  return (
    <div className="container">
      <h1>RBI GuideBot</h1>
      <form onSubmit={handleSubmit} className="query-form">
        <input
          type="text"
          value={query}
          onChange={e => setQuery(e.target.value)}
          placeholder="Ask about NBFC compliance..."
          className="query-input"
        />
        <button type="submit" className="submit-btn" disabled={loading}>
          {loading ? 'Loading...' : 'Ask'}
        </button>
      </form>
      {response && (
        <div className="response-block">
          <h2>Answer</h2>
          <p>{response}</p>
          {sources.length > 0 && (
            <div className="sources">
              <h3>Sources</h3>
              <ul>
                {sources.map((src, idx) => (
                  <li key={idx}>{src}</li>
                ))}
              </ul>
            </div>
          )}
          {chartUrl && (
            <div className="chart-block">
              <h3>Chart</h3>
              <img src={chartUrl} alt="Chart" style={{maxWidth: '100%'}} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
