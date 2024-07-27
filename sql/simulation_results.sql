DROP TABLE IF EXISTS simulation_results;
CREATE TABLE simulation_results (
    item_id smallint UNSIGNED NOT NULL,
    recipe_id mediumint UNSIGNED NOT NULL,
    simulation_trials int UNSIGNED NOT NULL,
    crafter_tier tinyint UNSIGNED NOT NULL,
    beastmen_regions JSON,
    enabled_guilds JSON,
    synth_cost int UNSIGNED NOT NULL,
    simulation_cost int UNSIGNED NOT NULL,
    quantity int UNSIGNED NOT NULL,
    from_scratch tinyint UNSIGNED NOT NULL,
    last_updated timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (item_id, recipe_id, simulation_trials, crafter_tier, beastmen_regions(255), enabled_guilds(255))
);