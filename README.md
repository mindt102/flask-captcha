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

# Run the app without TLS

## Change run.py
    
```python
    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.verify_mode = ssl.CERT_REQUIRED
    # context.load_verify_locations('myCA.pem')
    # context.load_cert_chain('server.crt', 'server.key')
    # app.run(host='0.0.0.0', port=5000,ssl_context=context, debug=True)

    app.run(host='0.0.0.0', port=5000, debug=True)
```

## Run the app

```bash
python3 run.py
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

# Create CA-signed certificates for the server

## Create a private key for the server

```bash
openssl genrsa -out server.key 2048
```

## Create a certificate-signing request for the server

```bash
openssl req -new -key server.key -out server.csr
```

## Create the signed certificate for the server

```bash
openssl x509 -req -in server.csr -CA myCA.pem -CAkey myCA.key -CAcreateserial -out server.crt -days 825 -sha256 -extfile server.ext
```

## Import the CA certificate into the browser

Import the `myCA.pem` file into your browser's certificate store as a trusted root certificate.

# Create CA-signed certificates for the client

Follow the same steps as above

# Import the client certificate into the browser
## Convert the client certificate to PKCS12 format

```bash
openssl pkcs12 -export -out pkcs12.p12 -inkey client.key -in client.crt
```
## Import into the browser

Import the `pkcs12.p12` file into your browser's certificate store.

# Run the app with mutual TLS

## Change run.py

```
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('myCA.pem')
    context.load_cert_chain('server.crt', 'server.key')
    app.run(host='0.0.0.0', port=5000,ssl_context=context, debug=True)

    # app.run(host='0.0.0.0', port=5000, debug=True)
```

## Run the app

```bash
python3 run.py
```

# References
- https://stackoverflow.com/questions/7580508/getting-chrome-to-accept-self-signed-localhost-certificate 
- https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login#step-8-testing-the-sign-up-method
- https://www.gitauharrison.com/articles/google-recaptcha-in-flask
- https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
- https://github.com/mr-satan1/mTLS-Flask-Template/blob/main/minimal-flask-dev.py
- https://velmuruganv.wordpress.com/2020/04/27/mtls-mutual-tls-authentication-chrome/