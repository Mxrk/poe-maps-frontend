import Vue from 'vue';
import VueTour from 'vue-tour';

import App from './App.vue';

require('vue-tour/dist/vue-tour.css');

Vue.config.productionTip = false;
Vue.use(VueTour);

new Vue({
  render: (h) => h(App),
}).$mount('#app');
