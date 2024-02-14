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
import emitter from '../eventbus';


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
    },
    pollForFileReady(filename) {
      const checkStatus = () => {
        axios.get(`https://api.valterbonez.com:443/status/${filename}`)
          .then(response => {
            if (response.data.status === 'ready') {
              emitter.emit('file-ready', true); // Emit an event when the file is ready
              clearInterval(this.pollingInterval);
            }
          }).catch(error => {
            console.error('Error polling for file status', error);
          });
      };

      this.pollingInterval = setInterval(checkStatus, 5000);
    },
  },
}

</script>

<style scoped>
button[disabled] {
  background-color: grey;
  cursor: not-allowed;
}
</style>

