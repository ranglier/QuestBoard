FROM node:22-alpine

WORKDIR /app

COPY package.json ./

# Build-time only : secret CA optionnel pour npm derriere un proxy d'entreprise
# qui intercepte TLS. Non persiste dans l'image. Sans secret, build registre npm
# public normal. Activation locale : voir compose.override.example.yaml.
RUN --mount=type=secret,id=proxy_ca \
    if [ -s /run/secrets/proxy_ca ]; then export NODE_EXTRA_CA_CERTS=/run/secrets/proxy_ca; fi; \
    npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
