DROP TABLE IF EXISTS auction_items;
CREATE TABLE auction_items (
    itemid smallint UNSIGNED PRIMARY KEY,
    single_price int UNSIGNED NOT NULL,
    stack_price int UNSIGNED NOT NULL
);
