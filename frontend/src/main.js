import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import VueClickAway from 'vue3-click-away'

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(VueClickAway)

app.mount('#app')
