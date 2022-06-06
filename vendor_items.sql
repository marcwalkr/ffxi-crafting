DROP TABLE IF EXISTS `vendor_items`;
CREATE TABLE `vendor_items` (
	`itemid` smallint(5) UNSIGNED NOT NULL,
    `npcid` int(10) UNSIGNED NOT NULL,
    `price` int(10) UNSIGNED NOT NULL,
    PRIMARY KEY (`itemid`, `npcid`)
);
