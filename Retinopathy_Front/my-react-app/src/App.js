import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [imageUrl, setImageUrl] = useState('');

  const onFileChange = event => {
    setFile(event.target.files[0]);
  };

  const onFileUpload = () => {
    const formData = new FormData();
    formData.append("image", file);
    axios.post('http://localhost:8000/process_image/', formData, { responseType: 'blob' })
      .then(response => {
        const localUrl = URL.createObjectURL(response.data);
        setImageUrl(localUrl);
      })
      .catch(error => console.log(error));
  };

  return (
    <div>
      <input type="file" onChange={onFileChange} />
      <button onClick={onFileUpload}>
        Upload!
      </button>
      {imageUrl && <img src={imageUrl} alt="Processed Image" />}
    </div>
  );
}

export default App;
