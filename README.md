# Create the database if it doesn't exist

```python
python3 init_db.py
```

# Prepare .env file
- Create a file named `.env` in the root directory of the project.
- Add the following environment variables to the file:
    - SECRET_KEY: A random string used for CSRF protection.
    - RECAPTCHA_PUBLIC_KEY: The public key for the Google reCAPTCHA v2.
    - RECAPTCHA_PRIVATE_KEY: The private key for the Google reCAPTCHA v2.

# Set Flask environment variables

```bash
export FLASK_APP=project
export FLASK_DEBUG=1
```

# Run the app without TLS

```bash
flask run -h 0.0.0.0
```

# Become a CA

## Create a private key

```bash
openssl genrsa -des3 -out myCA.key 2048
```

## Create a root certificate

```bash
openssl req -x509 -new -nodes -key myCA.key -sha256 -days 825 -out myCA.pem
```

# Create CA-signed certificates

## Create a private key

```bash
openssl genrsa -out server.key 2048
```

## Create a certificate-signing request

```bash
openssl req -new -key server.key -out server.csr
```

## Create the signed certificate

```bash
openssl x509 -req -in server.csr -CA myCA.pem -CAkey myCA.key -CAcreateserial -out server.crt -days 825 -sha256 -extfile server.ext
```

## Import the CA certificate into the browser

Import the `myCA.pem` file into your browser's certificate store as a trusted root certificate.

# Run the app with TLS

```bash
flask run -h 0.0.0.0 --cert=server.crt --key=server.key
```

# References
- https://stackoverflow.com/questions/7580508/getting-chrome-to-accept-self-signed-localhost-certificate 
- https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login#step-8-testing-the-sign-up-method
- https://www.gitauharrison.com/articles/google-recaptcha-in-flask
- https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https