DROP TABLE IF EXISTS auction_items;
CREATE TABLE auction_items (
    itemid smallint UNSIGNED PRIMARY KEY,
    avg_single_price float,
    avg_stack_price float,
    sales_frequency float,
    last_updated timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
