from project import create_app
import ssl

app = create_app()

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('myCA.pem')
    context.load_cert_chain('server.crt', 'server.key')
    app.run(host='0.0.0.0', port=5000,ssl_context=context, debug=True)

    # app.run(host='0.0.0.0', port=5000, debug=True)