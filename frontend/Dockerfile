FROM node:lts-alpine

ARG FOLDER=/frontend

Run mkdir -p $FOLDER

COPY . /frontend/.

WORKDIR $FOLDER

RUN npm install

EXPOSE 3000

RUN npm run build

CMD ["npm", "start"]
