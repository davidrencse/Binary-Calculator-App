import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [result, setResult] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchCalculation = async () => {
      if (!input.trim()) {
        setResult('0');
        return;
      }

      try {
        const response = await fetch(`${process.env.REACT_APP_API_URL}/calculate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ expression: input })
        });
        const data = await response.json();

        if (data.error) {
          setError(data.error);
          setResult('');
        } else {
          setResult(data.result.toString());
          setError('');
        }
      } catch (err) {
        setError('Connection error');
      }
    };

    // Debounce API calls
    const timer = setTimeout(fetchCalculation, 500);
    return () => clearTimeout(timer);
  }, [input]);

  const handleChange = (e) => {
    const value = e.target.value;
    // Basic client-side validation
    if (/^[\d+\-*/().\s]*$/.test(value)) {
      setInput(value);
    }
  };

  return (
    <div className="calculator">
      <h1>Calculator</h1>
      <input
        type="text"
        value={input}
        onChange={handleChange}
        placeholder="Type expression like 9+(4+1)/2"
        autoFocus
      />
      <div className="result">
        {error ? <span className="error">{error}</span> : result}
      </div>
      <div className="instructions">
        <p>Allowed: Numbers (0-9), Operators (+ - * /), Parentheses</p>
      </div>
    </div>
  );
}

export default App;
