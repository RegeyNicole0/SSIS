from os import getenv

SECRET_KEY = getenv("SECRET_KEY")
DB_NAME = getenv("DB_NAME")
DB_USERNAME = getenv("DB_USERNAME")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_HOST = getenv("DB_HOST")
DB_PORT = getenv("DB_PORT")
BOOTSTRAP_SERVE_LOCAL = getenv("BOOTSTRAP_SERVE_LOCAL")
CLOUDINARY_API_KEY=getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET=getenv("CLOUDINARY_API_SECRET")
CLOUDINARY_API_CLOUD=getenv("CLOUDINARY_API_CLOUD")
CLOUDINARY_API_CLOUD_FOLDER=getenv("CLOUDINARY_API_CLOUD_FOLDER")