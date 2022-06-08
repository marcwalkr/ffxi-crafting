DROP TABLE IF EXISTS item_costs;
CREATE TABLE item_costs (
	itemid smallint(5) UNSIGNED PRIMARY KEY,
    sourceid int(10) UNSIGNED,
    cost int(10) UNSIGNED,
    last_updated timestamp DEFAULT current_timestamp ON UPDATE current_timestamp
);