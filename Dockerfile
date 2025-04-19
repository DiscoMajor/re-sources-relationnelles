# Utilise une image de base Python
FROM python:3.11

# Crée un répertoire de travail
WORKDIR /app

# Copie les fichiers requirements.txt et installe les dépendances Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Installer Node.js et npm
RUN apt-get update && apt-get install -y nodejs npm

# Installe Tailwind CSS et ses dépendances
RUN npm install -D tailwindcss@latest postcss autoprefixer leaflet @hotwired/stimulus

# Copie le reste des fichiers de l'application
COPY . .

# Expose le port de l'application
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
