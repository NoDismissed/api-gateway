# API Gateway

Servidor para un sistema de microservicios (orquestador)

- expone HTTP/REST al exterior
- valida request, json, parametros
- traduce HTTP -> gRPC y gRPC -> HTTP
- manejar codigos de error
- auth, rate-limit, logging

- el gateway se testea aislado del dominio
- si tienes layout /app, asegurarse que la raiz del proyecto este en pythonpath
- se usa el mismo proto de los microservicios
- import relativo en pb2_grpc al usar app (paquete)
- opcion 1, correr repo user-service en docker exponiendo el puerto y correr api gateway en local con flask
- middleware JWT (proteccion de rutas)
- @wraps, decorador que mantiene identidad del metodo
- el gateway reenvia claims normalizados
- el sub en el jwt token debe ser string
- el requester va en g, almacena temporalmente datos durante un unico request

- flask --app app.app run
- python -m grpc_tools.protoc \
  -I app/proto \
  --python_out=app \
  --grpc_python_out=app \
  app/proto/*.proto
  (crea stubs en carpeta destino)
- curl -i -X POST http://localhost:5000/users/2/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "is_active": false,
    "role": "user"
  }'
  (actualizar usuario)
- curl -i -X POST http://localhost:5000/users \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser@example.com",
    "password_hash": "user_secret",
    "role": "user"
  }'
  (crear usuario)
- curl -i http://localhost:5000/users/1 \
  -H "Authorization: Bearer $TOKEN"
  (obtener usuario)
- curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"gateway@test.com","password":"hash"}'
  (login)
- curl -X POST http://localhost:5000/orders \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"total_amount": 123.45}'
  (crear orden)
- 