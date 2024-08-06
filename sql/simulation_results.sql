DROP TABLE IF EXISTS simulation_results;
CREATE TABLE simulation_results (
    item_id smallint UNSIGNED NOT NULL,
    recipe_id mediumint UNSIGNED NOT NULL,
    crafter_tier tinyint UNSIGNED NOT NULL,
    beastmen_regions JSON,
    conquest_ranking JSON, 
    enabled_guilds JSON,
    from_scratch tinyint UNSIGNED NOT NULL,
    synth_cost float UNSIGNED NOT NULL,
    simulation_cost float UNSIGNED NOT NULL,
    quantity int UNSIGNED NOT NULL,
    last_updated timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (item_id, recipe_id, crafter_tier, beastmen_regions(255), conquest_ranking(255), enabled_guilds(255), from_scratch)
);