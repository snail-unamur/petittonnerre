# Frontend Dockerfile
FROM node:20-alpine

WORKDIR /app

# Copier package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le code source
COPY . .

# Exposer le port
EXPOSE 4200

# Générer la config depuis .env et lancer
CMD ["sh", "-c", "npm run config && npm start -- --host 0.0.0.0 --poll 2000"]
