FROM node:18.16-alpine3.18 AS Build

WORKDIR /app

COPY . .

RUN npm i -g pnpm

RUN pnpm i --frozen-lockfile

RUN pnpm build

RUN pnpm prune --prod

FROM node:18.16-alpine3.18 AS Production

WORKDIR /app

COPY --from=Build --chown=node:node /app/node_modules ./node_modules
COPY --from=Build --chown=node:node /app/apps/earthquake/node_modules ./apps/earthquake/node_modules
COPY --from=Build --chown=node:node /app/apps/earthquake/dist ./apps/earthquake//dist

WORKDIR /app/apps/earthquake

USER node

ENV NODE_ENV production

EXPOSE 3000

CMD ["node", "dist/main.js"]
