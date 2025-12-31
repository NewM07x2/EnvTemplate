import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { urqlClient } from './lib/graphql/urqlClient'
import urql from '@urql/vue'
import App from './App.vue'
import router from './router'
import './styles/main.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(urql, urqlClient)

app.mount('#app')
