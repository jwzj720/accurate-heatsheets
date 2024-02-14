<template>
  <div id="app" class="container">
    <h1 class="title">Accurate Heat Sheets</h1>
    
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
  }
};
</script>

<style>

/* General styles */
body, html {
  font-family: 'Roboto', sans-serif;
  background-color: #f4f4f4;
  color: #333;
}

#app {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

/* Header styles */
.header {
  background-color: #000;
  color: #ffd700;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

/* Content styles */
.content {
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

/* Button styles */
button {
  background-color: #ffd700; /* Gold color */
  color: #000; /* Black color */
  border: none;
  padding: 10px 15px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #e6c300;
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
}

/* Input file styles */
input[type="file"] {
  border: 1px solid #ddd;
  padding: 10px;
  margin-top: 10px;
  border-radius: 4px;
}
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
