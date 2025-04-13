import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// Import Font Awesome
import { library } from '@fortawesome/fontawesome-svg-core';
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome";
import { faStore, faPhone, faEnvelope } from '@fortawesome/free-solid-svg-icons';
import { faSquareFacebook, faInstagram } from '@fortawesome/free-brands-svg-icons';

// Import các icon cần dùng
import { faBell, faCommentDots } from "@fortawesome/free-regular-svg-icons";

library.add(faBell, faCommentDots, faStore, faPhone, faEnvelope, faSquareFacebook, faInstagram);

const app = createApp(App)

app.use(router)

app.mount('#app')

app.component('font-awesome-icon', FontAwesomeIcon);
