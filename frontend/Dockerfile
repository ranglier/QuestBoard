FROM node:22-alpine

WORKDIR /app

# Autorités racine locales (proxy d'entreprise qui intercepte TLS). Le dossier
# certs/ existe toujours (.gitkeep) ; les .crt sont fournis par machine et NON
# versionnés. S'ils sont absents, cette étape est neutre (registre npm direct).
COPY certs/ /certs/

COPY package.json ./
RUN if ls /certs/*.crt >/dev/null 2>&1; then \
        export NODE_EXTRA_CA_CERTS=/certs/host-roots.crt; \
    fi; \
    npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
