import Keycloak from 'keycloak-js';

const keycloak = new Keycloak({
  url: 'https://keycloak.ltu-m7011e-YOUR-NAME.se',  // Change to your Keycloak URL
  realm: 'myapp',
  clientId: 'my-frontend-app'
});

export default keycloak;
