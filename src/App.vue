<template>
  <div id="app">
    <h1>Upload</h1>
    <file-upload></file-upload>
    <h1>Download</h1>
    <file-download></file-download>
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
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
