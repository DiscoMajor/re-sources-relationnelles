# Utilise une image de base Python
FROM python:3.11

# Crée un répertoire de travail
WORKDIR /app

# Installer les dépendances système pour PostgreSQL et Node.js
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    nodejs \
    npm

# Copie les fichiers requirements.txt et installe les dépendances Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copie package.json et package-lock.json (si dispo)
COPY package*.json ./

# Installe les dépendances Node.js, y compris les outils de build (leaflet, tailwindcss, stimulus)
RUN npm install -D tailwindcss@latest postcss autoprefixer leaflet @hotwired/stimulus \
    webpack webpack-cli babel-loader @babel/core @babel/preset-env

# Copie le reste des fichiers de l'application
COPY . .

# Build du bundle JavaScript
RUN npm run build

# Expose le port de l'application
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]