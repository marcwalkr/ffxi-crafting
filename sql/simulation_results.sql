DROP TABLE IF EXISTS simulation_results;
CREATE TABLE simulation_results (
    item_id smallint UNSIGNED NOT NULL,
    recipe_id mediumint UNSIGNED NOT NULL,
    crafter_tier tinyint UNSIGNED NOT NULL,
    min_cost_used boolean NOT NULL,
    synth_cost float UNSIGNED NOT NULL,
    simulation_cost float UNSIGNED NOT NULL,
    leftover_cost float UNSIGNED NOT NULL,
    quantity int UNSIGNED NOT NULL,
    cost_per_unit float UNSIGNED NOT NULL,
    last_updated timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (item_id, recipe_id, crafter_tier, min_cost_used)
);