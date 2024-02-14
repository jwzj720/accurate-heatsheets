<template>
  <div>
    <h2>Download New Heatsheet</h2>
    <button :disabled="isLoading" @click="downloadItem">
      <span v-if="isLoading">
        <i class="fa fa-spinner fa-spin"></i> Loading
      </span>
      <span v-else>
        Download
      </span>
    </button>
  </div>
</template>

<script>
import axios from 'axios';
import emitter from '@/plugins/eventbus';

export default {
  mounted() {
    emitter.on('file-ready', (isReady) => {
      if (isReady) {
        this.isFileReady = true;
      }
    });
  },
  beforeUnmount() {
    emitter.off('file-ready'); // Clean up the event listener when the component unmounts
  },
  data() {
    return {
      isFileReady: false, // Track file readiness
      isLoading: false,
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