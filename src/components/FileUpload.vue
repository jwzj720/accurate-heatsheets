<template>
  <div>
    <h2>Upload a PDF</h2>
    <input type="file" @change="onFileChange" accept="application/pdf" />
    <button @click="upload">Upload</button>
    <p>{{ uploadMessage }}</p> <!-- Display the upload message here -->
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      selectedFile: null,
      isLoading: false,
      uploadMessage: '', // Add a new property for the upload message
    };
  },
  methods: {
    onFileChange(e) {
      this.selectedFile = e.target.files[0];
    },
    upload() {
      this.isLoading = true;
      let formData = new FormData();
      formData.append('file', this.selectedFile);

      axios.post('https://api.valterbonez.com:443/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then((response) => {
        console.log('SUCCESS!');
        const filename = response.data.filename;
        document.cookie = `filename=${filename}; path=/`;
        this.isLoading = false;
        this.uploadMessage = 'File uploaded successfully!'; // Set the success message
      })
      .catch(() => {
        console.log('FAILURE!');
        this.isLoading = false;
        this.uploadMessage = 'File upload failed!'; // Set the failure message
      });
    }
  }
}
</script>

<style scoped>
button[disabled] {
  background-color: grey;
  cursor: not-allowed;
}
</style>