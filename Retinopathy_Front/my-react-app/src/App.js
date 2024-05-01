import React, { useState } from 'react';
import axios from 'axios';
import { Container, Row, Col, Form, Button, Image, Navbar } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [file, setFile] = useState(null);
  const [imageUrl, setImageUrl] = useState('');
  const [imageName, setImageName] = useState('');

  const onFileChange = event => {
    setFile(event.target.files[0]);
    setImageName(event.target.files[0].name);
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
    <>
      <Navbar bg="primary" variant="dark">
        <Container>
          <Navbar.Brand>Retinopathy</Navbar.Brand>
        </Container>
      </Navbar>
      <Container style={{ marginTop: '20px' }}>
        <Row className="justify-content-md-center">
          <Col md={6}>
            <Form>
              <Form.Group controlId="formFile" className="mb-3">
                <Form.Label>Выберите фото для разметки</Form.Label>
                <Form.Control type="file" onChange={onFileChange} />
              </Form.Group>
              <Button variant="primary" onClick={onFileUpload}>
                Загрузить!
              </Button>
            </Form>
          </Col>
        </Row>
        <Row className="justify-content-md-center" style={{ marginTop: '20px' }}>
          <Col md={6} className="text-center">
            {imageUrl && <>
              <Image src={imageUrl} alt="Processed Image" rounded />
              <br />
              <a href={imageUrl} download={imageName || "downloaded_image"}>
                <Button variant="success" style={{ marginTop: '10px' }}>
                  Сохранить фото
                </Button>
              </a>
            </>}
          </Col>
        </Row>
      </Container>
    </>
  );
}

export default App;
