# Dockerfile (frontend)
# Используем image node 14.x
FROM node:14-alpine AS build

# Устанавливаем рабочий каталог
WORKDIR /app

# Копируем package.json и устанавливаем зависимости
COPY package.json package-lock.json ./
RUN npm install

# Копируем остальной исходный код
COPY . .

# Запускаем сборку проекта
RUN npm run build

# Используем nginx для сервировки статики
FROM nginx:alpine
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
