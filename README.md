To Run:
1. `git clone https://github.com/Mahasvin24/LaunchLink.git`
2. `cd LaunchLink`
3. Create an environment `python -m venv venv`
4. Activate environment (for mac) `source venv/bin/activate`
5. Install Requirements `pip install -r requirements.txt`
6. Go to settings and remove the line `DEFAULT_FILE_STORAGE = 'LaunchLink.storage.VercelFileSystemStorage'`
7. In settings, replace
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_NAME'),
        'USER': os.getenv('POSTGRES_USER'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'HOST': os.getenv('POSTGRES_HOST'),
        'PORT': os.getenv('PGPORT'),
    }
}
```
with
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
8. Run `sh run.sh`

Images work here, on vercel it doesn't. So locally works best.




