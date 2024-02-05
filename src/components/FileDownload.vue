<template>
  <div>
    <h2>Download New Heatsheet</h2>
    <button @click="downloadItem">Download</button>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    downloadItem() {
      // Get filename from a cookie
      const filename = this.getCookie('filename') || 'downloaded.csv'; // Default filename

      axios.get(`heatsheet-api.vercel.app/pdf/${filename}`,{
        responseType: 'blob' // Set responseType to 'blob' to indicate binary data
      })
        .then(response => {
          console.log("new data");
          const blob = new Blob([response.data], { type: 'text/csv' }); // looks for a file of type csv
          const link = document.createElement('a'); // Create new <a> tag
          link.href = URL.createObjectURL(blob); // Set href to the blob URL

          link.download = "results_new.csv" // name of the file for the system to see
          link.click(); // Trigger the download
          URL.revokeObjectURL(link.href); // Free up the memory
        })
        .catch(console.error);
    },
    getCookie(name) {
      const value = `; ${document.cookie}`; // gets the cookie 
      const parts = value.split(`; ${name}=`); // splits the cookie
      if (parts.length === 2) return parts.pop().split(';').shift(); // returns the filename 
    }
  }
}
</script>
