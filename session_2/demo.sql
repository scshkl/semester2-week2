SELECT c.customer_id, oi.product_id FROM customers c
JOIN orders od ON c.customer_id=od.customer_id
JOIN order_items oi ON od.order_id=oi.order_id
WHERE c.customer_id=14;   --- produced product_id 46,38,20
---always check
select order_id from orders where customer_id=14;  --produce 65
select product_id from order_items where order_id=65;  --produce 46, 38, 20

--subquery
SELECT name FROM products WHERE product_id IN (
SELECT oi.product_id FROM customers c
JOIN orders od ON c.customer_id=od.customer_id
JOIN order_items oi ON od.order_id=oi.order_id
WHERE c.customer_id=14
);

---you can use results from one select in another select