DROP TABLE IF EXISTS auction;
CREATE TABLE auction (
	itemid smallint(5) UNSIGNED PRIMARY KEY,
    single_sales smallint(5) UNSIGNED,
    single_price_sum int(10) UNSIGNED,
    stack_sales smallint(5) UNSIGNED,
    stack_price_sum int(10) UNSIGNED,
    days smallint(5) UNSIGNED,
    last_updated timestamp DEFAULT current_timestamp ON UPDATE current_timestamp
);