import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [code, setCode] = useState('');
  const [completion, setCompletion] = useState('');

  const handleComplete = async () => {
    try {
      const response = await axios.post('http://localhost:3000/complete', { code });
      setCompletion(response.data.completion);
    } catch (error) {
      console.error("There was an error completing the code!", error);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Code Completion</h1>
        <textarea 
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="Enter your code here..."
        />
        <button onClick={handleComplete}>Complete Code</button>
        {completion && (
          <div>
            <h2>Completion:</h2>
            <pre>{completion}</pre>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;
