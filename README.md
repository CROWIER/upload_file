# Инструкция по запуску

1. Клонировать проект git clone
2. cp .env.example .env и Затем отредактируйте .env, указав актуальные значения
3. собрать и запустить контейнер docker-compose up --build
4. выполнить миграции docker-compose exec api alembic upgrade head
После этого сервис будет доступен по адресу:
📍 http://localhost:8000
Документация Swagger:
📘 http://localhost:8000/docs


# Документация API: Эндпоинт загрузки файла

## Эндпоинт: `POST /api/files/`

Эндпоинт позволяет загрузить файл (поддерживаемые форматы: `.pdf`, `.jpg`, `.jpeg`, `.png`, `.dcm`). Требуется авторизация через JWT-токен.

### 1. Успешная загрузка файла
**Описание**: Загружает файл с поддерживаемым расширением (например, `.png`) и возвращает метаданные файла.

**cURL-запрос**:
```bash
curl -X 'POST' \
  'http://localhost:8000/api/files/' \
  -H 'Authorization: Bearer <your_token>' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@test.png;type=image/png'
```

Ожидаемый ответ:

Код статуса: 200 OK
Тело (JSON):
```{
  "id": "08a5df20-da8c-4f05-ae3e-0b6e728acac7",
  "url": "http://minio:9000/files/32a60c33579a5f023db658a2a23da5fbebf6
  03cb10acd0dbdf1d47e7e1a15d74/Askar%20Bulabayev%20pbd.pdf?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=minioadmin%2F20250511%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250511T110356Z&X-Amz-Expires=1800&X-Amz-SignedHeaders=host&X-Amz-Signature=07592528e27979cb543d8e12af3c150a566f592f236b9c6defae7b5d57bfbb09"
}
```
2. Загрузка файла с неподдерживаемым расширением
Описание: Пытается загрузить файл с неподдерживаемым расширением (например, .txt), возвращает ошибку.

cURL-запрос:
```
curl -X 'POST' \
  'http://localhost:8000/api/files/' \
  -H 'Authorization: Bearer <your_token>' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@test.txt;type=text/plain'
```
Ожидаемый ответ:

Код статуса: 400 Bad Request
Тело (JSON):
```aiignore
{
  "detail": "Error uploading file: 400: Unsupported file extension"
}
```

3. Внутренняя ошибка сервера
Код статуса: 500 Internal Server Error
```aiignore
{
  "detail": "Error uploading file: HTTPConnectionPool(host='minio', port=9000): Max retries exceeded with url: /files?location= (Caused by NameResolutionError(\"<urllib3.connection.HTTPConnection object at 0xffffb2ced910>: Failed to resolve 'minio' ([Errno -2] Name or service not known)\"))"
}
```
Получение токена авторизации
Для получения JWT-токена используйте эндпоинт авторизации:

cURL-запрос:
```
curl -X 'POST' \
  'http://localhost:8000/api/auth/token' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'grant_type=password&username=string&password=string&scope=&client_id=string&client_secret=string'```
```
Код статуса: 200 OK
```aiignore
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE3NDY5NjM0ODJ9.rpMIV7m5Rzl_k5cqml9RkHberPbYBwKhZVptn7C7UmQ",
  "token_type": "bearer"
}
```