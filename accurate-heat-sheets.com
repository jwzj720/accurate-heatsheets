# nginx.conf
# HTTP - redirect all requests to HTTPS
server {
    listen 80;
    server_name accurate-heat-sheets.com;  # Ensure this matches your domain

    location / {
        return 301 https://$host$request_uri;  # Redirect to HTTPS
    }
}

# HTTPS
server {
    listen 443 ssl;
    server_name accurate-heat-sheets.com;  # Ensure this matches your domain

    ssl_certificate ssl_cert.pem;  # Path to your SSL certificate
    ssl_certificate_key ssl_private.key;  # Path to your SSL private key

    location / {
        # Serve files for the Vue.js application
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;

        # Specify MIME type
        types {
            text/html               html htm shtml;
            text/css                css;
            image/gif               gif;
            image/jpeg              jpeg jpg;
            application/javascript  js;
        }
        
        # Specifies what to return for requests for non-existent files or directories
        error_page 404 /index.html;
    }
}
