FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install --production
COPY ./scripts/docker_entrypoint.sh ./scripts/docker_entrypoint.sh
RUN chmod +x ./scripts/docker_entrypoint.sh
COPY . ./
RUN mkdir -p /app/database
EXPOSE 3000
ENV PORT=3000
CMD ["/bin/bash", "./scripts/docker_entrypoint.sh"]
