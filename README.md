# Python CV
Code base for more experimental computer vision & image processing implementations in Python.

## OCR Project name: Shibumi
- Project setup was in Google Cloud Platform
- `systemd` file was stored in /scripts folder for future references.
- Frontend UI was in [frontend-monorepo][https://gitlab.com/nixel/frontend-monorepo] repo, folder `packages/carton-printing`
- Frontend UI was built in next.js
- GCP setups & folder structure
```
Services    
- python
- miniconda
- flask (to serve python API in localhost:5000)
- nginx (to serve frontend app and API)
```

```
Folder structure
/var/www/shibumi
                 - python-cv/ (this repo)
                 - app (frontend-monorepo repo)     
```


[https://gitlab.com/nixel/frontend-monorepo]: git@gitlab.com:nixel/frontend-monorepo.git