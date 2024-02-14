import { createApp } from 'vue'
import App from './App.vue'
import WoopraPlugin from './plugins/woopra';


const app = createApp(App);

app.use(WoopraPlugin, {
    domain: "accurate-heat-sheets.com"
});

app.mount('#app');


