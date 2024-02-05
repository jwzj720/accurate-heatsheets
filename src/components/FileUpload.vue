<template>
    <div>
      <h2>Upload a PDF</h2>
      <input type="file" @change="onFileChange" accept="application/pdf" />
      <button @click="upload">Upload</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        selectedFile: null
      }
    },
    methods: {
      onFileChange(e) {
        this.selectedFile = e.target.files[0];
      },
      upload() {
        let formData = new FormData();
        formData.append('file', this.selectedFile);
  
        axios.post('http://valterbonez.tplinkdns.com:8081/upload', formData, {
            'Content-Type': 'multipart/form-data'
          }).then((response) => {
          console.log('SUCCESS!');
          // Get filename from the response
          const filename = response.data.filename;

          // Set filename as a cookie
          document.cookie = `filename=${filename}; path=/`;
        })
        .catch(() => {
          console.log('FAILURE!');
        });
      }
    }
  }
  </script>