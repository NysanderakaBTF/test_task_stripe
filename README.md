API методы с использованием Stripe Session:
* GET /item/{id}: Страница товара с кнопкой "Buy", перенаправляющей на Stripe Checkout.
* GET /buy/{id}: Возвращает Stripe Session ID для оплаты товара.
* GET /order/{id}: Страница заказа с общей стоимостью, скидками и кнопкой "Buy".
* GET /buy_order/{id}: Возвращает Stripe Session ID для оплаты заказа с учетом скидок.

API методы с использованием Stripe Payment Intent:
* GET intent/item/{id}: Страница товара с кнопкой "Buy", перенаправляющей на Stripe Checkout.
* GET intent/buy/{id}: Возвращает Stripe Session ID для оплаты товара.
* GET intent/order/{id}: Страница заказа с общей стоимостью, скидками и кнопкой "Buy".
* GET intent/buy_order/{id}: Возвращает Stripe Session ID для оплаты заказа с учетом скидок.

Требования
* Python 3.10
* Docker для запуска через контейнеры
* Аккаунт Stripe для получения API-ключей

Запуск
1. Получить в аккаунте Stripe API-ключи и добавить их в .env-example файл
2. Переименовать .env-example в .env
3. Запустить с помощью команды docker-compose up --build
4. Приложение будет доступно по http://localhost:8000. Перейти на админ-панель и добавить предметы, заказы и купоны (скидки). Имя пользователя администратора - admin, пароль указывается в .env