<template>
  <div>
    <h2>Download New Heatsheet</h2>
    <button :disabled="!isFileReady" @click="downloadItem">
      <span v-if="isProcessing">
        <i class="fa fa-spinner fa-spin"></i> Processing...
      </span>
      <span v-else-if="isLoading">
        <i class="fa fa-spinner fa-spin"></i> Loading...
      </span>
      <!-- Display "Download" only when the file is ready, otherwise no text -->
      <span v-else-if="isFileReady">
        Download
      </span>
      <!-- Nothing in the initial state, the button should be empty -->
    </button>
  </div>
</template>
<script>
import axios from 'axios';
import emitter from '../eventbus';

export default {
  mounted() {
    emitter.on('upload-started', () => {
      this.isProcessing = true;
      this.isFileReady = false;
    });
    emitter.on('file-ready', (isReady) => {
      this.isProcessing = false;
      this.isFileReady = isReady;
      if (isReady) {
        this.isLoading = false; // Assuming the file is now ready to be downloaded
      }
    });
  },
  beforeUnmount() {
    emitter.off('upload-started');
    emitter.off('file-ready');
  },
  data() {
    return {
      isFileReady: false, // Track file readiness
      isLoading: false, // Track if the download is in progress
      isProcessing: false, // Track if the file is being processed
      uploadStarted: false,
    };
  },

  methods: {
    downloadItem() {
      if (!this.isFileReady) return;
      this.isLoading = true; // Set loading state to true when download starts

      // Get filename from a cookie
      const filename = this.getCookie('filename') || 'downloaded.csv'; // Default filename
      if (filename === 'downloaded.csv') {
        console.error('Filename not found in cookies');
        this.isLoading = false; // Set loading state to false if there's an error
        return;
      }
      axios.get(`https://api.valterbonez.com:443/pdf/${filename}`,{
        responseType: 'blob' // Set responseType to 'blob' to indicate binary data
      })
        .then(response => {
          console.log("File recieved!");
          const blob = new Blob([response.data], { type: 'text/csv' }); // looks for a file of type csv
          const link = document.createElement('a'); // Create new <a> tag
          link.href = URL.createObjectURL(blob); // Set href to the blob URL

          link.download = "results_new.csv" // name of the file for the system to see
          link.click(); // Trigger the download
          URL.revokeObjectURL(link.href); // Free up the memory

          this.isLoading = false; // Set loading state to false when download is complete
        })
        .catch(error => {
          console.error(error);
          this.isLoading = false; // Set loading state to false if there's an error
        });
    },
    getCookie(name) {
      const value = `; ${document.cookie}`; // gets the cookie 
      const parts = value.split(`; ${name}=`); // splits the cookie
      if (parts.length === 2) return parts.pop().split(';').shift(); // returns the filename 
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