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
      selectedFile: null,
      isLoading: false, // Add a new loading state
    };
  },
  methods: {
    onFileChange(e) {
      this.selectedFile = e.target.files[0];
    },
    upload() {
      this.isLoading = true; // Set loading state to true when download starts
      let formData = new FormData();
      formData.append('file', this.selectedFile);

      axios.post('https://api.valterbonez.com:443/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      }).then((response) => {
        console.log('SUCCESS!');

        // Get filename from the response
        const filename = response.data.filename;

        // Set filename as a cookie
        document.cookie = `filename=${filename}; path=/`;
        this.isLoading = false; // Set loading state to false if there's an error
      })
      .catch(() => {
        console.log('FAILURE!');
        this.isLoading = false; // Set loading state to false if there's an error
  
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