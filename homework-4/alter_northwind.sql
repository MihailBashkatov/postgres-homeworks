-- Подключиться к БД Northwind и сделать следующие изменения:
-- 1. Добавить ограничение на поле unit_price таблицы products (цена должна быть больше 0)
ALTER TABLE products ADD CONSTRAINT chk_products_unit_price CHECK (unit_price > 0)


-- 2. Добавить ограничение, что поле discontinued таблицы products может содержать только значения 0 или 1
ALTER TABLE products ADD CONSTRAINT chk_products_discontinued CHECK (discontinued IN (0, 1))


-- 3. Создать новую таблицу, содержащую все продукты, снятые с продажи (discontinued = 1)
SELECT * INTO dropped_products FROM products WHERE discontinued = 1


-- 4. Удалить из products товары, снятые с продажи (discontinued = 1)
-- Для 4-го пункта может потребоваться удаление ограничения, связанного с foreign_key. Подумайте, как это можно решить, чтобы связь с таблицей order_details все же осталась.

-- 4. Удалить из products товары, снятые с продажи (discontinued = 1)
-- Для 4-го пункта может потребоваться удаление ограничения, связанного с foreign_key.
-- Подумайте, как это можно решить, чтобы связь с таблицей order_details все же осталась.


ALTER TABLE order_details DROP CONSTRAINT fk_order_details_products; -- Delete foreign  key from the table order_details
ALTER TABLE  products DROP CONSTRAINT pk_products; -- Delete primary  key from the table products
ALTER TABLE  order_details DROP CONSTRAINT pk_order_details; -- Delete primary  key from the table order_details
UPDATE products SET product_id = 100 WHERE  discontinued = 1; -- Set value 100 for product_id, discontinued = 1, table products
UPDATE order_details SET product_id = 100 WHERE EXISTS (SELECT * FROM products -- Set value 100 for product_id in the table order_details, which have value 100 in the table products
														WHERE products.product_id = 100);
DELETE FROM products WHERE product_id = 100; -- Delete lines, where  value 100 for product_id, table products
DELETE FROM order_details WHERE product_id = 100; -- Delete lines, where  value 100 for product_id, table order_details
ALTER TABLE products ADD CONSTRAINT pk_products PRIMARY KEY (product_id); -- Set primary key (product_id) for the table products
ALTER TABLE order_details ADD CONSTRAINT pk_order_details PRIMARY KEY (order_id);-- Set primary key (order_id) for the table order_details
ALTER TABLE order_details ADD CONSTRAINT fk_order_details_product FOREIGN KEY(product_id) REFERENCES products(product_id)-- Set foreign  key for the table order_details
                                                                                                                         -- refernce to product_id, table products
