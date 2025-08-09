import React, { useState } from 'react';
import axios from 'axios';
import DocumentEditor from '../components/DocumentEditor';
import Loader from '../components/Loader';

export default function DocuGen() {
  const [templateType, setTemplateType] = useState('');
  const [generatedDoc, setGeneratedDoc] = useState('');
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    if (!templateType) return alert("Please select a document type");
    setLoading(true);
    try {
      const res = await axios.post('http://localhost:5000/generate', { type: templateType });
      setGeneratedDoc(res.data.document);
    } catch (err) {
      alert("Error generating document");
    }
    setLoading(false);
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-bold">Document Generator</h2>
      <div className="mt-4 flex gap-2">
        <select value={templateType} onChange={(e) => setTemplateType(e.target.value)}>
          <option value="">Select Template</option>
          <option value="resume">Resume</option>
          <option value="contract">Contract</option>
          <option value="policy">Policy</option>
        </select>
        <button onClick={handleGenerate} className="bg-blue-600 text-white px-4 py-2 rounded">
          Generate
        </button>
      </div>

      {loading && <Loader />}
      {generatedDoc && <DocumentEditor content={generatedDoc} />}
    </div>
  );
}
