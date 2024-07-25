DROP TABLE IF EXISTS calculated_item_costs;
CREATE TABLE calculated_item_costs (
    item_id smallint UNSIGNED NOT NULL,
    recipe_id mediumint UNSIGNED NOT NULL,
    cost_per_unit int UNSIGNED NOT NULL,
    craft_skills JSON,
    beastmen_controlled_regions JSON,
    enabled_guilds JSON,
    auction_data_hash VARCHAR(32),
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (item_id, recipe_id, craft_skills(255), beastmen_controlled_regions(255), enabled_guilds(255), auction_data_hash)
);