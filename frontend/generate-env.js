const fs = require('fs');
const dotenv = require('dotenv');

// Charger le fichier .env
const envConfig = dotenv.config().parsed || {};

// Créer le contenu du fichier environment.ts
const environmentFileContent = `// Ce fichier est généré automatiquement depuis .env
// Ne pas modifier manuellement
export const environment = {
  production: false,
  apiUrl: '${envConfig.VITE_API_URL || 'http://localhost:8000'}'
};
`;

// Créer le contenu du fichier environment.prod.ts
const environmentProdFileContent = `// Ce fichier est généré automatiquement depuis .env
// Ne pas modifier manuellement
export const environment = {
  production: true,
  apiUrl: '${envConfig.VITE_API_URL || 'http://localhost:8000'}'
};
`;

// Écrire les fichiers
fs.writeFileSync('./src/environments/environment.ts', environmentFileContent);
fs.writeFileSync('./src/environments/environment.prod.ts', environmentProdFileContent);

console.log('✅ Fichiers d\'environnement générés avec succès!');
console.log(`   API URL: ${envConfig.VITE_API_URL || 'http://localhost:8000'}`);
