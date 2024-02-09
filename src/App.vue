<template>
  <div id="app" class="container">
    <h1 class="title">Accurate Heat Sheets App</h1>
    
    <section class="upload-section">
      <file-upload></file-upload>
    </section>
    
    <section class="download-section">
      <file-download></file-download>
    </section>
  </div>
</template>

<script>


import FileUpload from "./components/FileUpload.vue";
import FileDownload from "./components/FileDownload.vue";

export default {
  name: 'App',
  components: {
    FileUpload,
    FileDownload,
  },
  data()
  {
    return {
    };
  },
};

</script>

<style>
@import 'styles.css'; 
.container {
  text-align: center;
  font-family: 'Open Sans', sans-serif;
  color: #333;
}

.title {
  color: #000;
  margin-bottom: 30px;
}

.upload-section, .download-section {
  margin: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

button {
  background-color: #ffd700; /* gold */
  color: #000; /* black */
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  text-transform: uppercase;
  margin-top: 10px;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #fada5e; /* lighter gold */
}

input[type="file"] {
  border: 1px solid #ddd;
  padding: 5px;
  margin-top: 10px;
}
</style>
