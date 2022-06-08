-----------------------------------
-- Area: Upper Jeuno
--  NPC: Antonia
-- Standard Merchant NPC
-----------------------------------
local ID = require("scripts/zones/Upper_Jeuno/IDs")
require("scripts/globals/shop")

function onTrade(player, npc, trade)
end

function onTrigger(player, npc)
    local stock =
    {
        17061, 6256, -- mythril rod
        17027, 11232, -- oak cudgel
        17036, 18048, -- mythril mace
        17044, 6033, -- warhammer
        17089, 37440, -- oak pole
        16836, 44550, -- halberd
        16774, 10596, -- scythe
        17320, 7, -- iron arrow
    }

    player:showText(npc, ID.text.ANTONIA_SHOP_DIALOG)
    tpz.shop.general(player, stock, JEUNO)
end

function onEventUpdate(player, csid, option)
end

function onEventFinish(player, csid, option)
end
