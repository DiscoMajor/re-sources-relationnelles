# Utilise une image de base Python
FROM python:3.9

# Crée un répertoire de travail
WORKDIR /app

# Copie les fichiers requirements.txt et installe les dépendances Python
COPY requirements.txt .
RUN pip install -r requirements.txt

# Installer Node.js et npm
RUN apt-get update && apt-get install -y nodejs npm

# Installe Tailwind CSS et ses dépendances
RUN npm install -D tailwindcss@3 postcss autoprefixer

# Copie le reste des fichiers de l'application
COPY . .

# S'assurer que le dossier static/css existe
RUN mkdir -p static/css && touch static/css/styles.css

# Exécute la commande de build de Tailwind CSS
RUN npx tailwindcss -i ./static/css/styles.css -o ./static/css/output.css

# Expose le port de l'application
EXPOSE 8000

# Commande pour démarrer l'application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
