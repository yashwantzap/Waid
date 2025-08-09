import React, { useState } from 'react';
import axios from 'axios';
import Loader from '../components/Loader';

export default function Debugger() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Please select a Python file");
    const formData = new FormData();
    formData.append('file', file);
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:5000/debug', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setResult(res.data.result);
    } catch {
      alert("Error debugging file");
    }
    setLoading(false);
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold">Python Code Debugger</h2>
      <input type="file" accept=".py" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} className="bg-blue-600 text-white px-4 py-2 mt-2 rounded">
        Upload & Debug
      </button>
      {loading && <Loader />}
      {result && (
        <pre className="mt-4 p-4 bg-gray-100 rounded border">
          {result}
        </pre>
      )}
    </div>
  );
}
