DROP TABLE IF EXISTS `auction`;
CREATE TABLE `auction` (
	`itemid` smallint(5) UNSIGNED PRIMARY KEY,
    `single_price` int(10) UNSIGNED,
    `stack_price` int(10) UNSIGNED,
    `single_frequency` float(5,3) UNSIGNED,
    `stack_frequency` float(5,3) UNSIGNED
);