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
      axios.get('http://127.0.0.1:8081/download', { responseType: 'blob' })
        .then(response => {
          const blob = new Blob([response.data], { type: 'application/pdf' }); 
          const link = document.createElement('a'); // creates a new HTML anchor element - creates a trigger for the filedownload
          link.href = URL.createObjectURL(blob);
          link.download = 'downloaded.pdf'; //TODO: change this to the name of the file downloaded
          link.click();
          URL.revokeObjectURL(link.href);
        })
        .catch(console.error);
    }
  }
}
</script>
