DROP TABLE IF EXISTS auction_pages;
CREATE TABLE auction_pages (
	itemid smallint(5) UNSIGNED NOT NULL,
    single_sales tinyint(2) UNSIGNED NOT NULL,
    single_price_sum int(10) UNSIGNED NOT NULL,
    stack_sales tinyint(2) UNSIGNED NOT NULL,
    stack_price_sum int(10) UNSIGNED NOT NULL,
    num_days smallint(5) UNSIGNED NOT NULL,
    accessed timestamp NOT NULL
);