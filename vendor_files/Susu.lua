-----------------------------------
-- Area: Lower Jeuno
--  NPC: Susu
-- Standard Merchant NPC
-----------------------------------
local ID = require("scripts/zones/Lower_Jeuno/IDs")
require("scripts/globals/shop")

function onTrade(player, npc, trade)
end

function onTrigger(player, npc)
    local stock =
    {
        4647,20000,--banishga ii
        4683,2030,--barblind
        4697,2030,--barblindra
        4682,780,--barparalyze
        4696,780,--barparalyzra
        4681,400,--barpoison
        4695,400,--barpoisonra
        4684,4608,--barsilence
        4698,4608,--barsilencera
        4680,244,--barsleep
        4694,244,--barsleepra
        4628,8586,--cursna
        4629,35000,--holy
        4625,2330,--silena
        4626,19200,--stona
        4627,13300,--viruna
    }

    player:showText(npc, ID.text.SUSU_SHOP_DIALOG)
    tpz.shop.general(player, stock, JEUNO)
end

function onEventUpdate(player, csid, option)
end

function onEventFinish(player, csid, option)
end
