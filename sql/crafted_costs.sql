DROP TABLE IF EXISTS crafted_costs;
CREATE TABLE crafted_costs (
    item_id smallint UNSIGNED NOT NULL,
    recipe_id mediumint UNSIGNED NOT NULL,
    cost_per_unit int UNSIGNED NOT NULL,
    crafter_tier tinyint UNSIGNED NOT NULL,
    beastmen_controlled_regions JSON,
    enabled_guilds JSON,
    ingredient_costs JSON,
    PRIMARY KEY (item_id, recipe_id, crafter_tier, beastmen_controlled_regions(255), enabled_guilds(255))
);