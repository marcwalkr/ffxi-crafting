DROP TABLE IF EXISTS vendor_items;
CREATE TABLE vendor_items (
	itemid smallint UNSIGNED NOT NULL,
    npcid int UNSIGNED NOT NULL,
    price int UNSIGNED NOT NULL,
    sandoria_rank tinyint UNSIGNED DEFAULT 0,
    bastok_rank tinyint UNSIGNED DEFAULT 0,
    windurst_rank tinyint UNSIGNED DEFAULT 0,
    sandoria_citizen tinyint UNSIGNED DEFAULT 0,
    bastok_citizen tinyint UNSIGNED DEFAULT 0,
    windurst_citizen tinyint UNSIGNED DEFAULT 0,
    PRIMARY KEY (itemid, npcid)
);

-- Adelflete
INSERT INTO vendor_items VALUES (806,17780861,1863,0,0,0,0,0,0);	-- Tourmaline
INSERT INTO vendor_items VALUES (807,17780861,1863,0,0,0,0,0,0);	-- Sardonyx
INSERT INTO vendor_items VALUES (800,17780861,1863,0,0,0,0,0,0);	-- Amethyst
INSERT INTO vendor_items VALUES (814,17780861,1863,0,0,0,0,0,0);	-- Amber
INSERT INTO vendor_items VALUES (795,17780861,1863,0,0,0,0,0,0);	-- Lapis Lazuli
INSERT INTO vendor_items VALUES (809,17780861,1863,0,0,0,0,0,0);	-- Clear Topaz
INSERT INTO vendor_items VALUES (799,17780861,1863,0,0,0,0,0,0);	-- Onyx
INSERT INTO vendor_items VALUES (796,17780861,1863,0,0,0,0,0,0);	-- Light Opal
INSERT INTO vendor_items VALUES (13327,17780861,1250,0,0,0,0,0,0);	-- Silver Earring
INSERT INTO vendor_items VALUES (13456,17780861,1250,0,0,0,0,0,0);	-- Silver Ring

-- Ahyeekih
INSERT INTO vendor_items VALUES (4503,17752103,184,0,0,0,0,0,0);	-- Buburimu Grape
INSERT INTO vendor_items VALUES (1120,17752103,1620,0,0,0,0,0,0);	-- Casablanca
INSERT INTO vendor_items VALUES (4359,17752103,220,0,0,0,0,0,0);	-- Dhalmel Meat
INSERT INTO vendor_items VALUES (614,17752103,72,0,0,0,0,0,0);	-- Mhaura Garlic
INSERT INTO vendor_items VALUES (4445,17752103,40,0,0,0,0,0,0);	-- Yagudo Cherry

-- Albinie
INSERT INTO vendor_items VALUES (699,17727514,5688,1,0,0,1,0,0);	-- Oak Log
INSERT INTO vendor_items VALUES (644,17727514,1800,1,0,0,1,0,0);	-- Mythril Ore
INSERT INTO vendor_items VALUES (835,17727514,225,1,0,0,1,0,0);	-- Flax Flower
INSERT INTO vendor_items VALUES (694,17727514,2543,2,0,0,0,0,0);	-- Chestnut Log
INSERT INTO vendor_items VALUES (640,17727514,10,2,0,0,0,0,0);	-- Copper Ore
INSERT INTO vendor_items VALUES (643,17727514,810,2,0,0,0,0,0);	-- Iron Ore
INSERT INTO vendor_items VALUES (833,17727514,18,2,0,0,0,0,0);	-- Moko Grass
INSERT INTO vendor_items VALUES (4570,17727514,50,2,0,0,0,0,0);	-- Bird Egg
INSERT INTO vendor_items VALUES (698,17727514,86,0,0,0,0,0,0);	-- Ash Log
INSERT INTO vendor_items VALUES (1,17727514,1800,0,0,0,0,0,0);	-- Chocobo Bedding

-- Alizabe
INSERT INTO vendor_items VALUES (1523,17760320,290,0,0,0,0,0,0);	-- Apple Mint
INSERT INTO vendor_items VALUES (5164,17760320,1945,0,0,0,0,0,0);	-- Ground Wasabi
INSERT INTO vendor_items VALUES (17005,17760320,99,0,0,0,0,0,0);	-- Lufaise Fly
INSERT INTO vendor_items VALUES (5195,17760320,233,0,0,0,0,0,0);	-- Misareaux Parsley
INSERT INTO vendor_items VALUES (1695,17760320,920,0,0,0,0,0,0);	-- Habanero Peppers

-- Allard
INSERT INTO vendor_items VALUES (12466,16974278,20000,0,0,0,0,0,0);	-- Red Cap
INSERT INTO vendor_items VALUES (12594,16974278,32500,0,0,0,0,0,0);	-- Gambison
INSERT INTO vendor_items VALUES (12722,16974278,16900,0,0,0,0,0,0);	-- Bracers
INSERT INTO vendor_items VALUES (12850,16974278,24500,0,0,0,0,0,0);	-- Hose
INSERT INTO vendor_items VALUES (12978,16974278,16000,0,0,0,0,0,0);	-- Socks

-- Amalasanda
INSERT INTO vendor_items VALUES (704,17780858,144,0,0,0,0,0,0);	-- Bamboo Stick
INSERT INTO vendor_items VALUES (829,17780858,21000,0,0,0,0,0,0);	-- Silk Cloth
INSERT INTO vendor_items VALUES (1240,17780858,220,0,0,0,0,0,0);	-- Koma
INSERT INTO vendor_items VALUES (657,17780858,7000,0,0,0,0,0,0);	-- Tama-Hagane
INSERT INTO vendor_items VALUES (1415,17780858,73530,0,0,0,0,0,0);	-- Urushi
INSERT INTO vendor_items VALUES (1161,17780858,40,0,0,0,0,0,0);	-- Uchitake
INSERT INTO vendor_items VALUES (1164,17780858,40,0,0,0,0,0,0);	-- Tsurara
INSERT INTO vendor_items VALUES (1167,17780858,40,0,0,0,0,0,0);	-- Kawahori-Ogi
INSERT INTO vendor_items VALUES (1170,17780858,40,0,0,0,0,0,0);	-- Makibishi
INSERT INTO vendor_items VALUES (1173,17780858,40,0,0,0,0,0,0);	-- Hiraishin
INSERT INTO vendor_items VALUES (1176,17780858,40,0,0,0,0,0,0);	-- Mizu-Deppo
INSERT INTO vendor_items VALUES (1179,17780858,125,0,0,0,0,0,0);	-- Shihei
INSERT INTO vendor_items VALUES (1182,17780858,125,0,0,0,0,0,0);	-- Jusatsu
INSERT INTO vendor_items VALUES (1185,17780858,125,0,0,0,0,0,0);	-- Kaginawa
INSERT INTO vendor_items VALUES (1188,17780858,125,0,0,0,0,0,0);	-- Sairui-Ran
INSERT INTO vendor_items VALUES (1191,17780858,125,0,0,0,0,0,0);	-- Kodoku
INSERT INTO vendor_items VALUES (1194,17780858,125,0,0,0,0,0,0);	-- Shinobi-Tabi
INSERT INTO vendor_items VALUES (1471,17780858,316,0,0,0,0,0,0);	-- Sticky Rice
INSERT INTO vendor_items VALUES (1554,17780858,645,0,0,0,0,0,0);	-- Turmeric
INSERT INTO vendor_items VALUES (1555,17780858,1585,0,0,0,0,0,0);	-- Coriander
INSERT INTO vendor_items VALUES (1590,17780858,800,0,0,0,0,0,0);	-- Holy Basil
INSERT INTO vendor_items VALUES (1475,17780858,990,0,0,0,0,0,0);	-- Curry Powder
INSERT INTO vendor_items VALUES (5164,17780858,2595,0,0,0,0,0,0);	-- Ground Wasabi
INSERT INTO vendor_items VALUES (1652,17780858,200,0,0,0,0,0,0);	-- Rice Vinegar
INSERT INTO vendor_items VALUES (5237,17780858,492,0,0,0,0,0,0);	-- Shirataki
INSERT INTO vendor_items VALUES (2702,17780858,5000,0,0,0,0,0,0);	-- Buckwheat Flour
INSERT INTO vendor_items VALUES (4928,17780858,2331,0,0,0,0,0,0);	-- Katon: Ichi
INSERT INTO vendor_items VALUES (4931,17780858,2331,0,0,0,0,0,0);	-- Hyoton: Ichi
INSERT INTO vendor_items VALUES (4934,17780858,2331,0,0,0,0,0,0);	-- Huton: Ichi
INSERT INTO vendor_items VALUES (4937,17780858,2331,0,0,0,0,0,0);	-- Doton: Ichi
INSERT INTO vendor_items VALUES (4940,17780858,2331,0,0,0,0,0,0);	-- Raiton: Ichi
INSERT INTO vendor_items VALUES (4943,17780858,2331,0,0,0,0,0,0);	-- Suiton: Ichi
INSERT INTO vendor_items VALUES (4949,17780858,2849,0,0,0,0,0,0);	-- Jubaku: Ichi
INSERT INTO vendor_items VALUES (4952,17780858,2849,0,0,0,0,0,0);	-- Hojo: Ichi
INSERT INTO vendor_items VALUES (4955,17780858,2849,0,0,0,0,0,0);	-- Kurayami: Ichi
INSERT INTO vendor_items VALUES (4958,17780858,2849,0,0,0,0,0,0);	-- Dokumori: Ichi
INSERT INTO vendor_items VALUES (4961,17780858,2849,0,0,0,0,0,0);	-- Tonko: Ichi
INSERT INTO vendor_items VALUES (4964,17780858,9590,0,0,0,0,0,0);	-- Monomi: Ichi
INSERT INTO vendor_items VALUES (4687,17780858,60750,0,0,0,0,0,0);	-- Recall-Jugner
INSERT INTO vendor_items VALUES (4688,17780858,60750,0,0,0,0,0,0);	-- Recall-Pashh
INSERT INTO vendor_items VALUES (4689,17780858,60750,0,0,0,0,0,0);	-- Recall-Meriph
INSERT INTO vendor_items VALUES (4747,17780858,34656,0,0,0,0,0,0);	-- Teleport-Vahzl
INSERT INTO vendor_items VALUES (4728,17780858,34656,0,0,0,0,0,0);	-- Teleport-Yhoat
INSERT INTO vendor_items VALUES (4729,17780858,34656,0,0,0,0,0,0);	-- Teleport-Altep
INSERT INTO vendor_items VALUES (4730,17780858,34656,0,0,0,0,0,0);	-- Teleport-Holla
INSERT INTO vendor_items VALUES (4731,17780858,34656,0,0,0,0,0,0);	-- Teleport-Dem
INSERT INTO vendor_items VALUES (4732,17780858,34656,0,0,0,0,0,0);	-- Teleport-Mea
INSERT INTO vendor_items VALUES (4853,17780858,10428,0,0,0,0,0,0);	-- Drain
INSERT INTO vendor_items VALUES (4855,17780858,12850,0,0,0,0,0,0);	-- Aspir
INSERT INTO vendor_items VALUES (4857,17780858,10428,0,0,0,0,0,0);	-- Blaze Spikes
INSERT INTO vendor_items VALUES (4869,17780858,11953,0,0,0,0,0,0);	-- Warp
INSERT INTO vendor_items VALUES (4870,17780858,37200,0,0,0,0,0,0);	-- Warp II
INSERT INTO vendor_items VALUES (4873,17780858,32320,0,0,0,0,0,0);	-- Retrace
INSERT INTO vendor_items VALUES (4882,17780858,67818,0,0,0,0,0,0);	-- Sleepga II
INSERT INTO vendor_items VALUES (4946,17780858,13133,0,0,0,0,0,0);	-- Utsusemi: Ichi
INSERT INTO vendor_items VALUES (4994,17780858,11830,0,0,0,0,0,0);	-- Mage's Ballad

-- Antonia
INSERT INTO vendor_items VALUES (17061,17776715,6256,0,0,0,0,0,0);	-- Mythril Rod
INSERT INTO vendor_items VALUES (17027,17776715,11232,0,0,0,0,0,0);	-- Oak Cudgel
INSERT INTO vendor_items VALUES (17036,17776715,18048,0,0,0,0,0,0);	-- Mythril Mace
INSERT INTO vendor_items VALUES (17044,17776715,6033,0,0,0,0,0,0);	-- Warhammer
INSERT INTO vendor_items VALUES (17098,17776715,37440,0,0,0,0,0,0);	-- Oak Pole
INSERT INTO vendor_items VALUES (16836,17776715,44550,0,0,0,0,0,0);	-- Halberd
INSERT INTO vendor_items VALUES (16774,17776715,10596,0,0,0,0,0,0);	-- Scythe
INSERT INTO vendor_items VALUES (17320,17776715,7,0,0,0,0,0,0);	-- Iron Arrow

-- Antonian
INSERT INTO vendor_items VALUES (631,17723492,36,0,0,0,0,0,0);	-- Horo Flour
INSERT INTO vendor_items VALUES (629,17723492,43,0,0,0,0,0,0);	-- Millioncorn
INSERT INTO vendor_items VALUES (4415,17723492,111,0,0,0,0,0,0);	-- Roasted Corn
INSERT INTO vendor_items VALUES (841,17723492,36,0,0,0,0,0,0);	-- Yagudo Feather
INSERT INTO vendor_items VALUES (4505,17723492,90,0,0,0,0,0,0);	-- Sunflower Seeds

-- Apairemant
INSERT INTO vendor_items VALUES (1108,17719306,703,0,0,0,0,0,0);	-- Sulfur
INSERT INTO vendor_items VALUES (619,17719306,43,0,0,0,0,0,0);	-- Popoto
INSERT INTO vendor_items VALUES (611,17719306,36,0,0,0,0,0,0);	-- Rye Flour
INSERT INTO vendor_items VALUES (4388,17719306,40,0,0,0,0,0,0);	-- Eggplant

-- Arachagnon
INSERT INTO vendor_items VALUES (12633,17723587,270,0,0,0,0,0,0);	-- Elvaan Jerkin
INSERT INTO vendor_items VALUES (12634,17723587,270,0,0,0,0,0,0);	-- Elvaan Bodice
INSERT INTO vendor_items VALUES (12755,17723587,162,0,0,0,0,0,0);	-- Elvaan Gloves
INSERT INTO vendor_items VALUES (12759,17723587,162,0,0,0,0,0,0);	-- Elvaan Gauntlets
INSERT INTO vendor_items VALUES (12885,17723587,234,0,0,0,0,0,0);	-- Elvaan M Chausses
INSERT INTO vendor_items VALUES (12889,17723587,234,0,0,0,0,0,0);	-- Elvaan F Chausses
INSERT INTO vendor_items VALUES (13006,17723587,162,0,0,0,0,0,0);	-- Elvaan M Ledelsens
INSERT INTO vendor_items VALUES (13011,17723587,162,0,0,0,0,0,0);	-- Elvaan F Ledelsens

-- Areebah
INSERT INTO vendor_items VALUES (636,17776718,119,0,0,0,0,0,0);	-- Chamomile
INSERT INTO vendor_items VALUES (951,17776718,110,0,0,0,0,0,0);	-- Wijnruit
INSERT INTO vendor_items VALUES (948,17776718,60,0,0,0,0,0,0);	-- Carnation
INSERT INTO vendor_items VALUES (941,17776718,80,0,0,0,0,0,0);	-- Red Rose
INSERT INTO vendor_items VALUES (949,17776718,96,0,0,0,0,0,0);	-- Rain Lily
INSERT INTO vendor_items VALUES (956,17776718,120,0,0,0,0,0,0);	-- Lilac
INSERT INTO vendor_items VALUES (957,17776718,120,0,0,0,0,0,0);	-- Amaryllis
INSERT INTO vendor_items VALUES (958,17776718,120,0,0,0,0,0,0);	-- Marguerite

-- Arlenne
INSERT INTO vendor_items VALUES (17051,17723446,1409,1,0,0,1,0,0);	-- Yew Wand
INSERT INTO vendor_items VALUES (17090,17723446,3245,1,0,0,1,0,0);	-- Elm Staff
INSERT INTO vendor_items VALUES (17097,17723446,16416,1,0,0,1,0,0);	-- Elm Pole
INSERT INTO vendor_items VALUES (16835,17723446,15876,0,0,0,0,0,0);	-- Spear
INSERT INTO vendor_items VALUES (16845,17723446,16578,0,0,0,0,0,0);	-- Lance
INSERT INTO vendor_items VALUES (16770,17723446,11286,1,0,0,1,0,0);	-- Zaghnal
INSERT INTO vendor_items VALUES (17050,17723446,333,0,0,0,0,0,0);	-- Willow Wand
INSERT INTO vendor_items VALUES (17089,17723446,571,0,0,0,0,0,0);	-- Holly Staff
INSERT INTO vendor_items VALUES (17096,17723446,4568,2,0,0,0,0,0);	-- Holly Pole
INSERT INTO vendor_items VALUES (16834,17723446,4680,0,0,0,0,0,0);	-- Brass Spear
INSERT INTO vendor_items VALUES (16769,17723446,2542,0,0,0,0,0,0);	-- Brass Zaghnal
INSERT INTO vendor_items VALUES (17049,17723446,46,0,0,0,0,0,0);	-- Maple Wand
INSERT INTO vendor_items VALUES (17088,17723446,57,0,0,0,0,0,0);	-- Ash Staff
INSERT INTO vendor_items VALUES (16833,17723446,792,0,0,0,0,0,0);	-- Brass Baghnakhs
INSERT INTO vendor_items VALUES (16768,17723446,309,0,0,0,0,0,0);	-- Bronze Zaghnal

-- Aroro
INSERT INTO vendor_items VALUES (4862,17760312,114,0,0,1,0,0,1);	-- Blind
INSERT INTO vendor_items VALUES (4828,17760312,84,0,0,2,0,0,0);	-- Poison
INSERT INTO vendor_items VALUES (4838,17760312,368,0,0,2,0,0,0);	-- Bio
INSERT INTO vendor_items VALUES (4861,17760312,2300,0,0,2,0,0,0);	-- Sleep
INSERT INTO vendor_items VALUES (4767,17760312,62,0,0,0,0,0,0);	-- Stone
INSERT INTO vendor_items VALUES (4777,17760312,143,0,0,0,0,0,0);	-- Water
INSERT INTO vendor_items VALUES (4762,17760312,331,0,0,0,0,0,0);	-- Aero
INSERT INTO vendor_items VALUES (4752,17760312,855,0,0,0,0,0,0);	-- Fire
INSERT INTO vendor_items VALUES (4757,17760312,1619,0,0,0,0,0,0);	-- Blizzard
INSERT INTO vendor_items VALUES (4772,17760312,3334,0,0,0,0,0,0);	-- Thunder
INSERT INTO vendor_items VALUES (4843,17760312,4747,0,0,0,0,0,0);	-- Burn
INSERT INTO vendor_items VALUES (4844,17760312,3770,0,0,0,0,0,0);	-- Frost
INSERT INTO vendor_items VALUES (4845,17760312,2300,0,0,0,0,0,0);	-- Choke
INSERT INTO vendor_items VALUES (4846,17760312,1867,0,0,0,0,0,0);	-- Rasp
INSERT INTO vendor_items VALUES (4847,17760312,1393,0,0,0,0,0,0);	-- Shock
INSERT INTO vendor_items VALUES (4848,17760312,6508,0,0,0,0,0,0);	-- Drown

-- Ashene
INSERT INTO vendor_items VALUES (16455,17719354,4309,1,0,0,1,0,0);	-- Baselard
INSERT INTO vendor_items VALUES (16532,17719354,16934,1,0,0,1,0,0);	-- Gladius
INSERT INTO vendor_items VALUES (16545,17719354,21067,1,0,0,1,0,0);	-- Broadsword
INSERT INTO vendor_items VALUES (16576,17719354,35769,1,0,0,1,0,0);	-- Hunting Sword
INSERT INTO vendor_items VALUES (16524,17719354,13406,1,0,0,1,0,0);	-- Fleuret
INSERT INTO vendor_items VALUES (16450,17719354,1827,1,0,0,0,0,0);	-- Dagger
INSERT INTO vendor_items VALUES (16536,17719354,7128,1,0,0,0,0,0);	-- Iron Sword
INSERT INTO vendor_items VALUES (16566,17719354,8294,1,0,0,0,0,0);	-- Longsword
INSERT INTO vendor_items VALUES (16385,17719354,129,0,0,0,0,0,0);	-- Cesti
INSERT INTO vendor_items VALUES (16448,17719354,140,0,0,0,0,0,0);	-- Bronze Dagger
INSERT INTO vendor_items VALUES (16449,17719354,837,0,0,0,0,0,0);	-- Brass Dagger
INSERT INTO vendor_items VALUES (16531,17719354,3523,0,0,0,0,0,0);	-- Brass Xiphos
INSERT INTO vendor_items VALUES (16535,17719354,241,0,0,0,0,0,0);	-- Bronze Sword
INSERT INTO vendor_items VALUES (16565,17719354,1674,0,0,0,0,0,0);	-- Spatha

-- Attarena
INSERT INTO vendor_items VALUES (623,17723497,119,0,0,0,0,0,0);	-- Bay Leaves
INSERT INTO vendor_items VALUES (4154,17723497,6440,0,0,0,0,0,0);	-- Holy Water

-- Aulavia
INSERT INTO vendor_items VALUES (636,17735747,119,0,0,0,0,0,0);	-- Chamomile
INSERT INTO vendor_items VALUES (864,17735747,88,0,0,0,0,0,0);	-- Fish Scales
INSERT INTO vendor_items VALUES (936,17735747,14,0,0,0,0,0,0);	-- Rock Salt
INSERT INTO vendor_items VALUES (1410,17735747,1656,0,0,0,0,0,0);	-- Sweet William

-- Aveline
INSERT INTO vendor_items VALUES (625,17719318,79,1,0,0,1,0,0);	-- Apple Vinegar
INSERT INTO vendor_items VALUES (623,17719318,117,1,0,0,1,0,0);	-- Bay Leaves
INSERT INTO vendor_items VALUES (4382,17719318,28,1,0,0,1,0,0);	-- Frost Turnip
INSERT INTO vendor_items VALUES (4392,17719318,28,1,0,0,1,0,0);	-- Saruta Orange
INSERT INTO vendor_items VALUES (4363,17719318,39,2,0,0,0,0,0);	-- Faerie Apple
INSERT INTO vendor_items VALUES (4366,17719318,21,2,0,0,0,0,0);	-- La Theine Cabbage
INSERT INTO vendor_items VALUES (633,17719318,14,0,0,0,0,0,0);	-- Olive Oil
INSERT INTO vendor_items VALUES (638,17719318,166,0,0,0,0,0,0);	-- Sage
INSERT INTO vendor_items VALUES (4389,17719318,28,0,0,0,0,0,0);	-- San d'Orian Carrot
INSERT INTO vendor_items VALUES (4431,17719318,68,0,0,0,0,0,0);	-- San d'Orian Grape

-- Baehu-Faehu
INSERT INTO vendor_items VALUES (4444,17752104,22,0,0,0,0,0,0);	-- Rarab Tail
INSERT INTO vendor_items VALUES (689,17752104,33,0,0,0,0,0,0);	-- Lauan Log
INSERT INTO vendor_items VALUES (619,17752104,43,0,0,0,0,0,0);	-- Popoto
INSERT INTO vendor_items VALUES (4392,17752104,29,0,0,0,0,0,0);	-- Saruta Orange
INSERT INTO vendor_items VALUES (635,17752104,18,0,0,0,0,0,0);	-- Windurstian Tea Leaves

-- Bagnobrok
INSERT INTO vendor_items VALUES (640,17744032,11,0,0,0,0,0,0);	-- Copper Ore
INSERT INTO vendor_items VALUES (4450,17744032,694,0,0,0,0,0,0);	-- Coral Fungus
INSERT INTO vendor_items VALUES (4375,17744032,4032,0,0,0,0,0,0);	-- Danceshroom
INSERT INTO vendor_items VALUES (1650,17744032,6500,0,0,0,0,0,0);	-- Kopparnickel Ore
INSERT INTO vendor_items VALUES (5165,17744032,736,0,0,0,0,0,0);	-- Movalpolos Water

-- Bajahb
INSERT INTO vendor_items VALUES (12424,16982097,10260,0,0,0,0,0,0);	-- Iron Mask
INSERT INTO vendor_items VALUES (12552,16982097,15840,0,0,0,0,0,0);	-- Chainmail
INSERT INTO vendor_items VALUES (12680,16982097,8460,0,0,0,0,0,0);	-- Chain Mittens
INSERT INTO vendor_items VALUES (12808,16982097,12600,0,0,0,0,0,0);	-- Chain Hose
INSERT INTO vendor_items VALUES (12936,16982097,7740,0,0,0,0,0,0);	-- Greaves

-- Balthilda
INSERT INTO vendor_items VALUES (12473,17739803,1904,0,0,0,0,0,0);	-- Poet's Circlet
INSERT INTO vendor_items VALUES (12608,17739803,1288,0,0,0,0,0,0);	-- Tunic
INSERT INTO vendor_items VALUES (12601,17739803,2838,0,0,0,0,0,0);	-- Linen Robe
INSERT INTO vendor_items VALUES (12736,17739803,602,0,0,0,0,0,0);	-- Mitts
INSERT INTO vendor_items VALUES (12729,17739803,1605,0,0,0,0,0,0);	-- Linen Cuffs
INSERT INTO vendor_items VALUES (12864,17739803,860,0,0,0,0,0,0);	-- Slacks
INSERT INTO vendor_items VALUES (12857,17739803,2318,0,0,0,0,0,0);	-- Linen Slops
INSERT INTO vendor_items VALUES (12992,17739803,556,0,0,0,0,0,0);	-- Solea
INSERT INTO vendor_items VALUES (12985,17739803,1495,0,0,0,0,0,0);	-- Holly Clogs
INSERT INTO vendor_items VALUES (13469,17739803,1150,0,0,0,0,0,0);	-- Leather Ring

-- Belka
INSERT INTO vendor_items VALUES (4352,17743908,128,0,0,0,0,0,0);	-- Derfland Pear
INSERT INTO vendor_items VALUES (617,17743908,142,0,0,0,0,0,0);	-- Ginger
INSERT INTO vendor_items VALUES (4545,17743908,62,0,0,0,0,0,0);	-- Gysahl Greens
INSERT INTO vendor_items VALUES (1412,17743908,1656,0,0,0,0,0,0);	-- Olive Flower
INSERT INTO vendor_items VALUES (633,17743908,14,0,0,0,0,0,0);	-- Olive Oil
INSERT INTO vendor_items VALUES (951,17743908,110,0,0,0,0,0,0);	-- Wijnruit

-- Benaige
INSERT INTO vendor_items VALUES (628,17719317,234,1,0,0,1,0,0);	-- Cinnamon
INSERT INTO vendor_items VALUES (629,17719317,43,1,0,0,1,0,0);	-- Millioncorn
INSERT INTO vendor_items VALUES (622,17719317,43,2,0,0,0,0,0);	-- Dried Marjoram
INSERT INTO vendor_items VALUES (610,17719317,54,2,0,0,0,0,0);	-- San d'Orian Flour
INSERT INTO vendor_items VALUES (1840,17719317,1800,2,0,0,0,0,0);	-- Semolina
INSERT INTO vendor_items VALUES (627,17719317,36,2,0,0,0,0,0);	-- Maple Sugar
INSERT INTO vendor_items VALUES (621,17719317,25,0,0,0,0,0,0);	-- Crying Mustard
INSERT INTO vendor_items VALUES (611,17719317,36,0,0,0,0,0,0);	-- Rye Flour
INSERT INTO vendor_items VALUES (936,17719317,14,0,0,0,0,0,0);	-- Rock Salt
INSERT INTO vendor_items VALUES (4509,17719317,10,0,0,0,0,0,0);	-- Distilled Water
INSERT INTO vendor_items VALUES (5234,17719317,198,0,0,0,0,0,0);	-- Cibol

-- Bin Stejihna
INSERT INTO vendor_items VALUES (1840,17764461,1840,0,0,0,0,0,0);	-- Semolina
INSERT INTO vendor_items VALUES (4372,17764461,44,0,0,0,0,0,0);	-- Giant Sheep Meat
INSERT INTO vendor_items VALUES (622,17764461,44,0,0,0,0,0,0);	-- Dried Marjoram
INSERT INTO vendor_items VALUES (610,17764461,55,0,0,0,0,0,0);	-- San d'Orian Flour
INSERT INTO vendor_items VALUES (611,17764461,36,0,0,0,0,0,0);	-- Rye Flour
INSERT INTO vendor_items VALUES (4366,17764461,22,0,0,0,0,0,0);	-- La Theine Cabbage
INSERT INTO vendor_items VALUES (4378,17764461,55,0,0,0,0,0,0);	-- Selbina Milk

-- Blingbrix
INSERT INTO vendor_items VALUES (4116,17134075,4500,0,0,0,0,0,0);	-- Hi-Potion
INSERT INTO vendor_items VALUES (4132,17134075,28000,0,0,0,0,0,0);	-- Hi-Ether
INSERT INTO vendor_items VALUES (605,17134075,200,0,0,0,0,0,0);	-- Pickaxe
INSERT INTO vendor_items VALUES (1020,17134075,300,0,0,0,0,0,0);	-- Sickle

-- Boncort
INSERT INTO vendor_items VALUES (4441,17723465,837,1,0,0,1,0,0);	-- Grape Juice
INSERT INTO vendor_items VALUES (4356,17723465,180,2,0,0,0,0,0);	-- White Bread
INSERT INTO vendor_items VALUES (4380,17723465,198,2,0,0,0,0,0);	-- Smoked Salmon
INSERT INTO vendor_items VALUES (4423,17723465,270,2,0,0,0,0,0);	-- Apple Juice
INSERT INTO vendor_items VALUES (4364,17723465,108,0,0,0,0,0,0);	-- Black Bread
INSERT INTO vendor_items VALUES (4376,17723465,108,0,0,0,0,0,0);	-- Meat Jerky
INSERT INTO vendor_items VALUES (4509,17723465,10,0,0,0,0,0,0);	-- Distilled Water
INSERT INTO vendor_items VALUES (5007,17723465,163,0,0,0,0,0,0);	-- Scroll of Sword Madrigal

-- Bonmaurieut
INSERT INTO vendor_items VALUES (1413,17727530,1656,0,0,0,0,0,0);	-- Cattleya
INSERT INTO vendor_items VALUES (628,17727530,239,0,0,0,0,0,0);	-- Cinnamon
INSERT INTO vendor_items VALUES (4468,17727530,73,0,0,0,0,0,0);	-- Pamamas
INSERT INTO vendor_items VALUES (721,17727530,147,0,0,0,0,0,0);	-- Rattan Lumber

-- Boytz
INSERT INTO vendor_items VALUES (4128,17735724,4445,0,1,0,0,1,0);	-- Ether
INSERT INTO vendor_items VALUES (4151,17735724,736,0,2,0,0,0,0);	-- Echo Drops
INSERT INTO vendor_items VALUES (4112,17735724,837,0,2,0,0,0,0);	-- Potion
INSERT INTO vendor_items VALUES (17318,17735724,3,0,2,0,0,0,0);	-- Wooden Arrow
INSERT INTO vendor_items VALUES (217,17735724,900,0,0,0,0,0,0);	-- Brass Flowerpot
INSERT INTO vendor_items VALUES (605,17735724,180,0,0,0,0,0,0);	-- Pickaxe
INSERT INTO vendor_items VALUES (4150,17735724,2387,0,0,0,0,0,0);	-- Eye Drops
INSERT INTO vendor_items VALUES (4148,17735724,290,0,0,0,0,0,0);	-- Antidote
INSERT INTO vendor_items VALUES (17320,17735724,7,0,0,0,0,0,0);	-- Iron Arrow
INSERT INTO vendor_items VALUES (17336,17735724,5,0,0,0,0,0,0);	-- Crossbow Bolt

-- Brave Ox
INSERT INTO vendor_items VALUES (4654,17788945,77350,0,0,0,0,0,0);	-- Protect IV
INSERT INTO vendor_items VALUES (4736,17788945,73710,0,0,0,0,0,0);	-- Protectra IV
INSERT INTO vendor_items VALUES (4868,17788945,63700,0,0,0,0,0,0);	-- Dispel
INSERT INTO vendor_items VALUES (4860,17788945,31850,0,0,0,0,0,0);	-- Stun
INSERT INTO vendor_items VALUES (4720,17788945,31850,0,0,0,0,0,0);	-- Flash
INSERT INTO vendor_items VALUES (4750,17788945,546000,0,0,0,0,0,0);	-- Reraise III
INSERT INTO vendor_items VALUES (4638,17788945,78260,0,0,0,0,0,0);	-- Banish III
INSERT INTO vendor_items VALUES (4701,17788945,20092,0,0,0,0,0,0);	-- 4701, 20092, -- Cura
INSERT INTO vendor_items VALUES (4702,17788945,62192,0,0,0,0,0,0);	-- 4702, 62192, -- Sacrifice
INSERT INTO vendor_items VALUES (4703,17788945,64584,0,0,0,0,0,0);	-- 4703, 64584, -- Esuna
INSERT INTO vendor_items VALUES (4704,17788945,30967,0,0,0,0,0,0);	-- 4704, 30967, -- Auspice

-- Brave Wolf
INSERT INTO vendor_items VALUES (12301,17788944,31201,0,0,0,0,0,0);	-- Buckler
INSERT INTO vendor_items VALUES (12302,17788944,60260,0,0,0,0,0,0);	-- Darksteel Buckler
INSERT INTO vendor_items VALUES (13979,17788944,24373,0,0,0,0,0,0);	-- Silver Bangles
INSERT INTO vendor_items VALUES (12554,17788944,66066,0,0,0,0,0,0);	-- Banded Mail
INSERT INTO vendor_items VALUES (12682,17788944,35285,0,0,0,0,0,0);	-- Mufflers
INSERT INTO vendor_items VALUES (12810,17788944,52552,0,0,0,0,0,0);	-- Breeches
INSERT INTO vendor_items VALUES (12938,17788944,32382,0,0,0,0,0,0);	-- Sollerets
INSERT INTO vendor_items VALUES (12609,17788944,9423,0,0,0,0,0,0);	-- Black Tunic
INSERT INTO vendor_items VALUES (12737,17788944,4395,0,0,0,0,0,0);	-- White Mitts
INSERT INTO vendor_items VALUES (12865,17788944,6279,0,0,0,0,0,0);	-- Black Slacks
INSERT INTO vendor_items VALUES (12993,17788944,4084,0,0,0,0,0,0);	-- Sandals
INSERT INTO vendor_items VALUES (12578,17788944,28654,0,0,0,0,0,0);	-- Padded Armor
INSERT INTO vendor_items VALUES (12706,17788944,15724,0,0,0,0,0,0);	-- Iron Mittens
INSERT INTO vendor_items VALUES (12836,17788944,23063,0,0,0,0,0,0);	-- Iron Subligar
INSERT INTO vendor_items VALUES (12962,17788944,14327,0,0,0,0,0,0);	-- Leggins

-- Brunhilde
INSERT INTO vendor_items VALUES (12448,17739801,154,0,0,0,0,0,0);	-- Bronze Cap
INSERT INTO vendor_items VALUES (12432,17739801,1334,0,0,0,0,0,0);	-- Faceguard
INSERT INTO vendor_items VALUES (12433,17739801,11776,0,2,0,0,0,0);	-- Brass Mask
INSERT INTO vendor_items VALUES (12416,17739801,29311,0,2,0,0,0,0);	-- Sallet
INSERT INTO vendor_items VALUES (12576,17739801,235,0,0,0,0,0,0);	-- Bronze Harness
INSERT INTO vendor_items VALUES (12560,17739801,2051,0,0,0,0,0,0);	-- Scale Mail
INSERT INTO vendor_items VALUES (12561,17739801,17928,0,2,0,0,0,0);	-- Brass Scale Mail
INSERT INTO vendor_items VALUES (12704,17739801,128,0,0,0,0,0,0);	-- Bronze Mittens
INSERT INTO vendor_items VALUES (12688,17739801,1094,0,0,0,0,0,0);	-- Scale Finger Gauntlets
INSERT INTO vendor_items VALUES (12689,17739801,9479,0,2,0,0,0,0);	-- Brass Finger Gauntlets
INSERT INTO vendor_items VALUES (12417,17739801,52289,0,1,0,0,1,0);	-- Mythril Sallet
INSERT INTO vendor_items VALUES (12544,17739801,45208,0,1,0,0,1,0);	-- Breastplate
INSERT INTO vendor_items VALUES (12672,17739801,23846,0,1,0,0,1,0);	-- Gauntlets

-- Caiphimonride
INSERT INTO vendor_items VALUES (16450,16883792,2030,0,0,0,0,0,0);	-- Dagger
INSERT INTO vendor_items VALUES (16566,16883792,9216,0,0,0,0,0,0);	-- Longsword
INSERT INTO vendor_items VALUES (17335,16883792,4,0,0,0,0,0,0);	-- Rusty Bolt
INSERT INTO vendor_items VALUES (18375,16883792,37296,0,0,0,0,0,0);	-- Falx
INSERT INTO vendor_items VALUES (18214,16883792,20762,0,0,0,0,0,0);	-- Voulge

-- Capucine
INSERT INTO vendor_items VALUES (12473,17719352,1904,0,0,0,0,0,0);	-- Poet's Circlet
INSERT INTO vendor_items VALUES (12608,17719352,1288,0,0,0,0,0,0);	-- Tunic
INSERT INTO vendor_items VALUES (12601,17719352,2838,0,0,0,0,0,0);	-- Linen Robe
INSERT INTO vendor_items VALUES (12736,17719352,602,0,0,0,0,0,0);	-- Mitts
INSERT INTO vendor_items VALUES (12729,17719352,1605,0,0,0,0,0,0);	-- Linen Cuffs
INSERT INTO vendor_items VALUES (12864,17719352,860,0,0,0,0,0,0);	-- Slacks
INSERT INTO vendor_items VALUES (12857,17719352,2318,0,0,0,0,0,0);	-- Linen Slops
INSERT INTO vendor_items VALUES (12992,17719352,556,0,0,0,0,0,0);	-- Solea
INSERT INTO vendor_items VALUES (12985,17719352,1495,0,0,0,0,0,0);	-- Holly Clogs

-- Carautia
INSERT INTO vendor_items VALUES (12808,17719388,11340,1,0,0,1,0,0);	-- Chain Hose
INSERT INTO vendor_items VALUES (12936,17719388,6966,1,0,0,1,0,0);	-- Greaves
INSERT INTO vendor_items VALUES (12306,17719388,10281,1,0,0,1,0,0);	-- Kite Shield
INSERT INTO vendor_items VALUES (12292,17719388,4482,2,0,0,0,0,0);	-- Mahogany Shield
INSERT INTO vendor_items VALUES (12826,17719388,16552,2,0,0,0,0,0);	-- Studded Trousers
INSERT INTO vendor_items VALUES (12954,17719388,10054,2,0,0,0,0,0);	-- Studded Boots
INSERT INTO vendor_items VALUES (12290,17719388,544,0,0,0,0,0,0);	-- Maple Shield
INSERT INTO vendor_items VALUES (12832,17719388,187,0,0,0,0,0,0);	-- Bronze Subligar
INSERT INTO vendor_items VALUES (12833,17719388,1800,0,0,0,0,0,0);	-- Brass Subligar
INSERT INTO vendor_items VALUES (12824,17719388,482,0,0,0,0,0,0);	-- Leather Trousers
INSERT INTO vendor_items VALUES (12960,17719388,115,0,0,0,0,0,0);	-- Bronze Leggings
INSERT INTO vendor_items VALUES (12961,17719388,1116,0,0,0,0,0,0);	-- Brass Leggings
INSERT INTO vendor_items VALUES (12952,17719388,302,0,0,0,0,0,0);	-- Leather Highboots

-- Carmelide
INSERT INTO vendor_items VALUES (806,17739810,1713,0,0,0,0,0,0);	-- Tourmaline
INSERT INTO vendor_items VALUES (807,17739810,1713,0,0,0,0,0,0);	-- Sardonyx
INSERT INTO vendor_items VALUES (800,17739810,1713,0,0,0,0,0,0);	-- Amethyst
INSERT INTO vendor_items VALUES (814,17739810,1713,0,0,0,0,0,0);	-- Amber
INSERT INTO vendor_items VALUES (795,17739810,1713,0,0,0,0,0,0);	-- Lapis Lazuli
INSERT INTO vendor_items VALUES (809,17739810,1713,0,0,0,0,0,0);	-- Clear Topaz
INSERT INTO vendor_items VALUES (799,17739810,1713,0,0,0,0,0,0);	-- Onyx
INSERT INTO vendor_items VALUES (796,17739810,1713,0,0,0,0,0,0);	-- Light Opal
INSERT INTO vendor_items VALUES (13454,17739810,69,0,0,0,0,0,0);	-- Copper Ring

-- Challoux
INSERT INTO vendor_items VALUES (4545,17784886,62,0,0,0,0,0,0);	-- Gysahl Greens
INSERT INTO vendor_items VALUES (840,17784886,4,0,0,0,0,0,0);	-- Chocobo Feather
INSERT INTO vendor_items VALUES (17307,17784886,9,0,0,0,0,0,0);	-- Dart

-- Champalpieu
INSERT INTO vendor_items VALUES (4365,17776717,120,0,0,0,0,0,0);	-- Rolanberry
INSERT INTO vendor_items VALUES (17320,17776717,7,0,0,0,0,0,0);	-- Iron Arrow
INSERT INTO vendor_items VALUES (17336,17776717,5,0,0,0,0,0,0);	-- Crossbow Bolt
INSERT INTO vendor_items VALUES (605,17776717,180,0,0,0,0,0,0);	-- Pickaxe
INSERT INTO vendor_items VALUES (5064,17776717,567,0,0,0,0,0,0);	-- Wind Threnody
INSERT INTO vendor_items VALUES (5067,17776717,420,0,0,0,0,0,0);	-- Water Threnody

-- Charging Chocobo
INSERT INTO vendor_items VALUES (12801,17739802,58738,0,1,0,0,1,0);	-- Mythril Cuisses
INSERT INTO vendor_items VALUES (12929,17739802,36735,0,1,0,0,1,0);	-- Mythril Leggings
INSERT INTO vendor_items VALUES (12817,17739802,14131,0,2,0,0,0,0);	-- Brass Cuisses
INSERT INTO vendor_items VALUES (12800,17739802,34776,0,2,0,0,0,0);	-- Cuisses
INSERT INTO vendor_items VALUES (12945,17739802,8419,0,2,0,0,0,0);	-- Brass Greaves
INSERT INTO vendor_items VALUES (12928,17739802,21859,0,2,0,0,0,0);	-- Plate Leggings
INSERT INTO vendor_items VALUES (13080,17739802,16891,0,2,0,0,0,0);	-- Gorget
INSERT INTO vendor_items VALUES (12832,17739802,191,0,0,0,0,0,0);	-- Bronze Subligar
INSERT INTO vendor_items VALUES (12816,17739802,1646,0,0,0,0,0,0);	-- Scale Cuisses
INSERT INTO vendor_items VALUES (12960,17739802,117,0,0,0,0,0,0);	-- Bronze Leggings
INSERT INTO vendor_items VALUES (12944,17739802,998,0,0,0,0,0,0);	-- Scale Greaves

-- Chayaya
INSERT INTO vendor_items VALUES (17307,16974277,10,0,0,0,0,0,0);	-- Dart
INSERT INTO vendor_items VALUES (17308,16974277,60,0,0,0,0,0,0);	-- Hawkeye
INSERT INTO vendor_items VALUES (17313,16974277,1204,0,0,0,0,0,0);	-- Grenade
INSERT INTO vendor_items VALUES (17320,16974277,8,0,0,0,0,0,0);	-- Iron Arrow
INSERT INTO vendor_items VALUES (5477,16974277,68000,0,0,0,0,0,0);	-- Warrior Die
INSERT INTO vendor_items VALUES (5478,16974277,22400,0,0,0,0,0,0);	-- Monk Die
INSERT INTO vendor_items VALUES (5479,16974277,5000,0,0,0,0,0,0);	-- White Mage Die
INSERT INTO vendor_items VALUES (5480,16974277,108000,0,0,0,0,0,0);	-- Black Mage Die
INSERT INTO vendor_items VALUES (5481,16974277,62000,0,0,0,0,0,0);	-- Red Mage Die
INSERT INTO vendor_items VALUES (5482,16974277,50400,0,0,0,0,0,0);	-- Thief Die
INSERT INTO vendor_items VALUES (5483,16974277,90750,0,0,0,0,0,0);	-- Paladin Die
INSERT INTO vendor_items VALUES (5484,16974277,2205,0,0,0,0,0,0);	-- Dark Knight Die
INSERT INTO vendor_items VALUES (5485,16974277,26600,0,0,0,0,0,0);	-- Beastmaster Die
INSERT INTO vendor_items VALUES (5486,16974277,12780,0,0,0,0,0,0);	-- Bard Die
INSERT INTO vendor_items VALUES (5487,16974277,1300,0,0,0,0,0,0);	-- Ranger Die
INSERT INTO vendor_items VALUES (5495,16974277,63375,0,0,0,0,0,0);	-- Dancer Die
INSERT INTO vendor_items VALUES (5496,16974277,68250,0,0,0,0,0,0);	-- Scholar Die

-- Chenokih
INSERT INTO vendor_items VALUES (12850,17780865,24500,0,0,0,0,0,0);	-- Hose
INSERT INTO vendor_items VALUES (12866,17780865,22632,0,0,0,0,0,0);	-- Linen Slacks
INSERT INTO vendor_items VALUES (12851,17780865,57600,0,0,0,0,0,0);	-- Wool Hose
INSERT INTO vendor_items VALUES (12858,17780865,14756,0,0,0,0,0,0);	-- Wool Slops
INSERT INTO vendor_items VALUES (12865,17780865,6348,0,0,0,0,0,0);	-- Black Slacks
INSERT INTO vendor_items VALUES (12978,17780865,16000,0,0,0,0,0,0);	-- Socks
INSERT INTO vendor_items VALUES (12994,17780865,14352,0,0,0,0,0,0);	-- Shoes
INSERT INTO vendor_items VALUES (12979,17780865,35200,0,0,0,0,0,0);	-- Wool Socks
INSERT INTO vendor_items VALUES (12986,17780865,9180,0,0,0,0,0,0);	-- Chestnut Sabots
INSERT INTO vendor_items VALUES (12993,17780865,4128,0,0,0,0,0,0);	-- Sandals
INSERT INTO vendor_items VALUES (13577,17780865,11088,0,0,0,0,0,0);	-- Black Cape
INSERT INTO vendor_items VALUES (13568,17780865,1250,0,0,0,0,0,0);	-- Scarlet Ribbon

-- Chetak
INSERT INTO vendor_items VALUES (12466,17780864,20000,0,0,0,0,0,0);	-- Red Cap
INSERT INTO vendor_items VALUES (12467,17780864,45760,0,0,0,0,0,0);	-- Wool Cap
INSERT INTO vendor_items VALUES (12474,17780864,11166,0,0,0,0,0,0);	-- Wool Hat
INSERT INTO vendor_items VALUES (12594,17780864,32500,0,0,0,0,0,0);	-- Gambison
INSERT INTO vendor_items VALUES (12610,17780864,33212,0,0,0,0,0,0);	-- Cloak
INSERT INTO vendor_items VALUES (12595,17780864,68640,0,0,0,0,0,0);	-- Wool Gambison
INSERT INTO vendor_items VALUES (12602,17780864,18088,0,0,0,0,0,0);	-- Wool Robe
INSERT INTO vendor_items VALUES (12609,17780864,9527,0,0,0,0,0,0);	-- Black Tunic
INSERT INTO vendor_items VALUES (12722,17780864,16900,0,0,0,0,0,0);	-- Bracers
INSERT INTO vendor_items VALUES (12738,17780864,15732,0,0,0,0,0,0);	-- Linen Mitts
INSERT INTO vendor_items VALUES (12730,17780864,10234,0,0,0,0,0,0);	-- Wool Cuffs
INSERT INTO vendor_items VALUES (12737,17780864,4443,0,0,0,0,0,0);	-- White Mitts

-- Chhaya
INSERT INTO vendor_items VALUES (4112,17682456,910,0,0,0,0,0,0);	-- Potion
INSERT INTO vendor_items VALUES (4128,17682456,4832,0,0,0,0,0,0);	-- Ether
INSERT INTO vendor_items VALUES (4148,17682456,316,0,0,0,0,0,0);	-- Antidote
INSERT INTO vendor_items VALUES (4150,17682456,2595,0,0,0,0,0,0);	-- Eye Drops
INSERT INTO vendor_items VALUES (4151,17682456,800,0,0,0,0,0,0);	-- Echo Drops

-- Chichiroon
INSERT INTO vendor_items VALUES (5497,16994373,99224,0,0,0,0,0,0);	-- Bolter's Die
INSERT INTO vendor_items VALUES (5498,16994373,85500,0,0,0,0,0,0);	-- Caster's Die
INSERT INTO vendor_items VALUES (5499,16994373,97350,0,0,0,0,0,0);	-- Courser's Die
INSERT INTO vendor_items VALUES (5500,16994373,100650,0,0,0,0,0,0);	-- Blitzer's Die
INSERT INTO vendor_items VALUES (5501,16994373,109440,0,0,0,0,0,0);	-- Tactician's Die
INSERT INTO vendor_items VALUES (5502,16994373,116568,0,0,0,0,0,0);	-- Allies' Die
INSERT INTO vendor_items VALUES (5503,16994373,96250,0,0,0,0,0,0);	-- Miser's Die
INSERT INTO vendor_items VALUES (5504,16994373,95800,0,0,0,0,0,0);	-- Companion's Die
INSERT INTO vendor_items VALUES (5505,16994373,123744,0,0,0,0,0,0);	-- Avenger's Die
INSERT INTO vendor_items VALUES (6368,16994373,69288,0,0,0,0,0,0);	-- Geomancer Die
INSERT INTO vendor_items VALUES (6369,16994373,73920,0,0,0,0,0,0);	-- Rune Fencer Die

-- Chutarmire
INSERT INTO vendor_items VALUES (4768,17793068,5751,0,0,0,0,0,0);	-- Scroll of Stone II
INSERT INTO vendor_items VALUES (4778,17793068,8100,0,0,0,0,0,0);	-- Scroll of Water II
INSERT INTO vendor_items VALUES (4763,17793068,11970,0,0,0,0,0,0);	-- Scroll of Aero II
INSERT INTO vendor_items VALUES (4753,17793068,16560,0,0,0,0,0,0);	-- Scroll of Fire II
INSERT INTO vendor_items VALUES (4758,17793068,21870,0,0,0,0,0,0);	-- Scroll of Blizzard II
INSERT INTO vendor_items VALUES (4773,17793068,27900,0,0,0,0,0,0);	-- Scroll of Thunder II
INSERT INTO vendor_items VALUES (4797,17793068,1165,0,0,0,0,0,0);	-- Scroll of Stonega
INSERT INTO vendor_items VALUES (4807,17793068,2097,0,0,0,0,0,0);	-- Scroll of Waterga
INSERT INTO vendor_items VALUES (4792,17793068,4147,0,0,0,0,0,0);	-- Scroll of Aeroga
INSERT INTO vendor_items VALUES (4782,17793068,7025,0,0,0,0,0,0);	-- Scroll of Firaga
INSERT INTO vendor_items VALUES (4787,17793068,10710,0,0,0,0,0,0);	-- Scroll of Blizzaga
INSERT INTO vendor_items VALUES (4802,17793068,15120,0,0,0,0,0,0);	-- Scroll of Thundaga
INSERT INTO vendor_items VALUES (4829,17793068,22680,0,0,0,0,0,0);	-- Scroll of Poison II
INSERT INTO vendor_items VALUES (4839,17793068,12600,0,0,0,0,0,0);	-- Scroll of Bio II
INSERT INTO vendor_items VALUES (4833,17793068,4644,0,0,0,0,0,0);	-- Scroll of Poisonga
INSERT INTO vendor_items VALUES (4859,17793068,8100,0,0,0,0,0,0);	-- Scroll of Shock Spikes

-- Ciqala
INSERT INTO vendor_items VALUES (16392,17739799,4818,0,0,0,0,0,0);	-- Metal Knuckles
INSERT INTO vendor_items VALUES (17044,17739799,6033,0,0,0,0,0,0);	-- Warhammer
INSERT INTO vendor_items VALUES (16643,17739799,11285,0,0,0,0,0,0);	-- Battleaxe
INSERT INTO vendor_items VALUES (16705,17739799,4186,0,0,0,0,0,0);	-- Greataxe
INSERT INTO vendor_items VALUES (16391,17739799,828,0,0,0,0,0,0);	-- Brass Knuckles
INSERT INTO vendor_items VALUES (17043,17739799,2083,0,0,0,0,0,0);	-- Brass Hammer
INSERT INTO vendor_items VALUES (16641,17739799,1435,0,0,0,0,0,0);	-- Brass Axe
INSERT INTO vendor_items VALUES (16704,17739799,618,0,0,0,0,0,0);	-- Butterfly Axe
INSERT INTO vendor_items VALUES (16390,17739799,224,0,0,0,0,0,0);	-- Bronze Knuckles
INSERT INTO vendor_items VALUES (17042,17739799,312,0,0,0,0,0,0);	-- Bronze Hammer
INSERT INTO vendor_items VALUES (16640,17739799,290,0,0,0,0,0,0);	-- Bronze Axe
INSERT INTO vendor_items VALUES (17049,17739799,47,0,0,0,0,0,0);	-- Maple Wand
INSERT INTO vendor_items VALUES (17088,17739799,58,0,0,0,0,0,0);	-- Ash Staff

-- Corua
INSERT INTO vendor_items VALUES (4389,17719304,29,0,0,0,0,0,0);	-- San d'Orian Carrot
INSERT INTO vendor_items VALUES (4431,17719304,69,0,0,0,0,0,0);	-- San d'Orian Grape
INSERT INTO vendor_items VALUES (639,17719304,110,0,0,0,0,0,0);	-- Chestnut
INSERT INTO vendor_items VALUES (610,17719304,55,0,0,0,0,0,0);	-- San d'Orian Flour

-- Coullave
INSERT INTO vendor_items VALUES (4128,17727523,4445,1,0,0,1,0,0);	-- Ether
INSERT INTO vendor_items VALUES (17313,17727523,1107,1,0,0,1,0,0);	-- Grenade
INSERT INTO vendor_items VALUES (12456,17727523,552,2,0,0,0,0,0);	-- Hachimaki
INSERT INTO vendor_items VALUES (12584,17727523,833,2,0,0,0,0,0);	-- Kenpogi
INSERT INTO vendor_items VALUES (12968,17727523,424,2,0,0,0,0,0);	-- Kyahan
INSERT INTO vendor_items VALUES (4112,17727523,837,1,0,0,1,0,0);	-- Potion
INSERT INTO vendor_items VALUES (12712,17727523,458,2,0,0,0,0,0);	-- Tekko
INSERT INTO vendor_items VALUES (12840,17727523,666,2,0,0,0,0,0);	-- Sitabaki
INSERT INTO vendor_items VALUES (704,17727523,96,2,0,0,0,0,0);	-- Bamboo Stick
INSERT INTO vendor_items VALUES (4151,17727523,736,2,0,0,0,0,0);	-- Echo Drops
INSERT INTO vendor_items VALUES (4148,17727523,290,0,0,0,0,0,0);	-- Antidote
INSERT INTO vendor_items VALUES (4150,17727523,2387,0,0,0,0,0,0);	-- Eye Drops
INSERT INTO vendor_items VALUES (13469,17727523,1150,0,0,0,0,0,0);	-- Leather Ring

-- Coumuna
INSERT INTO vendor_items VALUES (16705,17776714,4550,0,0,0,0,0,0);	-- Greataxe
INSERT INTO vendor_items VALUES (16518,17776714,31000,0,0,0,0,0,0);	-- Mythril Degen
INSERT INTO vendor_items VALUES (16460,17776714,12096,0,0,0,0,0,0);	-- Kris
INSERT INTO vendor_items VALUES (16467,17776714,14560,0,0,0,0,0,0);	-- Mythril Knife
INSERT INTO vendor_items VALUES (16399,17776714,15488,0,0,0,0,0,0);	-- Katars
INSERT INTO vendor_items VALUES (16589,17776714,13962,0,0,0,0,0,0);	-- Two-Handed Sword
INSERT INTO vendor_items VALUES (16412,17776714,29760,0,0,0,0,0,0);	-- Mythril Claws
INSERT INTO vendor_items VALUES (16567,17776714,85250,0,0,0,0,0,0);	-- Knight's Sword

-- Creepstix
INSERT INTO vendor_items VALUES (5023,17780859,8160,0,0,0,0,0,0);	-- Scroll of Goblin Gavotte
INSERT INTO vendor_items VALUES (4734,17780859,7074,0,0,0,0,0,0);	-- Scroll of Protectra II
INSERT INTO vendor_items VALUES (4738,17780859,1700,0,0,0,0,0,0);	-- Scroll of Shellra

-- Croumangue
INSERT INTO vendor_items VALUES (4441,17727503,837,1,0,0,1,0,0);	-- Grape Juice
INSERT INTO vendor_items VALUES (4419,17727503,6300,1,0,0,1,0,0);	-- Mushroom Soup
INSERT INTO vendor_items VALUES (4404,17727503,540,1,0,0,1,0,0);	-- Roast Trout
INSERT INTO vendor_items VALUES (4423,17727503,270,2,0,0,0,0,0);	-- Apple Juice
INSERT INTO vendor_items VALUES (4537,17727503,468,2,0,0,0,0,0);	-- Roast Carp
INSERT INTO vendor_items VALUES (4560,17727503,1355,2,0,0,0,0,0);	-- Vegetable Soup
INSERT INTO vendor_items VALUES (4356,17727503,180,2,0,0,0,0,0);	-- White Bread
INSERT INTO vendor_items VALUES (4364,17727503,108,0,0,0,0,0,0);	-- Black Bread
INSERT INTO vendor_items VALUES (4535,17727503,360,0,0,0,0,0,0);	-- Boiled Crayfish
INSERT INTO vendor_items VALUES (4509,17727503,10,0,0,0,0,0,0);	-- Distilled Water
INSERT INTO vendor_items VALUES (4455,17727503,180,0,0,0,0,0,0);	-- Pebble Soup

-- Dabih Jajalioh
INSERT INTO vendor_items VALUES (957,17772597,120,0,0,0,0,0,0);	-- Amaryllis
INSERT INTO vendor_items VALUES (948,17772597,60,0,0,0,0,0,0);	-- Carnation
INSERT INTO vendor_items VALUES (636,17772597,119,0,0,0,0,0,0);	-- Chamomile
INSERT INTO vendor_items VALUES (956,17772597,120,0,0,0,0,0,0);	-- Lilac
INSERT INTO vendor_items VALUES (958,17772597,120,0,0,0,0,0,0);	-- Marguerite
INSERT INTO vendor_items VALUES (949,17772597,96,0,0,0,0,0,0);	-- Rain Lily
INSERT INTO vendor_items VALUES (941,17772597,80,0,0,0,0,0,0);	-- Red Rose
INSERT INTO vendor_items VALUES (951,17772597,110,0,0,0,0,0,0);	-- Wijnruit

-- Deadly Minnow
INSERT INTO vendor_items VALUES (12442,17776696,13179,0,0,0,0,0,0);	-- Studded Bandana
INSERT INTO vendor_items VALUES (12425,17776696,22800,0,0,0,0,0,0);	-- Silver Mask
INSERT INTO vendor_items VALUES (12426,17776696,47025,0,0,0,0,0,0);	-- Banded Helm
INSERT INTO vendor_items VALUES (12570,17776696,20976,0,0,0,0,0,0);	-- Studded Vest
INSERT INTO vendor_items VALUES (12553,17776696,35200,0,0,0,0,0,0);	-- Silver Mail
INSERT INTO vendor_items VALUES (12554,17776696,66792,0,0,0,0,0,0);	-- Banded Mail
INSERT INTO vendor_items VALUES (12698,17776696,11012,0,0,0,0,0,0);	-- Studded Gloves
INSERT INTO vendor_items VALUES (12681,17776696,18800,0,0,0,0,0,0);	-- Silver Mittens
INSERT INTO vendor_items VALUES (12672,17776696,23846,0,0,0,0,0,0);	-- Gauntlets
INSERT INTO vendor_items VALUES (12682,17776696,35673,0,0,0,0,0,0);	-- Mufflers

-- Deegis
INSERT INTO vendor_items VALUES (12450,17735722,18360,0,1,0,0,1,0);	-- Padded Cap
INSERT INTO vendor_items VALUES (12424,17735722,9234,0,1,0,0,1,0);	-- Iron Mask
INSERT INTO vendor_items VALUES (12578,17735722,28339,0,1,0,0,1,0);	-- Padded Armor
INSERT INTO vendor_items VALUES (12706,17735722,15552,0,1,0,0,1,0);	-- Iron Mittens
INSERT INTO vendor_items VALUES (12449,17735722,1471,0,2,0,0,0,0);	-- Brass Cap
INSERT INTO vendor_items VALUES (12440,17735722,396,0,2,0,0,0,0);	-- Leather Bandana
INSERT INTO vendor_items VALUES (12577,17735722,2236,0,2,0,0,0,0);	-- Brass Harness
INSERT INTO vendor_items VALUES (12568,17735722,604,0,2,0,0,0,0);	-- Leather Vest
INSERT INTO vendor_items VALUES (12705,17735722,1228,0,2,0,0,0,0);	-- Brass Mittens
INSERT INTO vendor_items VALUES (12696,17735722,324,0,2,0,0,0,0);	-- Leather Gloves
INSERT INTO vendor_items VALUES (12448,17735722,151,0,0,0,0,0,0);	-- Bronze Cap
INSERT INTO vendor_items VALUES (12576,17735722,230,0,0,0,0,0,0);	-- Bronze Harness
INSERT INTO vendor_items VALUES (12552,17735722,14256,0,0,0,0,0,0);	-- Chainmail
INSERT INTO vendor_items VALUES (12704,17735722,126,0,0,0,0,0,0);	-- Bronze Mittens
INSERT INTO vendor_items VALUES (12680,17735722,7614,0,0,0,0,0,0);	-- Chain Mittens

-- Deguerendars
INSERT INTO vendor_items VALUES (1523,17727527,290,0,0,0,0,0,0);	-- Apple Mint
INSERT INTO vendor_items VALUES (5164,17727527,1945,0,0,0,0,0,0);	-- Ground Wasabi
INSERT INTO vendor_items VALUES (17005,17727527,99,0,0,0,0,0,0);	-- Lufaise Fly
INSERT INTO vendor_items VALUES (5195,17727527,233,0,0,0,0,0,0);	-- Misareaux Parsley
INSERT INTO vendor_items VALUES (1695,17727527,920,0,0,0,0,0,0);	-- Habanero Peppers

-- Denvihr
INSERT INTO vendor_items VALUES (699,17743975,5688,0,1,0,0,1,0);	-- Oak Log
INSERT INTO vendor_items VALUES (644,17743975,1800,0,1,0,0,1,0);	-- Mythril Ore
INSERT INTO vendor_items VALUES (835,17743975,225,0,1,0,0,1,0);	-- Flax Flower
INSERT INTO vendor_items VALUES (698,17743975,86,0,2,0,0,0,0);	-- Ash Log
INSERT INTO vendor_items VALUES (694,17743975,2543,0,2,0,0,0,0);	-- Chestnut Log
INSERT INTO vendor_items VALUES (643,17743975,810,0,2,0,0,0,0);	-- Iron Ore
INSERT INTO vendor_items VALUES (833,17743975,18,0,2,0,0,0,0);	-- Moko Grass
INSERT INTO vendor_items VALUES (4570,17743975,50,0,2,0,0,0,0);	-- Bird Egg
INSERT INTO vendor_items VALUES (640,17743975,10,0,0,0,0,0,0);	-- Copper Ore
INSERT INTO vendor_items VALUES (136,17743975,1800,0,0,0,0,0,0);	-- Kaiserin Cosmetics

-- Dhen Tevryukoh
INSERT INTO vendor_items VALUES (1413,17744006,1656,0,0,0,0,0,0);	-- Cattleya
INSERT INTO vendor_items VALUES (628,17744006,239,0,0,0,0,0,0);	-- Cinnamon
INSERT INTO vendor_items VALUES (4468,17744006,73,0,0,0,0,0,0);	-- Pamamas
INSERT INTO vendor_items VALUES (721,17744006,147,0,0,0,0,0,0);	-- Rattan Lumber

-- Dohdjuma
INSERT INTO vendor_items VALUES (611,17793041,36,0,0,0,0,0,0);	-- Rye Flour
INSERT INTO vendor_items VALUES (5011,17793041,233,0,0,0,0,0,0);	-- Scroll of Sheepfoe Mambo
INSERT INTO vendor_items VALUES (4150,17793041,2335,0,0,0,0,0,0);	-- Eye Drops
INSERT INTO vendor_items VALUES (4148,17793041,284,0,0,0,0,0,0);	-- Antidote
INSERT INTO vendor_items VALUES (4509,17793041,10,0,0,0,0,0,0);	-- Distilled Water
INSERT INTO vendor_items VALUES (4112,17793041,819,0,0,0,0,0,0);	-- Potion
INSERT INTO vendor_items VALUES (17395,17793041,10,0,0,0,0,0,0);	-- Lugworm
INSERT INTO vendor_items VALUES (4378,17793041,54,0,0,0,0,0,0);	-- Selbina Milk
INSERT INTO vendor_items VALUES (4490,17793041,432,0,0,0,0,0,0);	-- Pickled Herring
INSERT INTO vendor_items VALUES (4559,17793041,4485,0,0,0,0,0,0);	-- Herb Quus

-- Drozga
INSERT INTO vendor_items VALUES (12432,17760405,1493,0,0,0,0,0,0);	-- Faceguard
INSERT INTO vendor_items VALUES (12560,17760405,2296,0,0,0,0,0,0);	-- Scale Mail
INSERT INTO vendor_items VALUES (12688,17760405,1225,0,0,0,0,0,0);	-- Scale Fng. Gnt.
INSERT INTO vendor_items VALUES (12816,17760405,1843,0,0,0,0,0,0);	-- Scale Cuisses
INSERT INTO vendor_items VALUES (12944,17760405,1117,0,0,0,0,0,0);	-- Scale Greaves
INSERT INTO vendor_items VALUES (13192,17760405,437,0,0,0,0,0,0);	-- Leather Belt
INSERT INTO vendor_items VALUES (13327,17760405,1287,0,0,0,0,0,0);	-- Silver Earring
INSERT INTO vendor_items VALUES (13469,17760405,1287,0,0,0,0,0,0);	-- Leather Ring

-- Dwago
INSERT INTO vendor_items VALUES (17395,16982093,9,0,0,0,0,0,0);	-- Lugworm
INSERT INTO vendor_items VALUES (17396,16982093,3,0,0,0,0,0,0);	-- Little worm
INSERT INTO vendor_items VALUES (17016,16982093,11,0,0,0,0,0,0);	-- Pet Food Alpha Biscuit
INSERT INTO vendor_items VALUES (17017,16982093,82,0,0,0,0,0,0);	-- Pet Food Beta Biscuit
INSERT INTO vendor_items VALUES (17862,16982093,98,0,0,0,0,0,0);	-- Jug of Bug Broth

-- Emaliveulaux
INSERT INTO vendor_items VALUES (1523,17735818,290,0,0,0,0,0,0);	-- Apple Mint
INSERT INTO vendor_items VALUES (5164,17735818,1945,0,0,0,0,0,0);	-- Ground Wasabi
INSERT INTO vendor_items VALUES (17005,17735818,99,0,0,0,0,0,0);	-- Lufaise Fly
INSERT INTO vendor_items VALUES (5195,17735818,233,0,0,0,0,0,0);	-- Misareaux Parsley
INSERT INTO vendor_items VALUES (1695,17735818,920,0,0,0,0,0,0);	-- Habanero Peppers

-- Ensasa
INSERT INTO vendor_items VALUES (104,17752097,3881,0,0,1,0,0,1);	-- Tarutaru Folding Screen
INSERT INTO vendor_items VALUES (17336,17752097,5,0,0,2,0,0,0);	-- Crossbow Bolt
INSERT INTO vendor_items VALUES (17318,17752097,3,0,0,2,0,0,0);	-- Wooden Arrow
INSERT INTO vendor_items VALUES (112,17752097,456,0,0,2,0,0,0);	-- Yellow Jar
INSERT INTO vendor_items VALUES (17319,17752097,4,0,0,0,0,0,0);	-- Bone Arrow
INSERT INTO vendor_items VALUES (218,17752097,920,0,0,0,0,0,0);	-- Earthen Flowerpot
INSERT INTO vendor_items VALUES (17396,17752097,3,0,0,0,0,0,0);	-- Little Worm
INSERT INTO vendor_items VALUES (17395,17752097,9,0,0,0,0,0,0);	-- Lugworm
INSERT INTO vendor_items VALUES (1890,17752097,576,0,0,0,0,0,0);	-- River Foliage
INSERT INTO vendor_items VALUES (5065,17752097,283,0,0,0,0,0,0);	-- Earth Threnody
INSERT INTO vendor_items VALUES (5062,17752097,644,0,0,0,0,0,0);	-- Fire Threnody
INSERT INTO vendor_items VALUES (1891,17752097,576,0,0,0,0,0,0);	-- Sea Foliage
INSERT INTO vendor_items VALUES (92,17752097,905,0,0,0,0,0,0);	-- Tarutaru Stool
INSERT INTO vendor_items VALUES (110,17752097,4744,0,0,0,0,0,0);	-- White Jar

-- Eugballion
INSERT INTO vendor_items VALUES (954,17723493,4121,0,0,0,0,0,0);	-- Magic Pot Shard

-- Evelyn
INSERT INTO vendor_items VALUES (1108,17743898,703,0,0,0,0,0,0);	-- Sulfur
INSERT INTO vendor_items VALUES (619,17743898,43,0,0,0,0,0,0);	-- Popoto
INSERT INTO vendor_items VALUES (611,17743898,36,0,0,0,0,0,0);	-- Rye Flour
INSERT INTO vendor_items VALUES (4388,17743898,40,0,0,0,0,0,0);	-- Eggplant

-- Ezura-Romazura
INSERT INTO vendor_items VALUES (4771,17162876,123750,0,0,0,0,0,0);	-- Scroll of Stone V
INSERT INTO vendor_items VALUES (4781,17162876,133110,0,0,0,0,0,0);	-- Scroll of Water V
INSERT INTO vendor_items VALUES (4766,17162876,144875,0,0,0,0,0,0);	-- Scroll of Aero V
INSERT INTO vendor_items VALUES (4756,17162876,162500,0,0,0,0,0,0);	-- Scroll of Fire V
INSERT INTO vendor_items VALUES (4761,17162876,186375,0,0,0,0,0,0);	-- Scroll of Blizzard V
INSERT INTO vendor_items VALUES (4893,17162876,168150,0,0,0,0,0,0);	-- Scroll of Stoneja
INSERT INTO vendor_items VALUES (4895,17162876,176700,0,0,0,0,0,0);	-- Scroll of Waterja
INSERT INTO vendor_items VALUES (4890,17162876,193800,0,0,0,0,0,0);	-- Scroll of Firaja
INSERT INTO vendor_items VALUES (4892,17162876,185240,0,0,0,0,0,0);	-- Scroll of Aeroja
INSERT INTO vendor_items VALUES (4863,17162876,126000,0,0,0,0,0,0);	-- Scroll of Break

-- Falgima
INSERT INTO vendor_items VALUES (4744,17793133,5351,0,0,0,0,0,0);	-- Scroll of Invisible
INSERT INTO vendor_items VALUES (4745,17793133,2325,0,0,0,0,0,0);	-- Scroll of Sneak
INSERT INTO vendor_items VALUES (4746,17793133,1204,0,0,0,0,0,0);	-- Scroll of Deodorize
INSERT INTO vendor_items VALUES (5104,17793133,30360,0,0,0,0,0,0);	-- Scroll of Flurry

-- Faustin
INSERT INTO vendor_items VALUES (639,17735742,110,0,0,0,0,0,0);	-- Chestnut
INSERT INTO vendor_items VALUES (4389,17735742,29,0,0,0,0,0,0);	-- San d'Orian Carrot
INSERT INTO vendor_items VALUES (610,17735742,55,0,0,0,0,0,0);	-- San d'Orian Flour
INSERT INTO vendor_items VALUES (4431,17735742,69,0,0,0,0,0,0);	-- San d'Orian Grape

-- Fayeewah
INSERT INTO vendor_items VALUES (5570,16982099,68,0,0,0,0,0,0);	-- Cup of Chai
INSERT INTO vendor_items VALUES (5572,16982099,2075,0,0,0,0,0,0);	-- Irmik Helvasi

-- Ferdoulemiont
INSERT INTO vendor_items VALUES (845,17719337,1125,1,0,0,1,0,0);	-- Black Chocobo Feather
INSERT INTO vendor_items VALUES (17307,17719337,9,2,0,0,0,0,0);	-- Dart
INSERT INTO vendor_items VALUES (17862,17719337,680,0,0,0,0,0,0);	-- Bug Broth
INSERT INTO vendor_items VALUES (17866,17719337,680,0,0,0,0,0,0);	-- Carrion Broth
INSERT INTO vendor_items VALUES (17860,17719337,81,0,0,0,0,0,0);	-- Carrot Broth
INSERT INTO vendor_items VALUES (17864,17719337,124,0,0,0,0,0,0);	-- Herbal Broth
INSERT INTO vendor_items VALUES (840,17719337,7,0,0,0,0,0,0);	-- Chocobo Feather
INSERT INTO vendor_items VALUES (4545,17719337,61,0,0,0,0,0,0);	-- Gysahl Greens
INSERT INTO vendor_items VALUES (17016,17719337,10,0,0,0,0,0,0);	-- Pet Food Alpha Biscuit
INSERT INTO vendor_items VALUES (17017,17719337,81,0,0,0,0,0,0);	-- Pet Food Beta Biscuit
INSERT INTO vendor_items VALUES (5073,17719337,49680,0,0,0,0,0,0);	-- Scroll of Chocobo Mazurka
INSERT INTO vendor_items VALUES (4997,17719337,16,0,0,0,0,0,0);	-- Scroll of Knight's Minne
INSERT INTO vendor_items VALUES (4998,17719337,864,0,0,0,0,0,0);	-- Scroll of Knight's Minne II
INSERT INTO vendor_items VALUES (4999,17719337,5148,0,0,0,0,0,0);	-- Scroll of Knight's Minne III
INSERT INTO vendor_items VALUES (2343,17719337,1984,0,0,0,0,0,0);	-- La Theine Millet

-- Fiva
INSERT INTO vendor_items VALUES (4503,17727524,184,0,0,0,0,0,0);	-- Buburimu Grape
INSERT INTO vendor_items VALUES (1120,17727524,1620,0,0,0,0,0,0);	-- Casablanca
INSERT INTO vendor_items VALUES (4359,17727524,220,0,0,0,0,0,0);	-- Dhalmel Meat
INSERT INTO vendor_items VALUES (614,17727524,72,0,0,0,0,0,0);	-- Mhaura Garlic
INSERT INTO vendor_items VALUES (4445,17727524,40,0,0,0,0,0,0);	-- Yagudo Cherry

-- Fomina
INSERT INTO vendor_items VALUES (612,17752105,55,0,0,0,0,0,0);	-- Kazham Peppers
INSERT INTO vendor_items VALUES (4432,17752105,55,0,0,0,0,0,0);	-- Kazham Pineapple
INSERT INTO vendor_items VALUES (4390,17752105,36,0,0,0,0,0,0);	-- Mithran Tomato
INSERT INTO vendor_items VALUES (626,17752105,234,0,0,0,0,0,0);	-- Black Pepper
INSERT INTO vendor_items VALUES (630,17752105,88,0,0,0,0,0,0);	-- Ogre Pumpkin
INSERT INTO vendor_items VALUES (632,17752105,110,0,0,0,0,0,0);	-- Kukuru Bean
INSERT INTO vendor_items VALUES (1411,17752105,1656,0,0,0,0,0,0);	-- Phalaenopsis

-- Galdeo
INSERT INTO vendor_items VALUES (623,17735746,119,0,0,0,0,0,0);	-- Bay Leaves
INSERT INTO vendor_items VALUES (4154,17735746,6440,0,0,0,0,0,0);	-- Holy Water

-- Galvin
INSERT INTO vendor_items VALUES (4128,17743906,4445,0,1,0,0,1,0);	-- Ether
INSERT INTO vendor_items VALUES (4151,17743906,736,0,2,0,0,0,0);	-- Echo Drops
INSERT INTO vendor_items VALUES (4112,17743906,837,0,2,0,0,0,0);	-- Potion
INSERT INTO vendor_items VALUES (17318,17743906,3,0,2,0,0,0,0);	-- Wooden Arrow
INSERT INTO vendor_items VALUES (4150,17743906,2387,0,0,0,0,0,0);	-- Eye Drops
INSERT INTO vendor_items VALUES (4148,17743906,290,0,0,0,0,0,0);	-- Antidote
INSERT INTO vendor_items VALUES (17320,17743906,7,0,0,0,0,0,0);	-- Iron Arrow
INSERT INTO vendor_items VALUES (17336,17743906,5,0,0,0,0,0,0);	-- Crossbow Bolt

-- Gavrie
INSERT INTO vendor_items VALUES (4150,16982088,2595,0,0,0,0,0,0);	-- Eye Drops
INSERT INTO vendor_items VALUES (4148,16982088,316,0,0,0,0,0,0);	-- Antidote
INSERT INTO vendor_items VALUES (4151,16982088,800,0,0,0,0,0,0);	-- Echo Drops
INSERT INTO vendor_items VALUES (4112,16982088,910,0,0,0,0,0,0);	-- Potion
INSERT INTO vendor_items VALUES (4128,16982088,4832,0,0,0,0,0,0);	-- Ether
INSERT INTO vendor_items VALUES (4155,16982088,3360,0,0,0,0,0,0);	-- Remedy
INSERT INTO vendor_items VALUES (4509,16982088,12,0,0,0,0,0,0);	-- Distilled Water
INSERT INTO vendor_items VALUES (18731,16982088,50,0,0,0,0,0,0);	-- Automaton Oil
INSERT INTO vendor_items VALUES (18732,16982088,250,0,0,0,0,0,0);	-- Automaton Oil +1
INSERT INTO vendor_items VALUES (18733,16982088,500,0,0,0,0,0,0);	-- Automaton Oil +2
INSERT INTO vendor_items VALUES (19185,16982088,1000,0,0,0,0,0,0);	-- Automaton Oil +3

-- Gekko
INSERT INTO vendor_items VALUES (4150,17784834,2387,0,0,0,0,0,0);	-- Eye Drops
INSERT INTO vendor_items VALUES (4148,17784834,290,0,0,0,0,0,0);	-- Antidote
INSERT INTO vendor_items VALUES (4151,17784834,720,0,0,0,0,0,0);	-- Echo Drops
INSERT INTO vendor_items VALUES (4112,17784834,837,0,0,0,0,0,0);	-- Potion
INSERT INTO vendor_items VALUES (4128,17784834,4445,0,0,0,0,0,0);	-- Ether
INSERT INTO vendor_items VALUES (4365,17784834,120,0,0,0,0,0,0);	-- Rolanberry
INSERT INTO vendor_items VALUES (189,17784834,36000,0,0,0,0,0,0);	-- Autumn's End
INSERT INTO vendor_items VALUES (188,17784834,31224,0,0,0,0,0,0);	-- Acolyte's Grief

-- Gelzerio
INSERT INTO vendor_items VALUES (13198,17735725,19602,0,0,0,0,0,0);	-- Swordbelt
INSERT INTO vendor_items VALUES (17389,17735725,486,0,1,0,0,1,0);	-- Bamboo Fishing Rod
INSERT INTO vendor_items VALUES (17396,17735725,3,0,2,0,0,0,0);	-- Little Worm
INSERT INTO vendor_items VALUES (17390,17735725,212,0,2,0,0,0,0);	-- Yew Fishing Rod
INSERT INTO vendor_items VALUES (13196,17735725,10054,0,0,0,0,0,0);	-- Silver Belt
INSERT INTO vendor_items VALUES (17395,17735725,10,0,0,0,0,0,0);	-- Lugworm
INSERT INTO vendor_items VALUES (17391,17735725,64,0,0,0,0,0,0);	-- Willow Fishing Rod
INSERT INTO vendor_items VALUES (12600,17735725,216,0,0,0,0,0,0);	-- Robe
INSERT INTO vendor_items VALUES (12728,17735725,118,0,0,0,0,0,0);	-- Cuffs
INSERT INTO vendor_items VALUES (12856,17735725,172,0,0,0,0,0,0);	-- Slops
INSERT INTO vendor_items VALUES (12984,17735725,111,0,0,0,0,0,0);	-- Ash Clogs
INSERT INTO vendor_items VALUES (12464,17735725,1742,0,0,0,0,0,0);	-- Headgear
INSERT INTO vendor_items VALUES (12592,17735725,2470,0,0,0,0,0,0);	-- Doublet
INSERT INTO vendor_items VALUES (12720,17735725,1363,0,0,0,0,0,0);	-- Gloves
INSERT INTO vendor_items VALUES (12848,17735725,1899,0,0,0,0,0,0);	-- Brais
INSERT INTO vendor_items VALUES (12976,17735725,1269,0,0,0,0,0,0);	-- Gaiters

-- Generoit
INSERT INTO vendor_items VALUES (4545,17788984,61,0,0,0,0,0,0);	-- Gysahl Greens
INSERT INTO vendor_items VALUES (840,17788984,7,0,0,0,0,0,0);	-- Chocobo Feather
INSERT INTO vendor_items VALUES (17016,17788984,10,0,0,0,0,0,0);	-- Pet Food Alpha Biscuit
INSERT INTO vendor_items VALUES (17017,17788984,81,0,0,0,0,0,0);	-- Pet Food Beta Biscuit
INSERT INTO vendor_items VALUES (17860,17788984,81,0,0,0,0,0,0);	-- Carrot Broth
INSERT INTO vendor_items VALUES (17862,17788984,687,0,0,0,0,0,0);	-- Bug Broth
INSERT INTO vendor_items VALUES (17864,17788984,125,0,0,0,0,0,0);	-- Herbal Broth
INSERT INTO vendor_items VALUES (17866,17788984,687,0,0,0,0,0,0);	-- Carrion Broth
INSERT INTO vendor_items VALUES (5073,17788984,50784,0,0,0,0,0,0);	-- Scroll of Chocobo Mazurka

-- Ghebi Damomohe
INSERT INTO vendor_items VALUES (4405,17780742,144,0,0,0,0,0,0);	-- Rice Ball
INSERT INTO vendor_items VALUES (4457,17780742,2700,0,0,0,0,0,0);	-- Eel Kabob
INSERT INTO vendor_items VALUES (4467,17780742,3,0,0,0,0,0,0);	-- Garlic Cracker

-- Ghemi Sinterilo
INSERT INTO vendor_items VALUES (4468,17801253,72,0,0,0,0,0,0);	-- Pamamas
INSERT INTO vendor_items VALUES (4432,17801253,54,0,0,0,0,0,0);	-- Kazham Pineapple
INSERT INTO vendor_items VALUES (4390,17801253,36,0,0,0,0,0,0);	-- Mithran Tomato
INSERT INTO vendor_items VALUES (612,17801253,54,0,0,0,0,0,0);	-- Kazham Peppers
INSERT INTO vendor_items VALUES (628,17801253,236,0,0,0,0,0,0);	-- Cinnamon
INSERT INTO vendor_items VALUES (632,17801253,109,0,0,0,0,0,0);	-- Kukuru Bean
INSERT INTO vendor_items VALUES (5187,17801253,156,0,0,0,0,0,0);	-- Elshimo Coconut
INSERT INTO vendor_items VALUES (5604,17801253,154,0,0,0,0,0,0);	-- Elshimo Pachira Fruit
INSERT INTO vendor_items VALUES (2869,17801253,9100,0,0,0,0,0,0);	-- Kazham Waystone
INSERT INTO vendor_items VALUES (731,17801253,2877,0,0,0,0,0,0);	-- Aquilaria Log

-- Glyke
INSERT INTO vendor_items VALUES (4499,17776677,92,0,0,0,0,0,0);	-- Iron Bread
INSERT INTO vendor_items VALUES (4408,17776677,128,0,0,0,0,0,0);	-- Tortilla
INSERT INTO vendor_items VALUES (4356,17776677,184,0,0,0,0,0,0);	-- White Bread
INSERT INTO vendor_items VALUES (4416,17776677,1400,0,0,0,0,0,0);	-- Pea Soup
INSERT INTO vendor_items VALUES (4456,17776677,2070,0,0,0,0,0,0);	-- Boiled Crab
INSERT INTO vendor_items VALUES (4437,17776677,662,0,0,0,0,0,0);	-- Roast Mutton
INSERT INTO vendor_items VALUES (4406,17776677,440,0,0,0,0,0,0);	-- Baked Apple
INSERT INTO vendor_items VALUES (4555,17776677,1711,0,0,0,0,0,0);	-- Windurst Salad
INSERT INTO vendor_items VALUES (4559,17776677,4585,0,0,0,0,0,0);	-- Herb Quus
INSERT INTO vendor_items VALUES (4422,17776677,184,0,0,0,0,0,0);	-- Orange Juice
INSERT INTO vendor_items VALUES (4423,17776677,276,0,0,0,0,0,0);	-- Apple Juice
INSERT INTO vendor_items VALUES (4442,17776677,368,0,0,0,0,0,0);	-- Pineapple Juice
INSERT INTO vendor_items VALUES (4424,17776677,1012,0,0,0,0,0,0);	-- Mellon Juice
INSERT INTO vendor_items VALUES (4441,17776677,855,0,0,0,0,0,0);	-- Grape Juice

-- Graine
INSERT INTO vendor_items VALUES (12440,17797130,457,0,0,0,0,0,0);	-- Leather Bandana
INSERT INTO vendor_items VALUES (12448,17797130,174,0,0,0,0,0,0);	-- Bronze Cap
INSERT INTO vendor_items VALUES (12449,17797130,1700,0,0,0,0,0,0);	-- Brass Cap
INSERT INTO vendor_items VALUES (12568,17797130,698,0,0,0,0,0,0);	-- Leather Vest
INSERT INTO vendor_items VALUES (12576,17797130,235,0,0,0,0,0,0);	-- Bronze Harness
INSERT INTO vendor_items VALUES (12577,17797130,2286,0,0,0,0,0,0);	-- Brass Harness
INSERT INTO vendor_items VALUES (12696,17797130,374,0,0,0,0,0,0);	-- Leather Gloves
INSERT INTO vendor_items VALUES (12704,17797130,128,0,0,0,0,0,0);	-- Bronze Mittens
INSERT INTO vendor_items VALUES (12705,17797130,1255,0,0,0,0,0,0);	-- Brass Mittens
INSERT INTO vendor_items VALUES (12824,17797130,557,0,0,0,0,0,0);	-- Leather Trousesrs
INSERT INTO vendor_items VALUES (12832,17797130,191,0,0,0,0,0,0);	-- Bronze Subligar
INSERT INTO vendor_items VALUES (12833,17797130,1840,0,0,0,0,0,0);	-- Brass Subligar
INSERT INTO vendor_items VALUES (12952,17797130,349,0,0,0,0,0,0);	-- Leather Highboots
INSERT INTO vendor_items VALUES (12960,17797130,117,0,0,0,0,0,0);	-- Bronze Leggings
INSERT INTO vendor_items VALUES (12961,17797130,1140,0,0,0,0,0,0);	-- Brass Leggings

-- Griselda
INSERT INTO vendor_items VALUES (4442,17735726,360,0,1,0,0,1,0);	-- Pineapple Juice
INSERT INTO vendor_items VALUES (4391,17735726,21,0,2,0,0,0,0);	-- Bretzel
INSERT INTO vendor_items VALUES (4490,17735726,432,0,2,0,0,0,0);	-- Pickled Herring
INSERT INTO vendor_items VALUES (4424,17735726,990,0,2,0,0,0,0);	-- Melon Juice
INSERT INTO vendor_items VALUES (4499,17735726,90,0,0,0,0,0,0);	-- Iron Bread
INSERT INTO vendor_items VALUES (4376,17735726,108,0,0,0,0,0,0);	-- Meat Jerky
INSERT INTO vendor_items VALUES (4509,17735726,10,0,0,0,0,0,0);	-- Distilled Water

-- Guruna-Maguruna
INSERT INTO vendor_items VALUES (13090,17760315,4714,0,0,0,0,0,0);	-- Beetle Gorget
INSERT INTO vendor_items VALUES (12601,17760315,2776,0,0,0,0,0,0);	-- Linen Robe
INSERT INTO vendor_items VALUES (12729,17760315,1570,0,0,0,0,0,0);	-- Linen Cuffs
INSERT INTO vendor_items VALUES (12608,17760315,1260,0,0,0,0,0,0);	-- Tunic
INSERT INTO vendor_items VALUES (12593,17760315,12355,0,0,2,0,0,0);	-- Cotton Doublet
INSERT INTO vendor_items VALUES (12696,17760315,324,0,0,0,0,0,0);	-- Leather Gloves
INSERT INTO vendor_items VALUES (12736,17760315,589,0,0,0,0,0,0);	-- Mitts
INSERT INTO vendor_items VALUES (12721,17760315,6696,0,0,2,0,0,0);	-- Cotton Gloves
INSERT INTO vendor_items VALUES (13085,17760315,972,0,0,0,0,0,0);	-- Hemp Gorget
INSERT INTO vendor_items VALUES (12592,17760315,2470,0,0,0,0,0,0);	-- Doublet
INSERT INTO vendor_items VALUES (12600,17760315,216,0,0,0,0,0,0);	-- Robe
INSERT INTO vendor_items VALUES (12568,17760315,604,0,0,0,0,0,0);	-- Leather Vest
INSERT INTO vendor_items VALUES (12720,17760315,1363,0,0,0,0,0,0);	-- Gloves
INSERT INTO vendor_items VALUES (12728,17760315,118,0,0,0,0,0,0);	-- Cuffs

-- Hagakoff
INSERT INTO vendor_items VALUES (16399,16982096,15448,0,0,0,0,0,0);	-- Katars (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (16400,16982096,67760,0,0,0,0,0,0);	-- Darksteel Katars
INSERT INTO vendor_items VALUES (16419,16982096,45760,0,0,0,0,0,0);	-- Patas (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (16448,16982096,156,0,0,0,0,0,0);	-- Bronze Dagger
INSERT INTO vendor_items VALUES (16450,16982096,2030,0,0,0,0,0,0);	-- Dagger
INSERT INTO vendor_items VALUES (16551,16982096,776,0,0,0,0,0,0);	-- Sapara
INSERT INTO vendor_items VALUES (16552,16982096,4525,0,0,0,0,0,0);	-- Scimitar
INSERT INTO vendor_items VALUES (16553,16982096,38800,0,0,0,0,0,0);	-- Tulwar (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (16657,16982096,6600,0,0,0,0,0,0);	-- Tabar
INSERT INTO vendor_items VALUES (16658,16982096,124305,0,0,0,0,0,0);	-- Darksteel Tabar (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (16704,16982096,672,0,0,0,0,0,0);	-- Butterfly Axe
INSERT INTO vendor_items VALUES (16705,16982096,4550,0,0,0,0,0,0);	-- Greataxe (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (16768,16982096,344,0,0,0,0,0,0);	-- Bronze Zaghnal
INSERT INTO vendor_items VALUES (16770,16982096,12540,0,0,0,0,0,0);	-- Zaghnal (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (17024,16982096,72,0,0,0,0,0,0);	-- Ash Club
INSERT INTO vendor_items VALUES (17025,16982096,1740,0,0,0,0,0,0);	-- Chestnut Club (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (18259,16982096,238,0,0,0,0,0,0);	-- Angon

-- Harmodios
INSERT INTO vendor_items VALUES (17347,17739808,990,0,1,0,0,1,0);	-- Piccolo
INSERT INTO vendor_items VALUES (17344,17739808,219,0,2,0,0,0,0);	-- Cornette
INSERT INTO vendor_items VALUES (17353,17739808,43,0,2,0,0,0,0);	-- Maple Harp
INSERT INTO vendor_items VALUES (5041,17739808,69120,0,2,0,0,0,0);	-- Scroll of Vital Etude
INSERT INTO vendor_items VALUES (5042,17739808,66240,0,2,0,0,0,0);	-- Scroll of Swift Etude
INSERT INTO vendor_items VALUES (5043,17739808,63360,0,2,0,0,0,0);	-- Scroll of Sage Etude
INSERT INTO vendor_items VALUES (5044,17739808,56700,0,2,0,0,0,0);	-- Scroll of Logical Etude
INSERT INTO vendor_items VALUES (5039,17739808,79560,0,2,0,0,0,0);	-- Scroll of Herculean Etude
INSERT INTO vendor_items VALUES (5040,17739808,76500,0,2,0,0,0,0);	-- Scroll of Uncanny Etude
INSERT INTO vendor_items VALUES (17351,17739808,4644,0,0,0,0,0,0);	-- Gemshorn
INSERT INTO vendor_items VALUES (17345,17739808,43,0,0,0,0,0,0);	-- Flute
INSERT INTO vendor_items VALUES (5045,17739808,54000,0,0,0,0,0,0);	-- Scroll of Bewitching Etude

-- Hasim
INSERT INTO vendor_items VALUES (4668,17780866,1760,0,0,0,0,0,0);	-- Scroll of Barfire
INSERT INTO vendor_items VALUES (4669,17780866,3624,0,0,0,0,0,0);	-- Scroll of Barblizzard
INSERT INTO vendor_items VALUES (4670,17780866,930,0,0,0,0,0,0);	-- Scroll of Baraero
INSERT INTO vendor_items VALUES (4671,17780866,156,0,0,0,0,0,0);	-- Scroll of Barstone
INSERT INTO vendor_items VALUES (4672,17780866,5754,0,0,0,0,0,0);	-- Scroll of Barthunder
INSERT INTO vendor_items VALUES (4673,17780866,360,0,0,0,0,0,0);	-- Scroll of Barwater
INSERT INTO vendor_items VALUES (4674,17780866,1760,0,0,0,0,0,0);	-- Scroll of Barfira
INSERT INTO vendor_items VALUES (4675,17780866,3624,0,0,0,0,0,0);	-- Scroll of Barblizzara
INSERT INTO vendor_items VALUES (4676,17780866,930,0,0,0,0,0,0);	-- Scroll of Baraera
INSERT INTO vendor_items VALUES (4677,17780866,156,0,0,0,0,0,0);	-- Scroll of Barstonra
INSERT INTO vendor_items VALUES (4678,17780866,5754,0,0,0,0,0,0);	-- Scroll of Barthundra
INSERT INTO vendor_items VALUES (4679,17780866,360,0,0,0,0,0,0);	-- Scroll of Barwatera
INSERT INTO vendor_items VALUES (4680,17780866,244,0,0,0,0,0,0);	-- Scroll of Barsleep
INSERT INTO vendor_items VALUES (4612,17780866,23400,0,0,0,0,0,0);	-- Scroll of Cure IV
INSERT INTO vendor_items VALUES (4616,17780866,11200,0,0,0,0,0,0);	-- Scroll of Curaga II
INSERT INTO vendor_items VALUES (4617,17780866,19932,0,0,0,0,0,0);	-- Scroll of Curaga III
INSERT INTO vendor_items VALUES (4653,17780866,32000,0,0,0,0,0,0);	-- Scroll of Protect III

-- Herminia
INSERT INTO vendor_items VALUES (12456,17793033,552,0,0,0,0,0,0);	-- Hachimaki
INSERT INTO vendor_items VALUES (12584,17793033,833,0,0,0,0,0,0);	-- Kenpogi
INSERT INTO vendor_items VALUES (12608,17793033,1274,0,0,0,0,0,0);	-- Tunic
INSERT INTO vendor_items VALUES (12712,17793033,458,0,0,0,0,0,0);	-- Tekko
INSERT INTO vendor_items VALUES (12736,17793033,596,0,0,0,0,0,0);	-- Mitts
INSERT INTO vendor_items VALUES (12840,17793033,666,0,0,0,0,0,0);	-- Sitabaki
INSERT INTO vendor_items VALUES (12968,17793033,424,0,0,0,0,0,0);	-- Kyahan
INSERT INTO vendor_items VALUES (12992,17793033,544,0,0,0,0,0,0);	-- Solea

-- Hilkomu-Makimu
INSERT INTO vendor_items VALUES (4829,17752096,23184,0,0,1,0,0,1);	-- Scroll of Poison II
INSERT INTO vendor_items VALUES (4839,17752096,12880,0,0,1,0,0,1);	-- Scroll of Bio II
INSERT INTO vendor_items VALUES (4833,17752096,4747,0,0,1,0,0,1);	-- Scroll of Poisonga
INSERT INTO vendor_items VALUES (4797,17752096,1191,0,0,2,0,0,0);	-- Scroll of Stonega
INSERT INTO vendor_items VALUES (4807,17752096,2143,0,0,2,0,0,0);	-- Scroll of Waterga
INSERT INTO vendor_items VALUES (4792,17752096,4239,0,0,2,0,0,0);	-- Scroll of Aeroga
INSERT INTO vendor_items VALUES (4782,17752096,7181,0,0,2,0,0,0);	-- Scroll of Firaga
INSERT INTO vendor_items VALUES (4787,17752096,10948,0,0,2,0,0,0);	-- Scroll of Blizzaga
INSERT INTO vendor_items VALUES (4802,17752096,15456,0,0,2,0,0,0);	-- Scroll of Thundaga
INSERT INTO vendor_items VALUES (4859,17752096,8280,0,0,2,0,0,0);	-- Scroll of Shock Spikes
INSERT INTO vendor_items VALUES (4768,17752096,5814,0,0,0,0,0,0);	-- Scroll of Stone II
INSERT INTO vendor_items VALUES (4778,17752096,8100,0,0,0,0,0,0);	-- Scroll of Water II
INSERT INTO vendor_items VALUES (4763,17752096,12236,0,0,0,0,0,0);	-- Scroll of Aero II
INSERT INTO vendor_items VALUES (4753,17752096,16928,0,0,0,0,0,0);	-- Scroll of Fire II
INSERT INTO vendor_items VALUES (4758,17752096,22356,0,0,0,0,0,0);	-- Scroll of Blizzard II
INSERT INTO vendor_items VALUES (4773,17752096,28520,0,0,0,0,0,0);	-- Scroll of Thunder II

-- Hohbiba-Mubiba
INSERT INTO vendor_items VALUES (17051,17760313,1440,0,0,1,0,0,1);	-- Yew Wand
INSERT INTO vendor_items VALUES (17090,17760313,3642,0,0,1,0,0,1);	-- Elm Staff
INSERT INTO vendor_items VALUES (17097,17760313,18422,0,0,1,0,0,1);	-- Elm Pole
INSERT INTO vendor_items VALUES (17059,17760313,91,0,0,0,0,0,0);	-- Bronze Rod
INSERT INTO vendor_items VALUES (17050,17760313,340,0,0,0,0,0,0);	-- Willow Wand
INSERT INTO vendor_items VALUES (17026,17760313,4945,0,0,2,0,0,0);	-- Bone Cudgel
INSERT INTO vendor_items VALUES (17089,17760313,584,0,0,0,0,0,0);	-- Holly Staff
INSERT INTO vendor_items VALUES (17096,17760313,4669,0,0,2,0,0,0);	-- Holly Pole
INSERT INTO vendor_items VALUES (17049,17760313,47,0,0,0,0,0,0);	-- Maple Wand
INSERT INTO vendor_items VALUES (17024,17760313,66,0,0,0,0,0,0);	-- Ash Club
INSERT INTO vendor_items VALUES (17025,17760313,1600,0,0,0,0,0,0);	-- Chestnut Club
INSERT INTO vendor_items VALUES (17088,17760313,58,0,0,0,0,0,0);	-- Ash Staff
INSERT INTO vendor_items VALUES (17095,17760313,386,0,0,0,0,0,0);	-- Ash Pole
INSERT INTO vendor_items VALUES (16448,17760313,140,0,0,0,0,0,0);	-- Bronze Dagger

-- Hortense
INSERT INTO vendor_items VALUES (4976,17739812,64,0,0,0,0,0,0);	-- Scroll of Foe Requiem
INSERT INTO vendor_items VALUES (4977,17739812,441,0,0,0,0,0,0);	-- Scroll of Foe Requiem II
INSERT INTO vendor_items VALUES (4978,17739812,3960,0,0,0,0,0,0);	-- Scroll of Foe Requiem III
INSERT INTO vendor_items VALUES (4979,17739812,6912,0,0,0,0,0,0);	-- Scroll of Foe Requiem IV
INSERT INTO vendor_items VALUES (4986,17739812,37,0,0,0,0,0,0);	-- Scroll of Army's Paeon
INSERT INTO vendor_items VALUES (4987,17739812,321,0,0,0,0,0,0);	-- Scroll of Army's Paeon II
INSERT INTO vendor_items VALUES (4988,17739812,3240,0,0,0,0,0,0);	-- Scroll of Army's Paeon III
INSERT INTO vendor_items VALUES (4989,17739812,5940,0,0,0,0,0,0);	-- Scroll of Army's Paeon IV
INSERT INTO vendor_items VALUES (5002,17739812,21,0,0,0,0,0,0);	-- Scroll of Valor Minuet
INSERT INTO vendor_items VALUES (5003,17739812,1101,0,0,0,0,0,0);	-- Scroll of Valor Minuet II
INSERT INTO vendor_items VALUES (5004,17739812,5544,0,0,0,0,0,0);	-- Scroll of Valor Minuet III

-- Ilita
INSERT INTO vendor_items VALUES (512,17743974,6000,0,0,0,0,0,0);	-- Linkshell
INSERT INTO vendor_items VALUES (16285,17743974,375,0,0,0,0,0,0);	-- Pendant Compass

-- Jajaroon
INSERT INTO vendor_items VALUES (2176,16994341,48,0,0,0,0,0,0);	-- Fire Card
INSERT INTO vendor_items VALUES (2177,16994341,48,0,0,0,0,0,0);	-- Ice Card
INSERT INTO vendor_items VALUES (2178,16994341,48,0,0,0,0,0,0);	-- Wind Card
INSERT INTO vendor_items VALUES (2179,16994341,48,0,0,0,0,0,0);	-- Earth Card
INSERT INTO vendor_items VALUES (2180,16994341,48,0,0,0,0,0,0);	-- Thunder Card
INSERT INTO vendor_items VALUES (2181,16994341,48,0,0,0,0,0,0);	-- Water Card
INSERT INTO vendor_items VALUES (2182,16994341,48,0,0,0,0,0,0);	-- Light Card
INSERT INTO vendor_items VALUES (2183,16994341,48,0,0,0,0,0,0);	-- Dark Card
INSERT INTO vendor_items VALUES (5870,16994341,10000,0,0,0,0,0,0);	-- Trump Card Case
INSERT INTO vendor_items VALUES (5488,16994341,35200,0,0,0,0,0,0);	-- Samurai Die
INSERT INTO vendor_items VALUES (5489,16994341,600,0,0,0,0,0,0);	-- Ninja Die
INSERT INTO vendor_items VALUES (5490,16994341,9216,0,0,0,0,0,0);	-- Dragoon Die
INSERT INTO vendor_items VALUES (5491,16994341,40000,0,0,0,0,0,0);	-- Summoner Die
INSERT INTO vendor_items VALUES (5492,16994341,3525,0,0,0,0,0,0);	-- Blue Mage Die
INSERT INTO vendor_items VALUES (5493,16994341,316,0,0,0,0,0,0);	-- Corsair Die
INSERT INTO vendor_items VALUES (5494,16994341,82500,0,0,0,0,0,0);	-- Puppetmaster Die

-- Jourille
INSERT INTO vendor_items VALUES (639,17752107,110,0,0,0,0,0,0);	-- Chestnut
INSERT INTO vendor_items VALUES (4389,17752107,29,0,0,0,0,0,0);	-- San d'Orian Carrot
INSERT INTO vendor_items VALUES (610,17752107,55,0,0,0,0,0,0);	-- San d'Orian Flour
INSERT INTO vendor_items VALUES (4431,17752107,69,0,0,0,0,0,0);	-- San d'Orian Grape

-- Justi
INSERT INTO vendor_items VALUES (32,17723485,170726,1,0,0,1,0,0);	-- Dresser
INSERT INTO vendor_items VALUES (55,17723485,69888,1,0,0,1,0,0);	-- Cabinet
INSERT INTO vendor_items VALUES (59,17723485,57333,1,0,0,1,0,0);	-- Chiffonier
INSERT INTO vendor_items VALUES (49,17723485,35272,2,0,0,0,0,0);	-- Coffer
INSERT INTO vendor_items VALUES (1657,17723485,92,0,0,0,0,0,0);	-- Bundling Twine
INSERT INTO vendor_items VALUES (93,17723485,518,0,0,0,0,0,0);	-- Water Cask
INSERT INTO vendor_items VALUES (57,17723485,15881,0,0,0,0,0,0);	-- Cupboard
INSERT INTO vendor_items VALUES (24,17723485,129168,0,0,0,0,0,0);	-- Oak Table
INSERT INTO vendor_items VALUES (46,17723485,8376,0,0,0,0,0,0);	-- Armor Box

-- Kahah Hobichai
INSERT INTO vendor_items VALUES (90,16974279,200,0,0,0,0,0,0);	-- Rusty Bucket
INSERT INTO vendor_items VALUES (605,16974279,200,0,0,0,0,0,0);	-- Pickaxe (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (1020,16974279,300,0,0,0,0,0,0);	-- Sickle (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (1021,16974279,500,0,0,0,0,0,0);	-- Hatchet (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (16465,16974279,164,0,0,0,0,0,0);	-- Bronze Knife
INSERT INTO vendor_items VALUES (16466,16974279,2425,0,0,0,0,0,0);	-- Knife

-- Khaf Jhifanm
INSERT INTO vendor_items VALUES (5567,16982095,200,0,0,0,0,0,0);	-- Dried Date
INSERT INTO vendor_items VALUES (5576,16982095,800,0,0,0,0,0,0);	-- Ayran
INSERT INTO vendor_items VALUES (5590,16982095,3750,0,0,0,0,0,0);	-- Balik Sandvici
INSERT INTO vendor_items VALUES (2235,16982095,320,0,0,0,0,0,0);	-- Wildgrass Seeds
INSERT INTO vendor_items VALUES (5075,16982095,4400,0,0,0,0,0,0);	-- Scroll of Raptor Mazurka
INSERT INTO vendor_items VALUES (2872,16982095,10000,0,0,0,0,0,0);	-- Empire Waystone

-- Khel Pahlhama
INSERT INTO vendor_items VALUES (512,17760323,8000,0,0,0,0,0,0);	-- Linkshell
INSERT INTO vendor_items VALUES (16285,17760323,375,0,0,0,0,0,0);	-- Pendant Compass

-- Khe Chalahko
INSERT INTO vendor_items VALUES (12416,17776716,29311,0,0,0,0,0,0);	-- Sallet
INSERT INTO vendor_items VALUES (12544,17776716,45208,0,0,0,0,0,0);	-- Breastplate
INSERT INTO vendor_items VALUES (12800,17776716,34776,0,0,0,0,0,0);	-- Cuisses
INSERT INTO vendor_items VALUES (12928,17776716,21859,0,0,0,0,0,0);	-- Plate Leggins
INSERT INTO vendor_items VALUES (12810,17776716,53130,0,0,0,0,0,0);	-- Breeches
INSERT INTO vendor_items VALUES (12938,17776716,32637,0,0,0,0,0,0);	-- Sollerets

-- Khifo Ryuhkowa
INSERT INTO vendor_items VALUES (16473,17801256,5713,0,0,0,0,0,0);	-- Kukri
INSERT INTO vendor_items VALUES (16595,17801256,153014,0,0,0,0,0,0);	-- Ram-Dao
INSERT INTO vendor_items VALUES (16833,17801256,809,0,0,0,0,0,0);	-- Bronze Spear
INSERT INTO vendor_items VALUES (16835,17801256,16228,0,0,0,0,0,0);	-- Spear
INSERT INTO vendor_items VALUES (16839,17801256,75541,0,0,0,0,0,0);	-- Partisan
INSERT INTO vendor_items VALUES (17025,17801256,1600,0,0,0,0,0,0);	-- Chestnut Club
INSERT INTO vendor_items VALUES (17026,17801256,4945,0,0,0,0,0,0);	-- Bone Cudgel
INSERT INTO vendor_items VALUES (17052,17801256,5255,0,0,0,0,0,0);	-- Chestnut Wand
INSERT INTO vendor_items VALUES (17092,17801256,29752,0,0,0,0,0,0);	-- Mahogany Staff
INSERT INTO vendor_items VALUES (17099,17801256,99176,0,0,0,0,0,0);	-- Mahogany Pole
INSERT INTO vendor_items VALUES (17163,17801256,39744,0,0,0,0,0,0);	-- Battle Bow
INSERT INTO vendor_items VALUES (17308,17801256,55,0,0,0,0,0,0);	-- Hawkeye
INSERT INTO vendor_items VALUES (17280,17801256,1610,0,0,0,0,0,0);	-- Boomerang
INSERT INTO vendor_items VALUES (17318,17801256,3,0,0,0,0,0,0);	-- Woden Arrow

-- Kindlix
INSERT INTO vendor_items VALUES (4250,17784984,22,0,0,0,0,0,0);	-- Crackler
INSERT INTO vendor_items VALUES (4167,17784984,25,0,0,0,0,0,0);	-- Cracker
INSERT INTO vendor_items VALUES (4168,17784984,25,0,0,0,0,0,0);	-- Twinkle Shower
INSERT INTO vendor_items VALUES (4169,17784984,25,0,0,0,0,0,0);	-- Little Comet
INSERT INTO vendor_items VALUES (4217,17784984,25,0,0,0,0,0,0);	-- Sparkling Hand
INSERT INTO vendor_items VALUES (4215,17784984,50,0,0,0,0,0,0);	-- Popstar
INSERT INTO vendor_items VALUES (4216,17784984,50,0,0,0,0,0,0);	-- Brilliant Snow
INSERT INTO vendor_items VALUES (5769,17784984,50,0,0,0,0,0,0);	-- Popper
INSERT INTO vendor_items VALUES (4186,17784984,100,0,0,0,0,0,0);	-- Airborne
INSERT INTO vendor_items VALUES (4218,17784984,100,0,0,0,0,0,0);	-- Air Rider
INSERT INTO vendor_items VALUES (5937,17784984,150,0,0,0,0,0,0);	-- Bubble Breeze
INSERT INTO vendor_items VALUES (5883,17784984,200,0,0,0,0,0,0);	-- Falling Star
INSERT INTO vendor_items VALUES (5882,17784984,250,0,0,0,0,0,0);	-- Marine Bliss
INSERT INTO vendor_items VALUES (4257,17784984,300,0,0,0,0,0,0);	-- Papillion
INSERT INTO vendor_items VALUES (5441,17784984,300,0,0,0,0,0,0);	-- Angelwing
INSERT INTO vendor_items VALUES (5936,17784984,300,0,0,0,0,0,0);	-- Mog Missile

-- Komalata
INSERT INTO vendor_items VALUES (4376,16883791,110,0,0,0,0,0,0);	-- Meat Jerky
INSERT INTO vendor_items VALUES (936,16883791,14,0,0,0,0,0,0);	-- Rock Salt
INSERT INTO vendor_items VALUES (611,16883791,36,0,0,0,0,0,0);	-- Rye Flour
INSERT INTO vendor_items VALUES (4509,16883791,10,0,0,0,0,0,0);	-- Distilled Water
INSERT INTO vendor_items VALUES (625,16883791,88,0,0,0,0,0,0);	-- Apple Vinegar
INSERT INTO vendor_items VALUES (4364,16883791,120,0,0,0,0,0,0);	-- Black Bread
INSERT INTO vendor_items VALUES (610,16883791,60,0,0,0,0,0,0);	-- San d'Orian Flour
INSERT INTO vendor_items VALUES (4389,16883791,32,0,0,0,0,0,0);	-- San d'Orian Carrot
INSERT INTO vendor_items VALUES (629,16883791,48,0,0,0,0,0,0);	-- Millioncorn
INSERT INTO vendor_items VALUES (1523,16883791,316,0,0,0,0,0,0);	-- Apple Mint

-- Kucha Malkobhi
INSERT INTO vendor_items VALUES (12635,17760438,273,0,0,0,0,0,0);	-- Tarutaru Kaftan
INSERT INTO vendor_items VALUES (12756,17760438,163,0,0,0,0,0,0);	-- Tarutaru Mitts
INSERT INTO vendor_items VALUES (12886,17760438,236,0,0,0,0,0,0);	-- Tarutaru Braccae
INSERT INTO vendor_items VALUES (13007,17760438,163,0,0,0,0,0,0);	-- Tarutaru Clomps
INSERT INTO vendor_items VALUES (12636,17760438,273,0,0,0,0,0,0);	-- Mithran Separates
INSERT INTO vendor_items VALUES (12757,17760438,163,0,0,0,0,0,0);	-- Mithran Gauntlets
INSERT INTO vendor_items VALUES (12887,17760438,236,0,0,0,0,0,0);	-- Mithran Loincloth
INSERT INTO vendor_items VALUES (13008,17760438,163,0,0,0,0,0,0);	-- Mithran Gaiters

-- Kulh Amariyo
INSERT INTO vendor_items VALUES (4472,16982094,38,0,0,0,0,0,0);	-- Crayfish
INSERT INTO vendor_items VALUES (5458,16982094,1200,0,0,0,0,0,0);	-- Yilanbaligi (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (5459,16982094,1800,0,0,0,0,0,0);	-- Sazanbaligu (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (5460,16982094,4650,0,0,0,0,0,0);	-- Kayabaligi (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (5461,16982094,130,0,0,0,0,0,0);	-- Alabaligi (Requires Astral Candescence)

-- Kumama
INSERT INTO vendor_items VALUES (12857,17760316,2268,0,0,0,0,0,0);	-- Linen Slops
INSERT INTO vendor_items VALUES (12985,17760316,1462,0,0,0,0,0,0);	-- Holly Clogs
INSERT INTO vendor_items VALUES (12292,17760316,4481,0,0,0,0,0,0);	-- Mahogony Shield
INSERT INTO vendor_items VALUES (12824,17760316,482,0,0,0,0,0,0);	-- Leather Trousers
INSERT INTO vendor_items VALUES (12849,17760316,9936,0,0,2,0,0,0);	-- Cotton Brais
INSERT INTO vendor_items VALUES (12952,17760316,309,0,0,0,0,0,0);	-- Leather Highboots
INSERT INTO vendor_items VALUES (12992,17760316,544,0,0,0,0,0,0);	-- Solea
INSERT INTO vendor_items VALUES (12977,17760316,6633,0,0,2,0,0,0);	-- Cotton Gaiters
INSERT INTO vendor_items VALUES (12290,17760316,556,0,0,0,0,0,0);	-- Maple Shield
INSERT INTO vendor_items VALUES (12848,17760316,1899,0,0,0,0,0,0);	-- Brais
INSERT INTO vendor_items VALUES (12856,17760316,172,0,0,0,0,0,0);	-- Slops
INSERT INTO vendor_items VALUES (12976,17760316,1269,0,0,0,0,0,0);	-- Gaiters
INSERT INTO vendor_items VALUES (12984,17760316,111,0,0,0,0,0,0);	-- Ash Clogs
INSERT INTO vendor_items VALUES (12289,17760316,110,0,0,0,0,0,0);	-- Lauan Shield

-- Kususu
INSERT INTO vendor_items VALUES (4641,17760311,1165,0,0,1,0,0,1);	-- Diaga
INSERT INTO vendor_items VALUES (4662,17760311,7025,0,0,1,0,0,1);	-- Stoneskin
INSERT INTO vendor_items VALUES (4664,17760311,837,0,0,1,0,0,1);	-- Slow
INSERT INTO vendor_items VALUES (4610,17760311,585,0,0,2,0,0,0);	-- Cure II
INSERT INTO vendor_items VALUES (4636,17760311,140,0,0,2,0,0,0);	-- Banish
INSERT INTO vendor_items VALUES (4646,17760311,1165,0,0,2,0,0,0);	-- Banishga
INSERT INTO vendor_items VALUES (4661,17760311,2097,0,0,2,0,0,0);	-- Blink
INSERT INTO vendor_items VALUES (4609,17760311,61,0,0,0,0,0,0);	-- Cure
INSERT INTO vendor_items VALUES (4615,17760311,1363,0,0,0,0,0,0);	-- Curaga
INSERT INTO vendor_items VALUES (4622,17760311,180,0,0,0,0,0,0);	-- Poisona
INSERT INTO vendor_items VALUES (4623,17760311,324,0,0,0,0,0,0);	-- Paralyna
INSERT INTO vendor_items VALUES (4624,17760311,990,0,0,0,0,0,0);	-- Blindna
INSERT INTO vendor_items VALUES (4631,17760311,82,0,0,0,0,0,0);	-- Dia
INSERT INTO vendor_items VALUES (4651,17760311,219,0,0,0,0,0,0);	-- Protect
INSERT INTO vendor_items VALUES (4656,17760311,1584,0,0,0,0,0,0);	-- Shell
INSERT INTO vendor_items VALUES (4663,17760311,360,0,0,0,0,0,0);	-- Aquaveil

-- Layton
INSERT INTO vendor_items VALUES (6049,17494719,8060,0,0,0,0,0,0);	-- Firestorm Schema
INSERT INTO vendor_items VALUES (6050,17494719,6318,0,0,0,0,0,0);	-- Rainstorm Schema
INSERT INTO vendor_items VALUES (6051,17494719,9100,0,0,0,0,0,0);	-- Thunderstorm Schema
INSERT INTO vendor_items VALUES (6052,17494719,8580,0,0,0,0,0,0);	-- Hailstorm Schema
INSERT INTO vendor_items VALUES (6053,17494719,5200,0,0,0,0,0,0);	-- Sandstorm Schema
INSERT INTO vendor_items VALUES (6054,17494719,6786,0,0,0,0,0,0);	-- Windstorm Schema
INSERT INTO vendor_items VALUES (6055,17494719,11440,0,0,0,0,0,0);	-- Aurorastorm Schema
INSERT INTO vendor_items VALUES (6056,17494719,10725,0,0,0,0,0,0);	-- Voidstorm Schema
INSERT INTO vendor_items VALUES (6041,17494719,7714,0,0,0,0,0,0);	-- Pyrohelix Schema
INSERT INTO vendor_items VALUES (6042,17494719,6786,0,0,0,0,0,0);	-- Hydrohelix Schema
INSERT INTO vendor_items VALUES (6043,17494719,8625,0,0,0,0,0,0);	-- Ionohelix Schema
INSERT INTO vendor_items VALUES (6044,17494719,7896,0,0,0,0,0,0);	-- Cryohelix Schema
INSERT INTO vendor_items VALUES (6045,17494719,6591,0,0,0,0,0,0);	-- Geohelix Schema
INSERT INTO vendor_items VALUES (6046,17494719,6981,0,0,0,0,0,0);	-- Anemohelix Schema
INSERT INTO vendor_items VALUES (6047,17494719,8940,0,0,0,0,0,0);	-- Luminohelix Schema
INSERT INTO vendor_items VALUES (6048,17494719,8790,0,0,0,0,0,0);	-- Noctohelix Schema

-- Lebondur
INSERT INTO vendor_items VALUES (636,17760435,119,0,0,0,0,0,0);	-- Chamomile
INSERT INTO vendor_items VALUES (864,17760435,88,0,0,0,0,0,0);	-- Fish Scales
INSERT INTO vendor_items VALUES (936,17760435,14,0,0,0,0,0,0);	-- Rock Salt
INSERT INTO vendor_items VALUES (1410,17760435,1656,0,0,0,0,0,0);	-- Sweet William

-- Leillaine
INSERT INTO vendor_items VALUES (4509,17776721,10,0,0,0,0,0,0);	-- Distilled Water
INSERT INTO vendor_items VALUES (4150,17776721,2387,0,0,0,0,0,0);	-- Eye Drops
INSERT INTO vendor_items VALUES (4148,17776721,290,0,0,0,0,0,0);	-- Antidote
INSERT INTO vendor_items VALUES (4151,17776721,736,0,0,0,0,0,0);	-- Echo Drops
INSERT INTO vendor_items VALUES (4112,17776721,837,0,0,0,0,0,0);	-- Potion
INSERT INTO vendor_items VALUES (4128,17776721,4445,0,0,0,0,0,0);	-- Ether
INSERT INTO vendor_items VALUES (4155,17776721,22400,0,0,0,0,0,0);	-- Remedy

-- Leyla
INSERT INTO vendor_items VALUES (17308,17784835,55,0,0,0,0,0,0);	-- Hawkeye
INSERT INTO vendor_items VALUES (17320,17784835,7,0,0,0,0,0,0);	-- Iron Arrow
INSERT INTO vendor_items VALUES (17336,17784835,5,0,0,0,0,0,0);	-- Crossbow Bolt
INSERT INTO vendor_items VALUES (4509,17784835,10,0,0,0,0,0,0);	-- Distilled Water
INSERT INTO vendor_items VALUES (5038,17784835,1000,0,0,0,0,0,0);	-- Enchanting Etude
INSERT INTO vendor_items VALUES (5037,17784835,1265,0,0,0,0,0,0);	-- Spirited Etude
INSERT INTO vendor_items VALUES (5036,17784835,1567,0,0,0,0,0,0);	-- Learned Etude
INSERT INTO vendor_items VALUES (5035,17784835,1913,0,0,0,0,0,0);	-- Quick Etude
INSERT INTO vendor_items VALUES (5034,17784835,2208,0,0,0,0,0,0);	-- Vivacious Etude
INSERT INTO vendor_items VALUES (5033,17784835,2815,0,0,0,0,0,0);	-- Dextrous Etude
INSERT INTO vendor_items VALUES (5032,17784835,3146,0,0,0,0,0,0);	-- Sinewy Etude

-- Lusiane
INSERT INTO vendor_items VALUES (17389,17719350,496,1,0,0,1,0,0);	-- Bamboo Fishing Rod
INSERT INTO vendor_items VALUES (17395,17719350,9,2,0,0,0,0,0);	-- Lugworm
INSERT INTO vendor_items VALUES (17390,17719350,217,2,0,0,0,0,0);	-- Yew Fishing Rod
INSERT INTO vendor_items VALUES (17396,17719350,3,0,0,0,0,0,0);	-- Little Worm
INSERT INTO vendor_items VALUES (5068,17719350,110,0,0,0,0,0,0);	-- Scroll of Light Threnoldy
INSERT INTO vendor_items VALUES (5066,17719350,1265,0,0,0,0,0,0);	-- Scroll of Lightning Threnoldy
INSERT INTO vendor_items VALUES (17391,17719350,66,0,0,0,0,0,0);	-- Willow Fishing Rod

-- Macchi Gazlitah
INSERT INTO vendor_items VALUES (5703,17772598,100,0,0,0,0,0,0);	-- Uleguerand Milk
INSERT INTO vendor_items VALUES (5684,17772598,250,0,0,0,0,0,0);	-- Chalaimbille
INSERT INTO vendor_items VALUES (17905,17772598,100,0,0,0,0,0,0);	-- Wormy Broth
INSERT INTO vendor_items VALUES (5686,17772598,800,0,0,0,0,0,0);	-- Cheese Sandwich
INSERT INTO vendor_items VALUES (5729,17772598,3360,0,0,0,0,0,0);	-- Bavarois
INSERT INTO vendor_items VALUES (5718,17772598,1300,0,0,0,0,0,0);	-- Cream Puff
INSERT INTO vendor_items VALUES (461,17772598,5000,0,0,0,0,0,0);	-- Buffalo Milk Case
INSERT INTO vendor_items VALUES (5152,17772598,1280,0,0,0,0,0,0);	-- Buffalo Meat
INSERT INTO vendor_items VALUES (4722,17772598,31878,0,0,0,0,0,0);	-- Enfire II
INSERT INTO vendor_items VALUES (4723,17772598,30492,0,0,0,0,0,0);	-- Enblizzard II
INSERT INTO vendor_items VALUES (4724,17772598,27968,0,0,0,0,0,0);	-- Enaero II
INSERT INTO vendor_items VALUES (4725,17772598,26112,0,0,0,0,0,0);	-- Enstone II
INSERT INTO vendor_items VALUES (4726,17772598,25600,0,0,0,0,0,0);	-- Enthunder II
INSERT INTO vendor_items VALUES (4727,17772598,33000,0,0,0,0,0,0);	-- Enwater II
INSERT INTO vendor_items VALUES (4850,17772598,150000,0,0,0,0,0,0);	-- Refresh II

-- Machielle
INSERT INTO vendor_items VALUES (688,17719303,18,0,0,0,0,0,0);	-- Arrowwood Log
INSERT INTO vendor_items VALUES (621,17719303,25,0,0,0,0,0,0);	-- Crying Mustard
INSERT INTO vendor_items VALUES (618,17719303,25,0,0,0,0,0,0);	-- Blue Peas
INSERT INTO vendor_items VALUES (698,17719303,88,0,0,0,0,0,0);	-- Ash Log

-- Maera
INSERT INTO vendor_items VALUES (4112,17678361,910,0,0,0,0,0,0);	-- Potion
INSERT INTO vendor_items VALUES (4128,17678361,4832,0,0,0,0,0,0);	-- Ether
INSERT INTO vendor_items VALUES (4148,17678361,316,0,0,0,0,0,0);	-- Antidote
INSERT INTO vendor_items VALUES (4150,17678361,2595,0,0,0,0,0,0);	-- Eye Drops
INSERT INTO vendor_items VALUES (4151,17678361,800,0,0,0,0,0,0);	-- Echo Drops

-- Malfud
INSERT INTO vendor_items VALUES (936,16982089,16,0,0,0,0,0,0);	-- Rock Salt
INSERT INTO vendor_items VALUES (626,16982089,255,0,0,0,0,0,0);	-- Black Pepper
INSERT INTO vendor_items VALUES (633,16982089,16,0,0,0,0,0,0);	-- Olive Oil
INSERT INTO vendor_items VALUES (4388,16982089,44,0,0,0,0,0,0);	-- Eggplant
INSERT INTO vendor_items VALUES (4390,16982089,40,0,0,0,0,0,0);	-- Mithran Tomato
INSERT INTO vendor_items VALUES (2213,16982089,12,0,0,0,0,0,0);	-- Pine Nuts

-- Mamaroon
INSERT INTO vendor_items VALUES (4860,16994346,27000,0,0,0,0,0,0);	-- Scroll of Stun
INSERT INTO vendor_items VALUES (4708,16994346,5160,0,0,0,0,0,0);	-- Scroll of Enfire
INSERT INTO vendor_items VALUES (4709,16994346,4098,0,0,0,0,0,0);	-- Scroll of Enblizzard
INSERT INTO vendor_items VALUES (4710,16994346,2500,0,0,0,0,0,0);	-- Scroll of Enaero
INSERT INTO vendor_items VALUES (4711,16994346,2030,0,0,0,0,0,0);	-- Scroll of Entone
INSERT INTO vendor_items VALUES (4712,16994346,1515,0,0,0,0,0,0);	-- Scroll of Enthunder
INSERT INTO vendor_items VALUES (4713,16994346,7074,0,0,0,0,0,0);	-- Scroll of Enwater
INSERT INTO vendor_items VALUES (4859,16994346,9000,0,0,0,0,0,0);	-- Scroll of Shock Spikes
INSERT INTO vendor_items VALUES (2502,16994346,29950,0,0,0,0,0,0);	-- White Puppet Turban
INSERT INTO vendor_items VALUES (2501,16994346,29950,0,0,0,0,0,0);	-- Black Puppet Turban

-- Mamerie
INSERT INTO vendor_items VALUES (4545,17801338,62,0,0,0,0,0,0);	-- Gysahl Greens
INSERT INTO vendor_items VALUES (840,17801338,7,0,0,0,0,0,0);	-- Chocobo Feather
INSERT INTO vendor_items VALUES (17016,17801338,11,0,0,0,0,0,0);	-- Pet Food Alpha Biscuit
INSERT INTO vendor_items VALUES (17017,17801338,82,0,0,0,0,0,0);	-- Pet Food Beta Biscuit
INSERT INTO vendor_items VALUES (17860,17801338,82,0,0,0,0,0,0);	-- Carrot Broth
INSERT INTO vendor_items VALUES (17862,17801338,695,0,0,0,0,0,0);	-- Bug Broth
INSERT INTO vendor_items VALUES (17864,17801338,126,0,0,0,0,0,0);	-- Herbal Broth
INSERT INTO vendor_items VALUES (17866,17801338,695,0,0,0,0,0,0);	-- Carrion Broth
INSERT INTO vendor_items VALUES (5073,17801338,50784,0,0,0,0,0,0);	-- Scroll of Chocobo Mazurka

-- Manyny
INSERT INTO vendor_items VALUES (5032,17764456,3112,0,0,0,0,0,0);	-- Sinewy Etude
INSERT INTO vendor_items VALUES (5033,17764456,2784,0,0,0,0,0,0);	-- Dextrous Etude
INSERT INTO vendor_items VALUES (5034,17764456,2184,0,0,0,0,0,0);	-- Vivacious Etude
INSERT INTO vendor_items VALUES (5035,17764456,1892,0,0,0,0,0,0);	-- Quick Etude
INSERT INTO vendor_items VALUES (5036,17764456,1550,0,0,0,0,0,0);	-- Learned Etude
INSERT INTO vendor_items VALUES (5037,17764456,1252,0,0,0,0,0,0);	-- Spirited Etude
INSERT INTO vendor_items VALUES (5038,17764456,990,0,0,0,0,0,0);	-- Enchanting Etude

-- Maqu Molpih
INSERT INTO vendor_items VALUES (631,17752102,36,0,0,0,0,0,0);	-- Horo Flour
INSERT INTO vendor_items VALUES (629,17752102,44,0,0,0,0,0,0);	-- Millioncorn
INSERT INTO vendor_items VALUES (4415,17752102,114,0,0,0,0,0,0);	-- Roasted Corn
INSERT INTO vendor_items VALUES (4505,17752102,92,0,0,0,0,0,0);	-- Sunflower Seeds
INSERT INTO vendor_items VALUES (841,17752102,36,0,0,0,0,0,0);	-- Yagudo Feather

-- Matoaka
INSERT INTO vendor_items VALUES (13327,17780863,1250,0,0,0,0,0,0);	-- Silver Earring
INSERT INTO vendor_items VALUES (13456,17780863,1250,0,0,0,0,0,0);	-- Silver Ring
INSERT INTO vendor_items VALUES (13328,17780863,4140,0,0,0,0,0,0);	-- Mythril Earring

-- Mazuro-Oozuro
INSERT INTO vendor_items VALUES (17005,16883790,108,0,0,0,0,0,0);	-- Lufaise Fly
INSERT INTO vendor_items VALUES (17383,16883790,2640,0,0,0,0,0,0);	-- Clothespole
INSERT INTO vendor_items VALUES (688,16883790,20,0,0,0,0,0,0);	-- Arrowwood Log
INSERT INTO vendor_items VALUES (690,16883790,7800,0,0,0,0,0,0);	-- Elm Log
INSERT INTO vendor_items VALUES (2871,16883790,10000,0,0,0,0,0,0);	-- Safehold Waystone
INSERT INTO vendor_items VALUES (4913,16883790,175827,0,0,0,0,0,0);	-- Scroll of Distract II
INSERT INTO vendor_items VALUES (4915,16883790,217000,0,0,0,0,0,0);	-- Scroll of Frazzle II
INSERT INTO vendor_items VALUES (4638,16883790,66000,0,0,0,0,0,0);	-- Banish III

-- Mazween
INSERT INTO vendor_items VALUES (4881,16982098,11200,0,0,0,0,0,0);	-- Scroll of Sleepga
INSERT INTO vendor_items VALUES (4867,16982098,18720,0,0,0,0,0,0);	-- Scroll of Sleep II
INSERT INTO vendor_items VALUES (4829,16982098,25200,0,0,0,0,0,0);	-- Poison II
INSERT INTO vendor_items VALUES (4839,16982098,14000,0,0,0,0,0,0);	-- Bio II
INSERT INTO vendor_items VALUES (4833,16982098,5160,0,0,0,0,0,0);	-- Poisonga
INSERT INTO vendor_items VALUES (4769,16982098,19932,0,0,0,0,0,0);	-- Stone III
INSERT INTO vendor_items VALUES (4779,16982098,22682,0,0,0,0,0,0);	-- Water III
INSERT INTO vendor_items VALUES (4764,16982098,27744,0,0,0,0,0,0);	-- Aero III
INSERT INTO vendor_items VALUES (4754,16982098,33306,0,0,0,0,0,0);	-- Fire III
INSERT INTO vendor_items VALUES (4759,16982098,39368,0,0,0,0,0,0);	-- Blizzard III
INSERT INTO vendor_items VALUES (4774,16982098,45930,0,0,0,0,0,0);	-- Thunder III
INSERT INTO vendor_items VALUES (4883,16982098,27000,0,0,0,0,0,0);	-- Absorb-TP
INSERT INTO vendor_items VALUES (4854,16982098,30780,0,0,0,0,0,0);	-- Drain II
INSERT INTO vendor_items VALUES (4885,16982098,70560,0,0,0,0,0,0);	-- Dread Spikes
INSERT INTO vendor_items VALUES (4886,16982098,44000,0,0,0,0,0,0);	-- Absorb-ACC
INSERT INTO vendor_items VALUES (4856,16982098,79800,0,0,0,0,0,0);	-- Aspir II

-- Mejuone
INSERT INTO vendor_items VALUES (4545,17776711,62,0,0,0,0,0,0);	-- Gysahl Greens
INSERT INTO vendor_items VALUES (840,17776711,7,0,0,0,0,0,0);	-- Chocobo Feather
INSERT INTO vendor_items VALUES (17307,17776711,9,0,0,0,0,0,0);	-- Dart

-- Melleupaux
INSERT INTO vendor_items VALUES (16450,16883793,2030,0,0,0,0,0,0);	-- Dagger
INSERT INTO vendor_items VALUES (16566,16883793,9216,0,0,0,0,0,0);	-- Longsword
INSERT INTO vendor_items VALUES (17335,16883793,4,0,0,0,0,0,0);	-- Rusty Bolt
INSERT INTO vendor_items VALUES (18375,16883793,37296,0,0,0,0,0,0);	-- Falx
INSERT INTO vendor_items VALUES (18214,16883793,20762,0,0,0,0,0,0);	-- Voulge

-- Melloa
INSERT INTO vendor_items VALUES (4591,17743888,147,0,1,0,0,1,0);	-- Pumpernickel
INSERT INTO vendor_items VALUES (4417,17743888,3036,0,1,0,0,1,0);	-- Egg Soup
INSERT INTO vendor_items VALUES (4442,17743888,368,0,1,0,0,1,0);	-- Pineapple Juice
INSERT INTO vendor_items VALUES (4391,17743888,22,0,2,0,0,0,0);	-- Bretzel
INSERT INTO vendor_items VALUES (4578,17743888,143,0,2,0,0,0,0);	-- Sausage
INSERT INTO vendor_items VALUES (4424,17743888,1012,0,2,0,0,0,0);	-- Melon Juice
INSERT INTO vendor_items VALUES (4437,17743888,662,0,2,0,0,0,0);	-- Roast Mutton
INSERT INTO vendor_items VALUES (4499,17743888,92,0,0,0,0,0,0);	-- Iron Bread
INSERT INTO vendor_items VALUES (4436,17743888,294,0,0,0,0,0,0);	-- Baked Popoto
INSERT INTO vendor_items VALUES (4455,17743888,184,0,0,0,0,0,0);	-- Pebble Soup
INSERT INTO vendor_items VALUES (4509,17743888,10,0,0,0,0,0,0);	-- Distilled Water

-- Migran
INSERT INTO vendor_items VALUES (12577,16883795,2485,0,0,0,0,0,0);	-- Brass Harness
INSERT INTO vendor_items VALUES (12985,16883795,1625,0,0,0,0,0,0);	-- Holly Clogs
INSERT INTO vendor_items VALUES (14317,16883795,101055,0,0,0,0,0,0);	-- Barone Cosciales
INSERT INTO vendor_items VALUES (15305,16883795,630255,0,0,0,0,0,0);	-- Barone Gambieras
INSERT INTO vendor_items VALUES (14848,16883795,181905,0,0,0,0,0,0);	-- Barone Manopolas
INSERT INTO vendor_items VALUES (15389,16883795,8000000,0,0,0,0,0,0);	-- Vir Subligar
INSERT INTO vendor_items VALUES (15390,16883795,8000000,0,0,0,0,0,0);	-- Femina Subligar

-- Mille
INSERT INTO vendor_items VALUES (688,17735744,18,0,0,0,0,0,0);	-- Arrowwood Log
INSERT INTO vendor_items VALUES (698,17735744,88,0,0,0,0,0,0);	-- Ash Log
INSERT INTO vendor_items VALUES (618,17735744,25,0,0,0,0,0,0);	-- Blue Peas
INSERT INTO vendor_items VALUES (621,17735744,25,0,0,0,0,0,0);	-- Crying Mustard

-- Millechuca
INSERT INTO vendor_items VALUES (636,17723498,119,0,0,0,0,0,0);	-- Chamomile
INSERT INTO vendor_items VALUES (864,17723498,88,0,0,0,0,0,0);	-- Fish Scales
INSERT INTO vendor_items VALUES (936,17723498,14,0,0,0,0,0,0);	-- Rock Salt
INSERT INTO vendor_items VALUES (1410,17723498,1656,0,0,0,0,0,0);	-- Sweet William

-- Millerovieunet
INSERT INTO vendor_items VALUES (954,17764465,4032,0,0,0,0,0,0);	-- Magic Pot Shard

-- Milva
INSERT INTO vendor_items VALUES (4444,17727525,22,0,0,0,0,0,0);	-- Rarab Tail
INSERT INTO vendor_items VALUES (689,17727525,33,0,0,0,0,0,0);	-- Lauan Log
INSERT INTO vendor_items VALUES (619,17727525,43,0,0,0,0,0,0);	-- Popoto
INSERT INTO vendor_items VALUES (4392,17727525,29,0,0,0,0,0,0);	-- Saruta Orange
INSERT INTO vendor_items VALUES (635,17727525,18,0,0,0,0,0,0);	-- Windurstian Tea Leaves

-- Miogique
INSERT INTO vendor_items VALUES (12552,17719387,14256,1,0,0,1,0,0);	-- Chainmail
INSERT INTO vendor_items VALUES (12680,17719387,7783,1,0,0,1,0,0);	-- Chain Mittens
INSERT INTO vendor_items VALUES (12672,17719387,23846,1,0,0,1,0,0);	-- Gauntlets
INSERT INTO vendor_items VALUES (12424,17719387,9439,1,0,0,1,0,0);	-- Iron Mask
INSERT INTO vendor_items VALUES (12442,17719387,13179,2,0,0,0,0,0);	-- Studded Bandana
INSERT INTO vendor_items VALUES (12698,17719387,11012,2,0,0,0,0,0);	-- Studded Gloves
INSERT INTO vendor_items VALUES (12570,17719387,20976,2,0,0,0,0,0);	-- Studded Vest
INSERT INTO vendor_items VALUES (12449,17719387,1504,0,0,0,0,0,0);	-- Brass Cap
INSERT INTO vendor_items VALUES (12577,17719387,2286,0,0,0,0,0,0);	-- Brass Harness
INSERT INTO vendor_items VALUES (12705,17719387,1255,0,0,0,0,0,0);	-- Brass Mittens
INSERT INTO vendor_items VALUES (12448,17719387,154,0,0,0,0,0,0);	-- Bronze Cap
INSERT INTO vendor_items VALUES (12576,17719387,576,0,0,0,0,0,0);	-- Bronze Harness
INSERT INTO vendor_items VALUES (12704,17719387,128,0,0,0,0,0,0);	-- Bronze Mittens
INSERT INTO vendor_items VALUES (12440,17719387,396,0,0,0,0,0,0);	-- Leather Bandana
INSERT INTO vendor_items VALUES (12696,17719387,331,0,0,0,0,0,0);	-- Leather Gloves
INSERT INTO vendor_items VALUES (12568,17719387,618,0,0,0,0,0,0);	-- Leather Vest

-- Misseulieu
INSERT INTO vendor_items VALUES (12577,16883794,2485,0,0,0,0,0,0);	-- Brass Harness
INSERT INTO vendor_items VALUES (12985,16883794,1625,0,0,0,0,0,0);	-- Holly Clogs
INSERT INTO vendor_items VALUES (14317,16883794,101055,0,0,0,0,0,0);	-- Barone Cosciales
INSERT INTO vendor_items VALUES (15305,16883794,630255,0,0,0,0,0,0);	-- Barone Gambieras
INSERT INTO vendor_items VALUES (14848,16883794,181905,0,0,0,0,0,0);	-- Barone Manopolas
INSERT INTO vendor_items VALUES (15389,16883794,8000000,0,0,0,0,0,0);	-- Vir Subligar
INSERT INTO vendor_items VALUES (15390,16883794,8000000,0,0,0,0,0,0);	-- Femina Subligar

-- Mjoll
INSERT INTO vendor_items VALUES (17321,17739804,16,0,1,0,0,1,0);	-- Silver Arrow
INSERT INTO vendor_items VALUES (17318,17739804,3,0,2,0,0,0,0);	-- Wooden Arrow
INSERT INTO vendor_items VALUES (17320,17739804,7,0,0,0,0,0,0);	-- Iron Arrow
INSERT INTO vendor_items VALUES (5069,17739804,199,0,0,0,0,0,0);	-- Scroll of Dark Threnody
INSERT INTO vendor_items VALUES (5063,17739804,1000,0,0,0,0,0,0);	-- Scroll of Ice Threnody

-- Mono Nchaa
INSERT INTO vendor_items VALUES (17318,17764455,3,0,0,2,0,0,0);	-- Wooden Arrow
INSERT INTO vendor_items VALUES (17308,17764455,55,0,0,2,0,0,0);	-- Hawkeye
INSERT INTO vendor_items VALUES (17216,17764455,165,0,0,2,0,0,0);	-- Light Crossbow
INSERT INTO vendor_items VALUES (17319,17764455,4,0,0,0,0,0,0);	-- Bone Arrow
INSERT INTO vendor_items VALUES (17336,17764455,5,0,0,0,0,0,0);	-- Crossbow Bolt
INSERT INTO vendor_items VALUES (5009,17764455,2649,0,0,0,0,0,0);	-- Scroll of Hunter's Prelude

-- Morefie
INSERT INTO vendor_items VALUES (13327,17780862,1250,0,0,0,0,0,0);	-- Silver Earring
INSERT INTO vendor_items VALUES (13456,17780862,1250,0,0,0,0,0,0);	-- Silver Ring
INSERT INTO vendor_items VALUES (13328,17780862,4140,0,0,0,0,0,0);	-- Mythril Earring

-- Mulnith
INSERT INTO vendor_items VALUES (4410,16982091,344,0,0,0,0,0,0);	-- Roast Mushroom
INSERT INTO vendor_items VALUES (5598,16982091,2000,0,0,0,0,0,0);	-- Sis Kebabi (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (5600,16982091,3000,0,0,0,0,0,0);	-- Balik Sis (Requires Astral Candescence)

-- Neigepance
INSERT INTO vendor_items VALUES (17307,17735733,9,0,1,0,0,1,0);	-- Dart
INSERT INTO vendor_items VALUES (845,17735733,1150,0,1,0,0,1,0);	-- Black Chocobo Feather
INSERT INTO vendor_items VALUES (4545,17735733,62,0,0,0,0,0,0);	-- Gysahl Greens
INSERT INTO vendor_items VALUES (840,17735733,7,0,0,0,0,0,0);	-- Chocobo Feather
INSERT INTO vendor_items VALUES (17016,17735733,11,0,0,0,0,0,0);	-- Pet Food Alpha Biscuit
INSERT INTO vendor_items VALUES (17017,17735733,82,0,0,0,0,0,0);	-- Pet Food Beta Biscuit
INSERT INTO vendor_items VALUES (17860,17735733,82,0,0,0,0,0,0);	-- Carrot Broth
INSERT INTO vendor_items VALUES (17862,17735733,695,0,0,0,0,0,0);	-- Bug Broth
INSERT INTO vendor_items VALUES (17864,17735733,126,0,0,0,0,0,0);	-- Herbal Broth
INSERT INTO vendor_items VALUES (17866,17735733,695,0,0,0,0,0,0);	-- Carrion Broth
INSERT INTO vendor_items VALUES (5073,17735733,50784,0,0,0,0,0,0);	-- Scroll of Chocobo Mazurka

-- Ness Rugetomal
INSERT INTO vendor_items VALUES (4394,17752101,10,0,0,1,0,0,1);	-- Ginger Cookie
INSERT INTO vendor_items VALUES (4407,17752101,727,0,0,1,0,0,1);	-- Carp Sushi
INSERT INTO vendor_items VALUES (4425,17752101,323,0,0,1,0,0,1);	-- Tomato Juice
INSERT INTO vendor_items VALUES (4459,17752101,1656,0,0,1,0,0,1);	-- Nebimonite Bake
INSERT INTO vendor_items VALUES (4397,17752101,14,0,0,2,0,0,0);	-- Cinna-cookie
INSERT INTO vendor_items VALUES (4422,17752101,184,0,0,2,0,0,0);	-- Orange Juice
INSERT INTO vendor_items VALUES (4456,17752101,2070,0,0,2,0,0,0);	-- Boiled Crab
INSERT INTO vendor_items VALUES (4510,17752101,21,0,0,0,0,0,0);	-- Acorn Cookie
INSERT INTO vendor_items VALUES (4376,17752101,108,0,0,0,0,0,0);	-- Meat Jerky
INSERT INTO vendor_items VALUES (4509,17752101,10,0,0,0,0,0,0);	-- Distilled Water
INSERT INTO vendor_items VALUES (4538,17752101,846,0,0,0,0,0,0);	-- Roast Pipira

-- Nhobi Zalkia
INSERT INTO vendor_items VALUES (916,17764464,855,0,0,0,0,0,0);	-- Cactuar Needle
INSERT INTO vendor_items VALUES (4412,17764464,299,0,0,0,0,0,0);	-- Thundermelon
INSERT INTO vendor_items VALUES (4491,17764464,184,0,0,0,0,0,0);	-- Watermelon

-- Nilerouche
INSERT INTO vendor_items VALUES (17005,16883789,108,0,0,0,0,0,0);	-- Lufaise Fly
INSERT INTO vendor_items VALUES (17383,16883789,2640,0,0,0,0,0,0);	-- Clothespole
INSERT INTO vendor_items VALUES (688,16883789,20,0,0,0,0,0,0);	-- Arrowwood Log
INSERT INTO vendor_items VALUES (690,16883789,7800,0,0,0,0,0,0);	-- Elm Log
INSERT INTO vendor_items VALUES (2871,16883789,10000,0,0,0,0,0,0);	-- Safehold Waystone
INSERT INTO vendor_items VALUES (4913,16883789,175827,0,0,0,0,0,0);	-- Scroll of Distract II
INSERT INTO vendor_items VALUES (4915,16883789,217000,0,0,0,0,0,0);	-- Scroll of Frazzle II
INSERT INTO vendor_items VALUES (4638,16883789,66000,0,0,0,0,0,0);	-- Banish III

-- Nimia
INSERT INTO vendor_items VALUES (612,17727528,55,0,0,0,0,0,0);	-- Kazham Peppers
INSERT INTO vendor_items VALUES (4432,17727528,55,0,0,0,0,0,0);	-- Kazham Pineapple
INSERT INTO vendor_items VALUES (4390,17727528,36,0,0,0,0,0,0);	-- Mithran Tomato
INSERT INTO vendor_items VALUES (626,17727528,234,0,0,0,0,0,0);	-- Black Pepper
INSERT INTO vendor_items VALUES (630,17727528,88,0,0,0,0,0,0);	-- Ogre Pumpkin
INSERT INTO vendor_items VALUES (632,17727528,110,0,0,0,0,0,0);	-- Kukuru Bean
INSERT INTO vendor_items VALUES (1411,17727528,1656,0,0,0,0,0,0);	-- Phalaenopsis

-- Nogga
INSERT INTO vendor_items VALUES (17316,17747977,675,0,2,0,0,0,0);	-- Bomb Arm
INSERT INTO vendor_items VALUES (17313,17747977,1083,0,0,0,0,0,0);	-- Grenade

-- Nuh Celodehki
INSERT INTO vendor_items VALUES (4398,17801261,993,0,0,0,0,0,0);	-- Fish Mithkabob
INSERT INTO vendor_items VALUES (4536,17801261,3133,0,0,0,0,0,0);	-- Blackened Frog
INSERT INTO vendor_items VALUES (4410,17801261,316,0,0,0,0,0,0);	-- Roast Mushroom
INSERT INTO vendor_items VALUES (4457,17801261,2700,0,0,0,0,0,0);	-- Eel Kabob

-- Numa
INSERT INTO vendor_items VALUES (12457,17743907,5079,0,1,0,0,1,0);	-- Cotton Hachimaki
INSERT INTO vendor_items VALUES (12585,17743907,7654,0,1,0,0,1,0);	-- Cotton Dogi
INSERT INTO vendor_items VALUES (12713,17743907,4212,0,1,0,0,1,0);	-- Cotton Tekko
INSERT INTO vendor_items VALUES (12841,17743907,6133,0,1,0,0,1,0);	-- Cotton Sitabaki
INSERT INTO vendor_items VALUES (12969,17743907,3924,0,1,0,0,1,0);	-- Cotton Kyahan
INSERT INTO vendor_items VALUES (13205,17743907,3825,0,1,0,0,1,0);	-- Silver Obi
INSERT INTO vendor_items VALUES (12456,17743907,759,0,2,0,0,0,0);	-- Hachimaki
INSERT INTO vendor_items VALUES (12584,17743907,1145,0,2,0,0,0,0);	-- Kenpogi
INSERT INTO vendor_items VALUES (12712,17743907,630,0,2,0,0,0,0);	-- Tekko
INSERT INTO vendor_items VALUES (12840,17743907,915,0,2,0,0,0,0);	-- Sitabaki
INSERT INTO vendor_items VALUES (12968,17743907,584,0,2,0,0,0,0);	-- Kyahan
INSERT INTO vendor_items VALUES (704,17743907,132,0,2,0,0,0,0);	-- Bamboo Stick
INSERT INTO vendor_items VALUES (605,17743907,180,0,0,0,0,0,0);	-- Pickaxe

-- Nya Labiccio
INSERT INTO vendor_items VALUES (1108,17764460,703,0,0,0,0,0,0);	-- Sulfur
INSERT INTO vendor_items VALUES (619,17764460,43,0,0,0,0,0,0);	-- Popoto
INSERT INTO vendor_items VALUES (611,17764460,36,0,0,0,0,0,0);	-- Rye Flour
INSERT INTO vendor_items VALUES (4388,17764460,40,0,0,0,0,0,0);	-- Eggplant

-- Oggodett
INSERT INTO vendor_items VALUES (631,17739819,36,0,0,0,0,0,0);	-- Horo Flour
INSERT INTO vendor_items VALUES (629,17739819,43,0,0,0,0,0,0);	-- Millioncorn
INSERT INTO vendor_items VALUES (4415,17739819,111,0,0,0,0,0,0);	-- Roasted Corn
INSERT INTO vendor_items VALUES (4505,17739819,90,0,0,0,0,0,0);	-- Sunflower Seeds
INSERT INTO vendor_items VALUES (841,17739819,36,0,0,0,0,0,0);	-- Yagudo Feather

-- Olaf
INSERT INTO vendor_items VALUES (17248,17747976,46836,0,2,0,0,0,0);	-- Arquebus
INSERT INTO vendor_items VALUES (17340,17747976,90,0,0,0,0,0,0);	-- Bullet
INSERT INTO vendor_items VALUES (928,17747976,463,0,0,0,0,0,0);	-- Bomb Ash

-- Olwyn
INSERT INTO vendor_items VALUES (4128,17739805,4445,0,1,0,0,1,0);	-- Ether
INSERT INTO vendor_items VALUES (4151,17739805,736,0,2,0,0,0,0);	-- Echo Drops
INSERT INTO vendor_items VALUES (4112,17739805,837,0,2,0,0,0,0);	-- Potion
INSERT INTO vendor_items VALUES (4150,17739805,2387,0,0,0,0,0,0);	-- Eye Drops
INSERT INTO vendor_items VALUES (4148,17739805,290,0,0,0,0,0,0);	-- Antidote

-- Orez-Ebrez
INSERT INTO vendor_items VALUES (12466,17752094,20000,0,0,1,0,0,1);	-- Red Cap
INSERT INTO vendor_items VALUES (12458,17752094,8972,0,0,1,0,0,1);	-- Soil Hachimaki
INSERT INTO vendor_items VALUES (12455,17752094,7026,0,0,1,0,0,1);	-- Beetle Mask
INSERT INTO vendor_items VALUES (12472,17752094,144,0,0,2,0,0,0);	-- Circlet
INSERT INTO vendor_items VALUES (12465,17752094,8024,0,0,2,0,0,0);	-- Cotton Headgear
INSERT INTO vendor_items VALUES (12440,17752094,396,0,0,2,0,0,0);	-- Leather Bandana
INSERT INTO vendor_items VALUES (12473,17752094,1863,0,0,2,0,0,0);	-- Poet's Circlet
INSERT INTO vendor_items VALUES (12499,17752094,14400,0,0,2,0,0,0);	-- Flax Headband
INSERT INTO vendor_items VALUES (12457,17752094,3272,0,0,2,0,0,0);	-- Cotton Hachimaki
INSERT INTO vendor_items VALUES (12454,17752094,3520,0,0,0,0,0,0);	-- Bone Mask
INSERT INTO vendor_items VALUES (12474,17752094,10924,0,0,2,0,0,0);	-- Wool Hat
INSERT INTO vendor_items VALUES (12464,17752094,1742,0,0,0,0,0,0);	-- Headgear
INSERT INTO vendor_items VALUES (12456,17752094,552,0,0,0,0,0,0);	-- Hachimaki
INSERT INTO vendor_items VALUES (12498,17752094,1800,0,0,0,0,0,0);	-- Cotton Headband
INSERT INTO vendor_items VALUES (12448,17752094,151,0,0,0,0,0,0);	-- Bronze Cap
INSERT INTO vendor_items VALUES (12449,17752094,1471,0,0,0,0,0,0);	-- Brass Cap

-- Ostalie
INSERT INTO vendor_items VALUES (4128,17719351,4445,1,0,0,1,0,0);	-- Ether
INSERT INTO vendor_items VALUES (4112,17719351,837,1,0,0,1,0,0);	-- Potion
INSERT INTO vendor_items VALUES (4151,17719351,736,2,0,0,0,0,0);	-- Echo Drops
INSERT INTO vendor_items VALUES (4148,17719351,290,0,0,0,0,0,0);	-- Antidote
INSERT INTO vendor_items VALUES (12472,17719351,144,0,0,0,0,0,0);	-- Circlet
INSERT INTO vendor_items VALUES (12728,17719351,118,0,0,0,0,0,0);	-- Cuffs
INSERT INTO vendor_items VALUES (4150,17719351,2387,0,0,0,0,0,0);	-- Eye Drops
INSERT INTO vendor_items VALUES (1021,17719351,450,0,0,0,0,0,0);	-- Hatchet
INSERT INTO vendor_items VALUES (13192,17719351,382,0,0,0,0,0,0);	-- Leather Belt
INSERT INTO vendor_items VALUES (13193,17719351,2430,0,0,0,0,0,0);	-- Lizard Belt
INSERT INTO vendor_items VALUES (605,17719351,180,0,0,0,0,0,0);	-- Pickaxe
INSERT INTO vendor_items VALUES (12600,17719351,216,0,0,0,0,0,0);	-- Robe
INSERT INTO vendor_items VALUES (12856,17719351,172,0,0,0,0,0,0);	-- Slops

-- Otete
INSERT INTO vendor_items VALUES (623,17752106,119,0,0,0,0,0,0);	-- Bay Leaves
INSERT INTO vendor_items VALUES (4154,17752106,6440,0,0,0,0,0,0);	-- Holy Water

-- Pahya Lolohoiv
INSERT INTO vendor_items VALUES (4509,17801279,10,0,0,0,0,0,0);	-- Distilled Water
INSERT INTO vendor_items VALUES (4150,17801279,2387,0,0,0,0,0,0);	-- Eye Drops
INSERT INTO vendor_items VALUES (4148,17801279,290,0,0,0,0,0,0);	-- Antidote
INSERT INTO vendor_items VALUES (4151,17801279,736,0,0,0,0,0,0);	-- Echo Drops
INSERT INTO vendor_items VALUES (4112,17801279,837,0,0,0,0,0,0);	-- Potion
INSERT INTO vendor_items VALUES (4128,17801279,4445,0,0,0,0,0,0);	-- Ether
INSERT INTO vendor_items VALUES (924,17801279,556,0,0,0,0,0,0);	-- Fiend Blood
INSERT INTO vendor_items VALUES (943,17801279,294,0,0,0,0,0,0);	-- Poison Dust

-- Palguevion
INSERT INTO vendor_items VALUES (4382,17723491,29,0,0,0,0,0,0);	-- Frost Turnip
INSERT INTO vendor_items VALUES (638,17723491,170,0,0,0,0,0,0);	-- Sage

-- Patolle
INSERT INTO vendor_items VALUES (916,17727529,855,0,0,0,0,0,0);	-- Cactuar Needle
INSERT INTO vendor_items VALUES (4412,17727529,299,0,0,0,0,0,0);	-- Thundermelon
INSERT INTO vendor_items VALUES (4491,17727529,184,0,0,0,0,0,0);	-- Watermelon

-- Paunelie
INSERT INTO vendor_items VALUES (512,17719488,8000,0,0,0,0,0,0);	-- Linkshell
INSERT INTO vendor_items VALUES (16285,17719488,375,0,0,0,0,0,0);	-- Pendant Compass

-- Pawkrix
INSERT INTO vendor_items VALUES (631,17780760,36,0,0,0,0,0,0);	-- Horo Flour
INSERT INTO vendor_items VALUES (4458,17780760,276,0,0,0,0,0,0);	-- Goblin Bread
INSERT INTO vendor_items VALUES (4539,17780760,650,0,0,0,0,0,0);	-- Goblin Pie
INSERT INTO vendor_items VALUES (4495,17780760,35,0,0,0,0,0,0);	-- Goblin Chocolate
INSERT INTO vendor_items VALUES (4543,17780760,1140,0,0,0,0,0,0);	-- Goblin Mushpot
INSERT INTO vendor_items VALUES (952,17780760,515,0,0,0,0,0,0);	-- Poison Flour
INSERT INTO vendor_items VALUES (1239,17780760,490,0,0,0,0,0,0);	-- Goblin Doll

-- Pelftrix
INSERT INTO vendor_items VALUES (4116,17162831,4500,0,0,0,0,0,0);	-- Hi-Potion
INSERT INTO vendor_items VALUES (4132,17162831,28000,0,0,0,0,0,0);	-- Hi-Ether
INSERT INTO vendor_items VALUES (1020,17162831,300,0,0,0,0,0,0);	-- Sickle
INSERT INTO vendor_items VALUES (1021,17162831,500,0,0,0,0,0,0);	-- Hatchet

-- Peritrage
INSERT INTO vendor_items VALUES (17218,17739800,14158,0,0,0,0,0,0);	-- Zamburak
INSERT INTO vendor_items VALUES (17298,17739800,294,0,0,0,0,0,0);	-- Tathlum
INSERT INTO vendor_items VALUES (17217,17739800,2166,0,0,0,0,0,0);	-- Crossbow
INSERT INTO vendor_items VALUES (17337,17739800,22,0,0,0,0,0,0);	-- Mythril Bolt
INSERT INTO vendor_items VALUES (17216,17739800,165,0,0,0,0,0,0);	-- Light Crossbow
INSERT INTO vendor_items VALUES (17336,17739800,5,0,0,0,0,0,0);	-- Crossbow Bolt

-- Phamelise
INSERT INTO vendor_items VALUES (4372,17719305,44,0,0,0,0,0,0);	-- Giant Sheep Meat
INSERT INTO vendor_items VALUES (622,17719305,44,0,0,0,0,0,0);	-- Dried Marjoram
INSERT INTO vendor_items VALUES (610,17719305,55,0,0,0,0,0,0);	-- San d'Orian Flour
INSERT INTO vendor_items VALUES (611,17719305,36,0,0,0,0,0,0);	-- Rye Flour
INSERT INTO vendor_items VALUES (1840,17719305,1840,0,0,0,0,0,0);	-- Semolina
INSERT INTO vendor_items VALUES (4366,17719305,22,0,0,0,0,0,0);	-- La Theine Cabbage
INSERT INTO vendor_items VALUES (4378,17719305,55,0,0,0,0,0,0);	-- Selbina Milk

-- Pikini-Mikini
INSERT INTO vendor_items VALUES (4150,17797138,2335,0,0,0,0,0,0);	-- Eye Drops
INSERT INTO vendor_items VALUES (4148,17797138,284,0,0,0,0,0,0);	-- Antidote
INSERT INTO vendor_items VALUES (4151,17797138,720,0,0,0,0,0,0);	-- Echo Drops
INSERT INTO vendor_items VALUES (4112,17797138,819,0,0,0,0,0,0);	-- Potion
INSERT INTO vendor_items VALUES (4509,17797138,10,0,0,0,0,0,0);	-- Distilled Water
INSERT INTO vendor_items VALUES (917,17797138,1821,0,0,0,0,0,0);	-- Parchment
INSERT INTO vendor_items VALUES (17395,17797138,9,0,0,0,0,0,0);	-- Lugworm
INSERT INTO vendor_items VALUES (1021,17797138,450,0,0,0,0,0,0);	-- Hatchet
INSERT INTO vendor_items VALUES (4376,17797138,108,0,0,0,0,0,0);	-- Meat Jerky
INSERT INTO vendor_items VALUES (5299,17797138,133,0,0,0,0,0,0);	-- Salsa

-- Pipiroon
INSERT INTO vendor_items VALUES (17313,16994348,1204,0,0,0,0,0,0);	-- Grenade
INSERT INTO vendor_items VALUES (17315,16994348,6000,0,0,0,0,0,0);	-- Riot Grenade
INSERT INTO vendor_items VALUES (928,16994348,515,0,0,0,0,0,0);	-- Bomb Ash
INSERT INTO vendor_items VALUES (2873,16994348,10000,0,0,0,0,0,0);	-- Nashmau Waystone

-- Pirvidiauce
INSERT INTO vendor_items VALUES (12986,17723486,9180,1,0,0,1,0,0);	-- Chestnut Sabbots
INSERT INTO vendor_items VALUES (4128,17723486,4445,1,0,0,1,0,0);	-- Ether
INSERT INTO vendor_items VALUES (4112,17723486,837,1,0,0,1,0,0);	-- Potion
INSERT INTO vendor_items VALUES (17336,17723486,6,2,0,0,0,0,0);	-- Crossbow bolt
INSERT INTO vendor_items VALUES (4151,17723486,720,2,0,0,0,0,0);	-- Echo Drops
INSERT INTO vendor_items VALUES (12985,17723486,1462,2,0,0,0,0,0);	-- Holly Clogs
INSERT INTO vendor_items VALUES (4148,17723486,284,0,0,0,0,0,0);	-- Antidote
INSERT INTO vendor_items VALUES (12984,17723486,111,0,0,0,0,0,0);	-- Ash Clogs
INSERT INTO vendor_items VALUES (219,17723486,900,0,0,0,0,0,0);	-- Ceramic Flowerpot
INSERT INTO vendor_items VALUES (4150,17723486,2335,0,0,0,0,0,0);	-- Eye Drops
INSERT INTO vendor_items VALUES (1774,17723486,1984,0,0,0,0,0,0);	-- Red Gravel
INSERT INTO vendor_items VALUES (17318,17723486,3,0,0,0,0,0,0);	-- Wooden Arrow

-- Pohka Chichiyowahl
INSERT INTO vendor_items VALUES (17388,16793986,1238,0,0,0,0,0,0);	-- Fastwater F. Rod
INSERT INTO vendor_items VALUES (17382,16793986,11845,0,0,0,0,0,0);	-- S.H. Fishing Rod
INSERT INTO vendor_items VALUES (4148,16793986,290,0,0,0,0,0,0);	-- Antidote

-- Poporoon
INSERT INTO vendor_items VALUES (12952,16994349,336,0,0,0,0,0,0);	-- Leather Highboots
INSERT INTO vendor_items VALUES (12953,16994349,3438,0,0,0,0,0,0);	-- Lizard Ledelsens
INSERT INTO vendor_items VALUES (12954,16994349,11172,0,0,0,0,0,0);	-- Studded Boots
INSERT INTO vendor_items VALUES (12955,16994349,20532,0,0,0,0,0,0);	-- Cuir Highboots

-- Posso Ruhbini
INSERT INTO vendor_items VALUES (688,17760317,18,0,0,0,0,0,0);	-- Arrowwood Log
INSERT INTO vendor_items VALUES (698,17760317,87,0,0,0,0,0,0);	-- Ash Log
INSERT INTO vendor_items VALUES (618,17760317,25,0,0,0,0,0,0);	-- Blue Peas
INSERT INTO vendor_items VALUES (621,17760317,25,0,0,0,0,0,0);	-- Crying Mustard

-- Pourette
INSERT INTO vendor_items VALUES (4352,17719493,128,0,0,0,0,0,0);	-- Derfland Pear
INSERT INTO vendor_items VALUES (617,17719493,142,0,0,0,0,0,0);	-- Ginger
INSERT INTO vendor_items VALUES (4545,17719493,62,0,0,0,0,0,0);	-- Gysahl Greens
INSERT INTO vendor_items VALUES (1412,17719493,1656,0,0,0,0,0,0);	-- Olive Flower
INSERT INTO vendor_items VALUES (633,17719493,14,0,0,0,0,0,0);	-- Olive Oil
INSERT INTO vendor_items VALUES (951,17719493,110,0,0,0,0,0,0);	-- Wijnruit

-- Prestapiq
INSERT INTO vendor_items VALUES (640,17752108,11,0,0,0,0,0,0);	-- Copper Ore
INSERT INTO vendor_items VALUES (4450,17752108,694,0,0,0,0,0,0);	-- Coral Fungus
INSERT INTO vendor_items VALUES (4375,17752108,4032,0,0,0,0,0,0);	-- Danceshroom
INSERT INTO vendor_items VALUES (1650,17752108,6500,0,0,0,0,0,0);	-- Kopparnickel Ore
INSERT INTO vendor_items VALUES (5165,17752108,736,0,0,0,0,0,0);	-- Movalpolos Water

-- Proud Beard
INSERT INTO vendor_items VALUES (12631,17735795,276,0,0,0,0,0,0);	-- Hume Tunic
INSERT INTO vendor_items VALUES (12632,17735795,276,0,0,0,0,0,0);	-- Hume Vest
INSERT INTO vendor_items VALUES (12754,17735795,165,0,0,0,0,0,0);	-- Hume M Gloves
INSERT INTO vendor_items VALUES (12760,17735795,165,0,0,0,0,0,0);	-- Hume F Gloves
INSERT INTO vendor_items VALUES (12883,17735795,239,0,0,0,0,0,0);	-- Hume Slacks
INSERT INTO vendor_items VALUES (12884,17735795,239,0,0,0,0,0,0);	-- Hume Pants
INSERT INTO vendor_items VALUES (13005,17735795,165,0,0,0,0,0,0);	-- Hume M Boots
INSERT INTO vendor_items VALUES (13010,17735795,165,0,0,0,0,0,0);	-- Hume F Boots
INSERT INTO vendor_items VALUES (12637,17735795,276,0,0,0,0,0,0);	-- Galkan Surcoat
INSERT INTO vendor_items VALUES (12758,17735795,165,0,0,0,0,0,0);	-- Galkan Bracers
INSERT INTO vendor_items VALUES (12888,17735795,239,0,0,0,0,0,0);	-- Galkan Braguette
INSERT INTO vendor_items VALUES (13009,17735795,165,0,0,0,0,0,0);	-- Galkan Sandals

-- Pyropox
INSERT INTO vendor_items VALUES (4251,17784985,25,0,0,0,0,0,0);	-- Festive Fan
INSERT INTO vendor_items VALUES (4252,17784985,25,0,0,0,0,0,0);	-- Summer Fan
INSERT INTO vendor_items VALUES (4256,17784985,25,0,0,0,0,0,0);	-- Ouka Ranman
INSERT INTO vendor_items VALUES (4184,17784985,50,0,0,0,0,0,0);	-- Kongou Inaho
INSERT INTO vendor_items VALUES (4185,17784985,50,0,0,0,0,0,0);	-- Meifu Goma
INSERT INTO vendor_items VALUES (4253,17784985,50,0,0,0,0,0,0);	-- Spirit Masque
INSERT INTO vendor_items VALUES (5881,17784985,50,0,0,0,0,0,0);	-- Shisai Kaboku
INSERT INTO vendor_items VALUES (4183,17784985,100,0,0,0,0,0,0);	-- Konron Hassen
INSERT INTO vendor_items VALUES (5360,17784985,100,0,0,0,0,0,0);	-- Muteppo
INSERT INTO vendor_items VALUES (5361,17784985,100,0,0,0,0,0,0);	-- Datechochin
INSERT INTO vendor_items VALUES (6268,17784985,150,0,0,0,0,0,0);	-- Komanezumi
INSERT INTO vendor_items VALUES (5884,17784985,250,0,0,0,0,0,0);	-- Rengedama
INSERT INTO vendor_items VALUES (5532,17784985,250,0,0,0,0,0,0);	-- Ichinintousen Koma
INSERT INTO vendor_items VALUES (5725,17784985,300,0,0,0,0,0,0);	-- Goshikitenge

-- Quelpia
INSERT INTO vendor_items VALUES (4610,17793067,585,0,0,0,0,0,0);	-- Scroll of Cure II
INSERT INTO vendor_items VALUES (4611,17793067,3261,0,0,0,0,0,0);	-- Scroll of Cure III
INSERT INTO vendor_items VALUES (4616,17793067,10080,0,0,0,0,0,0);	-- Scroll of Curaga II
INSERT INTO vendor_items VALUES (4620,17793067,5178,0,0,0,0,0,0);	-- Scroll of Raise
INSERT INTO vendor_items VALUES (4629,17793067,31500,0,0,0,0,0,0);	-- Scroll of Holy
INSERT INTO vendor_items VALUES (4632,17793067,10080,0,0,0,0,0,0);	-- Scroll of Dia II
INSERT INTO vendor_items VALUES (4637,17793067,8100,0,0,0,0,0,0);	-- Scroll of Banish II
INSERT INTO vendor_items VALUES (4652,17793067,6366,0,0,0,0,0,0);	-- Scroll of Protect II
INSERT INTO vendor_items VALUES (4657,17793067,15840,0,0,0,0,0,0);	-- Scroll of Shell II
INSERT INTO vendor_items VALUES (4665,17793067,18000,0,0,0,0,0,0);	-- Scroll of Haste
INSERT INTO vendor_items VALUES (4708,17793067,4644,0,0,0,0,0,0);	-- Scroll of Enfire
INSERT INTO vendor_items VALUES (4709,17793067,3688,0,0,0,0,0,0);	-- Scroll of Enblizzard
INSERT INTO vendor_items VALUES (4710,17793067,2250,0,0,0,0,0,0);	-- Scroll of Enaero
INSERT INTO vendor_items VALUES (4711,17793067,1827,0,0,0,0,0,0);	-- Scroll of Enstone
INSERT INTO vendor_items VALUES (4712,17793067,1363,0,0,0,0,0,0);	-- Scroll of Enthunder
INSERT INTO vendor_items VALUES (4713,17793067,6366,0,0,0,0,0,0);	-- Scroll of Enwater

-- Quesse
INSERT INTO vendor_items VALUES (845,17764454,1150,0,0,1,0,0,1);	-- Black Chocobo Feather
INSERT INTO vendor_items VALUES (17307,17764454,9,0,0,2,0,0,0);	-- Dart
INSERT INTO vendor_items VALUES (4545,17764454,62,0,0,0,0,0,0);	-- Gysahl Greens
INSERT INTO vendor_items VALUES (840,17764454,7,0,0,0,0,0,0);	-- Chocobo Feather
INSERT INTO vendor_items VALUES (17016,17764454,11,0,0,0,0,0,0);	-- Pet Food Alpha Biscuit
INSERT INTO vendor_items VALUES (17017,17764454,82,0,0,0,0,0,0);	-- Pet Food Beta Biscuit
INSERT INTO vendor_items VALUES (17860,17764454,82,0,0,0,0,0,0);	-- Carrot Broth
INSERT INTO vendor_items VALUES (17862,17764454,695,0,0,0,0,0,0);	-- Bug Broth
INSERT INTO vendor_items VALUES (17864,17764454,126,0,0,0,0,0,0);	-- Herbal Broth
INSERT INTO vendor_items VALUES (17866,17764454,695,0,0,0,0,0,0);	-- Carrion Broth
INSERT INTO vendor_items VALUES (5073,17764454,50784,0,0,0,0,0,0);	-- Scroll of Chocobo Mazurka

-- Raghd
INSERT INTO vendor_items VALUES (13456,17739811,1150,0,1,0,0,1,0);	-- Silver Ring
INSERT INTO vendor_items VALUES (13327,17739811,1150,0,1,0,0,1,0);	-- Silver Earring
INSERT INTO vendor_items VALUES (13465,17739811,184,0,2,0,0,0,0);	-- Brass Ring
INSERT INTO vendor_items VALUES (13454,17739811,69,0,0,0,0,0,0);	-- Copper Ring

-- Regine
INSERT INTO vendor_items VALUES (4641,17318611,1165,1,0,0,1,0,0);	-- Scroll of Diaga
INSERT INTO vendor_items VALUES (4664,17318611,837,1,0,0,1,0,0);	-- Scroll of Slow
INSERT INTO vendor_items VALUES (4662,17318611,7025,1,0,0,1,0,0);	-- Scroll of Stoneskin
INSERT INTO vendor_items VALUES (4636,17318611,140,2,0,0,0,0,0);	-- Scroll of Banish
INSERT INTO vendor_items VALUES (4646,17318611,1165,2,0,0,0,0,0);	-- Scroll of Banishga
INSERT INTO vendor_items VALUES (4661,17318611,2097,2,0,0,0,0,0);	-- Scroll of Blink
INSERT INTO vendor_items VALUES (4610,17318611,585,2,0,0,0,0,0);	-- Scroll of Cure II
INSERT INTO vendor_items VALUES (4663,17318611,360,0,0,0,0,0,0);	-- Scroll of Aquaveil
INSERT INTO vendor_items VALUES (4624,17318611,990,0,0,0,0,0,0);	-- Scroll of Blindna
INSERT INTO vendor_items VALUES (4615,17318611,1363,0,0,0,0,0,0);	-- Scroll of Curaga
INSERT INTO vendor_items VALUES (4609,17318611,61,0,0,0,0,0,0);	-- Scroll of Cure
INSERT INTO vendor_items VALUES (4631,17318611,82,0,0,0,0,0,0);	-- Scroll of Dia
INSERT INTO vendor_items VALUES (4623,17318611,324,0,0,0,0,0,0);	-- Scroll of Paralyna
INSERT INTO vendor_items VALUES (4622,17318611,180,0,0,0,0,0,0);	-- Scroll of Poisona
INSERT INTO vendor_items VALUES (4651,17318611,219,0,0,0,0,0,0);	-- Scroll of Protect
INSERT INTO vendor_items VALUES (4656,17318611,1584,0,0,0,0,0,0);	-- Scroll of Shell
INSERT INTO vendor_items VALUES (4862,17318611,111,1,0,0,1,0,0);	-- Scroll of Blind
INSERT INTO vendor_items VALUES (4838,17318611,360,2,0,0,0,0,0);	-- Scroll of Bio
INSERT INTO vendor_items VALUES (4828,17318611,82,2,0,0,0,0,0);	-- Scroll of Poison
INSERT INTO vendor_items VALUES (4861,17318611,2250,2,0,0,0,0,0);	-- Scroll of Sleep
INSERT INTO vendor_items VALUES (4762,17318611,324,0,0,0,0,0,0);	-- Scroll of Aero
INSERT INTO vendor_items VALUES (4757,17318611,1584,0,0,0,0,0,0);	-- Scroll of Blizzard
INSERT INTO vendor_items VALUES (4843,17318611,4644,0,0,0,0,0,0);	-- Scroll of Burn
INSERT INTO vendor_items VALUES (4845,17318611,2250,0,0,0,0,0,0);	-- Scroll of Choke
INSERT INTO vendor_items VALUES (4848,17318611,6366,0,0,0,0,0,0);	-- Scroll of Drown
INSERT INTO vendor_items VALUES (4752,17318611,837,0,0,0,0,0,0);	-- Scroll of Fire
INSERT INTO vendor_items VALUES (4844,17318611,3688,0,0,0,0,0,0);	-- Scroll of Frost
INSERT INTO vendor_items VALUES (4846,17318611,1827,0,0,0,0,0,0);	-- Scroll of Rasp
INSERT INTO vendor_items VALUES (4847,17318611,1363,0,0,0,0,0,0);	-- Scroll of Shock
INSERT INTO vendor_items VALUES (4767,17318611,61,0,0,0,0,0,0);	-- Scroll of Stone
INSERT INTO vendor_items VALUES (4772,17318611,3261,0,0,0,0,0,0);	-- Scroll of Thunder
INSERT INTO vendor_items VALUES (4777,17318611,140,0,0,0,0,0,0);	-- Scroll of Water

-- Rhimonne
INSERT INTO vendor_items VALUES (4545,17780869,62,0,0,0,0,0,0);	-- Gysahl Greens
INSERT INTO vendor_items VALUES (840,17780869,4,0,0,0,0,0,0);	-- Chocobo Feather
INSERT INTO vendor_items VALUES (17307,17780869,9,0,0,0,0,0,0);	-- Dart

-- Rodellieux
INSERT INTO vendor_items VALUES (4571,17735743,90,0,0,0,0,0,0);	-- Beaugreens
INSERT INTO vendor_items VALUES (4363,17735743,39,0,0,0,0,0,0);	-- Faerie Apple
INSERT INTO vendor_items VALUES (691,17735743,54,0,0,0,0,0,0);	-- Maple Log

-- Rosswald
INSERT INTO vendor_items VALUES (4372,17743933,44,0,0,0,0,0,0);	-- Giant Sheep Meat
INSERT INTO vendor_items VALUES (622,17743933,44,0,0,0,0,0,0);	-- Dried Marjoram
INSERT INTO vendor_items VALUES (610,17743933,55,0,0,0,0,0,0);	-- San d'Orian Flour
INSERT INTO vendor_items VALUES (611,17743933,36,0,0,0,0,0,0);	-- Rye Flour
INSERT INTO vendor_items VALUES (1840,17743933,1840,0,0,0,0,0,0);	-- Semolina
INSERT INTO vendor_items VALUES (4366,17743933,22,0,0,0,0,0,0);	-- La Theine Cabbage
INSERT INTO vendor_items VALUES (4378,17743933,55,0,0,0,0,0,0);	-- Selbina Milk

-- Rubahah
INSERT INTO vendor_items VALUES (629,16982090,48,0,0,0,0,0,0);	-- Millioncorn
INSERT INTO vendor_items VALUES (2237,16982090,60,0,0,0,0,0,0);	-- Imperial Flour (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (2214,16982090,68,0,0,0,0,0,0);	-- Imperial Rice (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (2271,16982090,316,0,0,0,0,0,0);	-- Coffee Beans (Requires Astral Candescence)

-- Runito-Monito
INSERT INTO vendor_items VALUES (16405,17797127,106,0,0,0,0,0,0);	-- Cat Bagnakhs
INSERT INTO vendor_items VALUES (16407,17797127,1554,0,0,0,0,0,0);	-- Brass Bagnakhs
INSERT INTO vendor_items VALUES (16449,17797127,855,0,0,0,0,0,0);	-- Brass Dagger
INSERT INTO vendor_items VALUES (17059,17797127,92,0,0,0,0,0,0);	-- Bronze Rod
INSERT INTO vendor_items VALUES (17081,17797127,634,0,0,0,0,0,0);	-- Brass Rod
INSERT INTO vendor_items VALUES (16531,17797127,3601,0,0,0,0,0,0);	-- Brass Xiphos
INSERT INTO vendor_items VALUES (16583,17797127,2502,0,0,0,0,0,0);	-- Claymore
INSERT INTO vendor_items VALUES (16704,17797127,618,0,0,0,0,0,0);	-- Butterfly Axe
INSERT INTO vendor_items VALUES (17307,17797127,9,0,0,0,0,0,0);	-- Dart
INSERT INTO vendor_items VALUES (17318,17797127,3,0,0,0,0,0,0);	-- Wooden Arrow
INSERT INTO vendor_items VALUES (17319,17797127,4,0,0,0,0,0,0);	-- Bone Arrow
INSERT INTO vendor_items VALUES (17336,17797127,5,0,0,0,0,0,0);	-- Crossbow Bolts

-- Ryan
INSERT INTO vendor_items VALUES (16640,17760404,290,0,0,0,0,0,0);	-- Bronze Axe
INSERT INTO vendor_items VALUES (16535,17760404,246,0,0,0,0,0,0);	-- Bronze Sword
INSERT INTO vendor_items VALUES (17336,17760404,5,0,0,0,0,0,0);	-- Crossbow Bolt
INSERT INTO vendor_items VALUES (12576,17760404,235,0,0,0,0,0,0);	-- Bronze Harness
INSERT INTO vendor_items VALUES (12577,17760404,2286,0,0,0,0,0,0);	-- Brass Harness
INSERT INTO vendor_items VALUES (12704,17760404,128,0,0,0,0,0,0);	-- Bronze Mittens
INSERT INTO vendor_items VALUES (12705,17760404,1255,0,0,0,0,0,0);	-- Brass Mittens
INSERT INTO vendor_items VALUES (12832,17760404,191,0,0,0,0,0,0);	-- Bronze Subligar
INSERT INTO vendor_items VALUES (12833,17760404,1840,0,0,0,0,0,0);	-- Brass Subligar
INSERT INTO vendor_items VALUES (12960,17760404,117,0,0,0,0,0,0);	-- Bronze Leggings
INSERT INTO vendor_items VALUES (12961,17760404,1140,0,0,0,0,0,0);	-- Brass Leggings
INSERT INTO vendor_items VALUES (12584,17760404,1145,0,0,0,0,0,0);	-- Kenpogi
INSERT INTO vendor_items VALUES (12712,17760404,630,0,0,0,0,0,0);	-- Tekko
INSERT INTO vendor_items VALUES (12840,17760404,915,0,0,0,0,0,0);	-- Sitabaki
INSERT INTO vendor_items VALUES (12968,17760404,584,0,0,0,0,0,0);	-- Kyahan

-- Saluhwa
INSERT INTO vendor_items VALUES (12290,16982092,605,0,0,0,0,0,0);	-- Mapple Shield (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (12291,16982092,1815,0,0,0,0,0,0);	-- Elm Shield (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (12292,16982092,4980,0,0,0,0,0,0);	-- Mahogany Shield (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (12293,16982092,15600,0,0,0,0,0,0);	-- Oak Shield (Requires Astral Candescence)
INSERT INTO vendor_items VALUES (12295,16982092,64791,0,0,0,0,0,0);	-- Round Shield (Requires Astral Candescence)

-- Sattsuh Ahkanpari
INSERT INTO vendor_items VALUES (1413,17760436,1656,0,0,0,0,0,0);	-- Cattleya
INSERT INTO vendor_items VALUES (628,17760436,239,0,0,0,0,0,0);	-- Cinnamon
INSERT INTO vendor_items VALUES (4468,17760436,73,0,0,0,0,0,0);	-- Pamamas
INSERT INTO vendor_items VALUES (721,17760436,147,0,0,0,0,0,0);	-- Rattan Lumber

-- Sawyer
INSERT INTO vendor_items VALUES (4591,17743887,147,0,1,0,0,1,0);	-- Pumpernickel
INSERT INTO vendor_items VALUES (4417,17743887,3036,0,1,0,0,1,0);	-- Egg Soup
INSERT INTO vendor_items VALUES (4442,17743887,368,0,1,0,0,1,0);	-- Pineapple Juice
INSERT INTO vendor_items VALUES (4391,17743887,22,0,2,0,0,0,0);	-- Bretzel
INSERT INTO vendor_items VALUES (4578,17743887,143,0,2,0,0,0,0);	-- Sausage
INSERT INTO vendor_items VALUES (4424,17743887,1012,0,2,0,0,0,0);	-- Melon Juice
INSERT INTO vendor_items VALUES (4437,17743887,662,0,2,0,0,0,0);	-- Roast Mutton
INSERT INTO vendor_items VALUES (4499,17743887,92,0,0,0,0,0,0);	-- Iron Bread
INSERT INTO vendor_items VALUES (4436,17743887,294,0,0,0,0,0,0);	-- Baked Popoto
INSERT INTO vendor_items VALUES (4455,17743887,184,0,0,0,0,0,0);	-- Pebble Soup
INSERT INTO vendor_items VALUES (4509,17743887,10,0,0,0,0,0,0);	-- Distilled Water

-- Scamplix
INSERT INTO vendor_items VALUES (4509,17788946,10,0,0,0,0,0,0);	-- Distilled Waterr
INSERT INTO vendor_items VALUES (4376,17788946,108,0,0,0,0,0,0);	-- Meat Jerky
INSERT INTO vendor_items VALUES (4458,17788946,270,0,0,0,0,0,0);	-- Goblin Bread
INSERT INTO vendor_items VALUES (1817,17788946,720,0,0,0,0,0,0);	-- Cactus Arm
INSERT INTO vendor_items VALUES (4128,17788946,4348,0,0,0,0,0,0);	-- Ether
INSERT INTO vendor_items VALUES (4412,17788946,292,0,0,0,0,0,0);	-- Thundermelon
INSERT INTO vendor_items VALUES (4491,17788946,180,0,0,0,0,0,0);	-- Watermelon
INSERT INTO vendor_items VALUES (4112,17788946,819,0,0,0,0,0,0);	-- Potion
INSERT INTO vendor_items VALUES (4148,17788946,284,0,0,0,0,0,0);	-- Antidote
INSERT INTO vendor_items VALUES (4163,17788946,1080,0,0,0,0,0,0);	-- Blinding Potion
INSERT INTO vendor_items VALUES (13328,17788946,4050,0,0,0,0,0,0);	-- Mythril Earring
INSERT INTO vendor_items VALUES (107,17788946,180,0,0,0,0,0,0);	-- Water Jug
INSERT INTO vendor_items VALUES (2868,17788946,9000,0,0,0,0,0,0);	-- Rabao Waystone

-- Sheia Pohrichamaha
INSERT INTO vendor_items VALUES (4571,17760318,90,0,0,0,0,0,0);	-- Beaugreens
INSERT INTO vendor_items VALUES (4363,17760318,39,0,0,0,0,0,0);	-- Faerie Apple
INSERT INTO vendor_items VALUES (691,17760318,54,0,0,0,0,0,0);	-- Maple Log

-- Shilah
INSERT INTO vendor_items VALUES (4434,17719321,4500,1,0,0,1,0,0);	-- Mushroom Risotto
INSERT INTO vendor_items VALUES (4419,17719321,6300,1,0,0,1,0,0);	-- Mushroom Soup
INSERT INTO vendor_items VALUES (4494,17719321,2494,1,0,0,1,0,0);	-- Sah d'Orian Tea
INSERT INTO vendor_items VALUES (4356,17719321,180,2,0,0,0,0,0);	-- White Bread
INSERT INTO vendor_items VALUES (4533,17719321,1080,2,0,0,0,0,0);	-- Delicious Puls
INSERT INTO vendor_items VALUES (4560,17719321,1355,2,0,0,0,0,0);	-- Vegetable Soup
INSERT INTO vendor_items VALUES (4572,17719321,1669,2,0,0,0,0,0);	-- Beaugreen Saute
INSERT INTO vendor_items VALUES (4441,17719321,837,2,0,0,0,0,0);	-- Grape Juice
INSERT INTO vendor_items VALUES (4364,17719321,108,0,0,0,0,0,0);	-- Black Bread
INSERT INTO vendor_items VALUES (4492,17719321,540,0,0,0,0,0,0);	-- Puls
INSERT INTO vendor_items VALUES (4455,17719321,180,0,0,0,0,0,0);	-- Pebble Soup
INSERT INTO vendor_items VALUES (4509,17719321,10,0,0,0,0,0,0);	-- Distilled Water
INSERT INTO vendor_items VALUES (5541,17719321,1260,0,0,0,0,0,0);	-- Royal Grape

-- Shiny Teeth
INSERT INTO vendor_items VALUES (16450,17788943,1867,0,0,0,0,0,0);	-- Dagger
INSERT INTO vendor_items VALUES (16460,17788943,11128,0,0,0,0,0,0);	-- Kris
INSERT INTO vendor_items VALUES (16466,17788943,2231,0,0,0,0,0,0);	-- Knife
INSERT INTO vendor_items VALUES (16552,17788943,4163,0,0,0,0,0,0);	-- Scimitar
INSERT INTO vendor_items VALUES (16553,17788943,35308,0,0,0,0,0,0);	-- Tulwar
INSERT INTO vendor_items VALUES (16558,17788943,62560,0,0,0,0,0,0);	-- Falchion
INSERT INTO vendor_items VALUES (17060,17788943,2439,0,0,0,0,0,0);	-- Rod
INSERT INTO vendor_items VALUES (16401,17788943,103803,0,0,0,0,0,0);	-- Jamadhars
INSERT INTO vendor_items VALUES (17155,17788943,23887,0,0,0,0,0,0);	-- Composite Bow
INSERT INTO vendor_items VALUES (17298,17788943,294,0,0,0,0,0,0);	-- Tathlum
INSERT INTO vendor_items VALUES (17320,17788943,7,0,0,0,0,0,0);	-- Iron Arrow
INSERT INTO vendor_items VALUES (17340,17788943,92,0,0,0,0,0,0);	-- Bullet
INSERT INTO vendor_items VALUES (17315,17788943,5460,0,0,0,0,0,0);	-- Riot Grenade
INSERT INTO vendor_items VALUES (17284,17788943,8996,0,0,0,0,0,0);	-- Chakram

-- Shohrun-Tuhrun
INSERT INTO vendor_items VALUES (4665,17752095,18000,0,0,1,0,0,1);	-- Haste
INSERT INTO vendor_items VALUES (4620,17752095,5178,0,0,2,0,0,0);	-- Scroll of Raise
INSERT INTO vendor_items VALUES (4632,17752095,10080,0,0,2,0,0,0);	-- Scroll of Dia II
INSERT INTO vendor_items VALUES (4637,17752095,8100,0,0,2,0,0,0);	-- Scroll of Banish II
INSERT INTO vendor_items VALUES (4652,17752095,6366,0,0,2,0,0,0);	-- Scroll of Protect II
INSERT INTO vendor_items VALUES (4657,17752095,15840,0,0,2,0,0,0);	-- Scroll of Shell II
INSERT INTO vendor_items VALUES (4708,17752095,4644,0,0,2,0,0,0);	-- Scroll of Enfire
INSERT INTO vendor_items VALUES (4709,17752095,3688,0,0,2,0,0,0);	-- Scroll of Enblizzard
INSERT INTO vendor_items VALUES (4710,17752095,2250,0,0,2,0,0,0);	-- Scroll of Enaero
INSERT INTO vendor_items VALUES (4711,17752095,1827,0,0,2,0,0,0);	-- Scroll of Enstone
INSERT INTO vendor_items VALUES (4712,17752095,1363,0,0,2,0,0,0);	-- Scroll of Enthunder
INSERT INTO vendor_items VALUES (4713,17752095,6366,0,0,2,0,0,0);	-- Scroll of Enwater
INSERT INTO vendor_items VALUES (4611,17752095,3261,0,0,0,0,0,0);	-- Scroll of Cure III
INSERT INTO vendor_items VALUES (4654,17752095,78200,0,0,0,0,0,0);	-- Scroll of Protect IV
INSERT INTO vendor_items VALUES (4736,17752095,74520,0,0,0,0,0,0);	-- Scroll of Protectra IV
INSERT INTO vendor_items VALUES (4868,17752095,64400,0,0,0,0,0,0);	-- Scroll of Dispel

-- Silke
INSERT INTO vendor_items VALUES (6059,17134152,29925,0,0,0,0,0,0);	-- Animus Augeo Schema
INSERT INTO vendor_items VALUES (6060,17134152,29925,0,0,0,0,0,0);	-- Animus Minuo Schema
INSERT INTO vendor_items VALUES (6061,17134152,36300,0,0,0,0,0,0);	-- Adloquim Schema

-- Solby-Maholby
INSERT INTO vendor_items VALUES (17395,17809502,9,0,0,0,0,0,0);	-- Lugworm
INSERT INTO vendor_items VALUES (4899,17809502,450,0,0,0,0,0,0);	-- Earth Spirit Pact

-- Somn-Paemn
INSERT INTO vendor_items VALUES (689,17739822,33,0,0,0,0,0,0);	-- Lauan Log
INSERT INTO vendor_items VALUES (619,17739822,43,0,0,0,0,0,0);	-- Popoto
INSERT INTO vendor_items VALUES (4444,17739822,22,0,0,0,0,0,0);	-- Rarab Tail
INSERT INTO vendor_items VALUES (4392,17739822,29,0,0,0,0,0,0);	-- Saruta Orange
INSERT INTO vendor_items VALUES (635,17739822,18,0,0,0,0,0,0);	-- Windurstian Tea Leaves

-- Sororo
INSERT INTO vendor_items VALUES (4641,17739807,1165,0,1,0,0,1,0);	-- Diaga
INSERT INTO vendor_items VALUES (4662,17739807,7025,0,1,0,0,1,0);	-- Stoneskin
INSERT INTO vendor_items VALUES (4664,17739807,837,0,1,0,0,1,0);	-- Slow
INSERT INTO vendor_items VALUES (4610,17739807,585,0,2,0,0,0,0);	-- Cure II
INSERT INTO vendor_items VALUES (4636,17739807,140,0,2,0,0,0,0);	-- Banish
INSERT INTO vendor_items VALUES (4646,17739807,1165,0,2,0,0,0,0);	-- Banishga
INSERT INTO vendor_items VALUES (4661,17739807,2097,0,2,0,0,0,0);	-- Blink
INSERT INTO vendor_items VALUES (4608,17739807,61,0,0,0,0,0,0);	-- Cure
INSERT INTO vendor_items VALUES (4615,17739807,1363,0,0,0,0,0,0);	-- Curaga
INSERT INTO vendor_items VALUES (4622,17739807,180,0,0,0,0,0,0);	-- Poisona
INSERT INTO vendor_items VALUES (4623,17739807,324,0,0,0,0,0,0);	-- Paralyna
INSERT INTO vendor_items VALUES (4624,17739807,990,0,0,0,0,0,0);	-- Blindna
INSERT INTO vendor_items VALUES (4606,17739807,82,0,0,0,0,0,0);	-- Dia
INSERT INTO vendor_items VALUES (4651,17739807,219,0,0,0,0,0,0);	-- Protect
INSERT INTO vendor_items VALUES (4656,17739807,1584,0,0,0,0,0,0);	-- Shell
INSERT INTO vendor_items VALUES (4721,17739807,29700,0,0,0,0,0,0);	-- 4721, 29700, 3, -- Repose (WoTG)
INSERT INTO vendor_items VALUES (4663,17739807,368,0,0,0,0,0,0);	-- Aquaveil

-- Spondulix
INSERT INTO vendor_items VALUES (4116,17171113,4500,0,0,0,0,0,0);	-- Hi-Potion
INSERT INTO vendor_items VALUES (4132,17171113,28000,0,0,0,0,0,0);	-- Hi-Ether
INSERT INTO vendor_items VALUES (2563,17171113,3035,0,0,0,0,0,0);	-- Karugo Clay

-- Stinknix
INSERT INTO vendor_items VALUES (943,17780841,294,0,0,0,0,0,0);	-- Poison Dust
INSERT INTO vendor_items VALUES (944,17780841,1035,0,0,0,0,0,0);	-- Venom Dust
INSERT INTO vendor_items VALUES (945,17780841,2000,0,0,0,0,0,0);	-- Paralysis Dust
INSERT INTO vendor_items VALUES (17320,17780841,7,0,0,0,0,0,0);	-- Iron Arrow
INSERT INTO vendor_items VALUES (17336,17780841,5,0,0,0,0,0,0);	-- Crossbow Bolt
INSERT INTO vendor_items VALUES (17313,17780841,1107,0,0,0,0,0,0);	-- Grenade

-- Sugandhi
INSERT INTO vendor_items VALUES (16473,16839271,5589,0,1,0,0,1,0);	-- Kukri
INSERT INTO vendor_items VALUES (16545,16839271,21067,0,1,0,0,1,0);	-- Broadsword
INSERT INTO vendor_items VALUES (16513,16839271,11588,0,1,0,0,1,0);	-- Tuck
INSERT INTO vendor_items VALUES (16558,16839271,61200,0,1,0,0,1,0);	-- Falchion
INSERT INTO vendor_items VALUES (16466,16839271,2182,0,2,0,0,0,0);	-- Knife
INSERT INTO vendor_items VALUES (16537,16839271,30960,0,2,0,0,0,0);	-- Mythril Sword
INSERT INTO vendor_items VALUES (16552,16839271,4072,0,2,0,0,0,0);	-- Scimitar
INSERT INTO vendor_items VALUES (16465,16839271,147,0,0,0,0,0,0);	-- Bronze Knife
INSERT INTO vendor_items VALUES (16405,16839271,104,0,0,0,0,0,0);	-- Cat Baghnakhs
INSERT INTO vendor_items VALUES (16535,16839271,241,0,0,0,0,0,0);	-- Bronze Sword
INSERT INTO vendor_items VALUES (16536,16839271,7128,0,0,0,0,0,0);	-- Iron Sword
INSERT INTO vendor_items VALUES (16517,16839271,9201,0,0,0,0,0,0);	-- Degen
INSERT INTO vendor_items VALUES (16551,16839271,698,0,0,0,0,0,0);	-- Sapara

-- Susu
INSERT INTO vendor_items VALUES (4647,17780867,20000,0,0,0,0,0,0);	-- Scroll of Banishga II
INSERT INTO vendor_items VALUES (4683,17780867,2030,0,0,0,0,0,0);	-- Scroll of Barblind
INSERT INTO vendor_items VALUES (4697,17780867,2030,0,0,0,0,0,0);	-- Scroll of Barblindra
INSERT INTO vendor_items VALUES (4682,17780867,780,0,0,0,0,0,0);	-- Scroll of Barparalyze
INSERT INTO vendor_items VALUES (4696,17780867,780,0,0,0,0,0,0);	-- Scroll of Barparalyzra
INSERT INTO vendor_items VALUES (4681,17780867,400,0,0,0,0,0,0);	-- Scroll of Barpoison
INSERT INTO vendor_items VALUES (4695,17780867,400,0,0,0,0,0,0);	-- Scroll of Barpoisonra
INSERT INTO vendor_items VALUES (4684,17780867,4608,0,0,0,0,0,0);	-- Scroll of Barsilence
INSERT INTO vendor_items VALUES (4698,17780867,4608,0,0,0,0,0,0);	-- Scroll of Barsilencera
INSERT INTO vendor_items VALUES (4680,17780867,244,0,0,0,0,0,0);	-- Scroll of Barsleep
INSERT INTO vendor_items VALUES (4694,17780867,244,0,0,0,0,0,0);	-- Scroll of Barsleepra
INSERT INTO vendor_items VALUES (4628,17780867,8586,0,0,0,0,0,0);	-- Scroll of Cursna
INSERT INTO vendor_items VALUES (4629,17780867,35000,0,0,0,0,0,0);	-- Scroll of Holy
INSERT INTO vendor_items VALUES (4625,17780867,2330,0,0,0,0,0,0);	-- Scroll of Silena
INSERT INTO vendor_items VALUES (4626,17780867,19200,0,0,0,0,0,0);	-- Scroll of Stona
INSERT INTO vendor_items VALUES (4627,17780867,13300,0,0,0,0,0,0);	-- Scroll of Viruna

-- Taajiji
INSERT INTO vendor_items VALUES (4411,17752100,756,0,0,1,0,0,1);	-- Dhalmel Pie
INSERT INTO vendor_items VALUES (4434,17752100,5050,0,0,1,0,0,1);	-- Mushroom Risotto
INSERT INTO vendor_items VALUES (4554,17752100,12762,0,0,1,0,0,1);	-- Shallops Tropicale
INSERT INTO vendor_items VALUES (4393,17752100,984,0,0,1,0,0,1);	-- Orange Kuchen
INSERT INTO vendor_items VALUES (4506,17752100,5216,0,0,2,0,0,0);	-- Mutton Tortilla
INSERT INTO vendor_items VALUES (4440,17752100,6064,0,0,2,0,0,0);	-- Whitefish Stew
INSERT INTO vendor_items VALUES (4572,17752100,1669,0,0,2,0,0,0);	-- Beaugreen Saute
INSERT INTO vendor_items VALUES (4422,17752100,184,0,0,2,0,0,0);	-- Orange Juice
INSERT INTO vendor_items VALUES (4438,17752100,1324,0,0,2,0,0,0);	-- Dhalmel Steak
INSERT INTO vendor_items VALUES (4408,17752100,128,0,0,0,0,0,0);	-- Tortilla
INSERT INTO vendor_items VALUES (4492,17752100,552,0,0,0,0,0,0);	-- Puls
INSERT INTO vendor_items VALUES (4433,17752100,2387,0,0,0,0,0,0);	-- Dhalmel Stew
INSERT INTO vendor_items VALUES (4509,17752100,10,0,0,0,0,0,0);	-- Distilled Water
INSERT INTO vendor_items VALUES (4493,17752100,184,0,0,0,0,0,0);	-- Windurstian Tea
INSERT INTO vendor_items VALUES (4555,17752100,1711,0,0,0,0,0,0);	-- Windurst Salad

-- Tahn Posbei
INSERT INTO vendor_items VALUES (12289,17801254,110,0,0,0,0,0,0);	-- Lauan Shield
INSERT INTO vendor_items VALUES (12292,17801254,4531,0,0,0,0,0,0);	-- Mahogany Shield
INSERT INTO vendor_items VALUES (12295,17801254,59607,0,0,0,0,0,0);	-- Round Shield
INSERT INTO vendor_items VALUES (12455,17801254,7026,0,0,0,0,0,0);	-- Beetle Mask
INSERT INTO vendor_items VALUES (12583,17801254,10833,0,0,0,0,0,0);	-- Beetle Harness
INSERT INTO vendor_items VALUES (12711,17801254,5707,0,0,0,0,0,0);	-- Beetle Mittens
INSERT INTO vendor_items VALUES (12835,17801254,8666,0,0,0,0,0,0);	-- Beetle Subligar
INSERT INTO vendor_items VALUES (12967,17801254,5332,0,0,0,0,0,0);	-- Beetre Leggins
INSERT INTO vendor_items VALUES (12440,17801254,404,0,0,0,0,0,0);	-- Leather Bandana
INSERT INTO vendor_items VALUES (12568,17801254,618,0,0,0,0,0,0);	-- Leather Vest
INSERT INTO vendor_items VALUES (12696,17801254,331,0,0,0,0,0,0);	-- Leather Gloves
INSERT INTO vendor_items VALUES (12952,17801254,309,0,0,0,0,0,0);	-- Leather Highboots
INSERT INTO vendor_items VALUES (13092,17801254,28777,0,0,0,0,0,0);	-- Coeurl Gorget

-- Takiyah
INSERT INTO vendor_items VALUES (954,17748139,4121,0,0,0,0,0,0);	-- Magic Pot Shard

-- Taniko-Maniko
INSERT INTO vendor_items VALUES (16769,17760314,2542,0,0,0,0,0,0);	-- Brass Zaghnal
INSERT INTO vendor_items VALUES (17154,17760314,7999,0,0,0,0,0,0);	-- Wrapped Bow
INSERT INTO vendor_items VALUES (17323,17760314,141,0,0,0,0,0,0);	-- Ice Arrow
INSERT INTO vendor_items VALUES (17324,17760314,141,0,0,0,0,0,0);	-- Lighning Arrow
INSERT INTO vendor_items VALUES (16405,17760314,104,0,0,0,0,0,0);	-- Cat Baghnakhs
INSERT INTO vendor_items VALUES (16385,17760314,129,0,0,0,0,0,0);	-- Cesti
INSERT INTO vendor_items VALUES (16649,17760314,5864,0,0,2,0,0,0);	-- Bone Pick
INSERT INTO vendor_items VALUES (17153,17760314,493,0,0,0,0,0,0);	-- Self Bow
INSERT INTO vendor_items VALUES (17318,17760314,3,0,0,0,0,0,0);	-- Wooden Arrow
INSERT INTO vendor_items VALUES (17308,17760314,55,0,0,0,0,0,0);	-- Hawkeye
INSERT INTO vendor_items VALUES (17280,17760314,1610,0,0,0,0,0,0);	-- Boomerang
INSERT INTO vendor_items VALUES (16642,17760314,4198,0,0,0,0,0,0);	-- Bone Axe
INSERT INTO vendor_items VALUES (16768,17760314,309,0,0,0,0,0,0);	-- Bronze Zaghnal
INSERT INTO vendor_items VALUES (16832,17760314,97,0,0,0,0,0,0);	-- Harpoon
INSERT INTO vendor_items VALUES (17152,17760314,40,0,0,0,0,0,0);	-- Bone Axe
INSERT INTO vendor_items VALUES (17319,17760314,1610,0,0,0,0,0,0);	-- Bone Arrow

-- Taraihi-Perunhi
INSERT INTO vendor_items VALUES (4352,17670767,128,0,0,0,0,0,0);	-- Derfland Pear
INSERT INTO vendor_items VALUES (617,17670767,142,0,0,0,0,0,0);	-- Ginger
INSERT INTO vendor_items VALUES (4545,17670767,62,0,0,0,0,0,0);	-- Gysahl Greens
INSERT INTO vendor_items VALUES (1412,17670767,1656,0,0,0,0,0,0);	-- Olive Flower
INSERT INTO vendor_items VALUES (633,17670767,14,0,0,0,0,0,0);	-- Olive Oil
INSERT INTO vendor_items VALUES (951,17670767,110,0,0,0,0,0,0);	-- Wijnruit

-- Tavourine
INSERT INTO vendor_items VALUES (16584,17723447,37800,1,0,0,1,0,0);	-- Mythril Claymore
INSERT INTO vendor_items VALUES (16466,17723447,2182,1,0,0,1,0,0);	-- Knife
INSERT INTO vendor_items VALUES (17060,17723447,2386,1,0,0,1,0,0);	-- Rod
INSERT INTO vendor_items VALUES (16640,17723447,284,2,0,0,0,0,0);	-- Bronze Axe
INSERT INTO vendor_items VALUES (16465,17723447,147,2,0,0,0,0,0);	-- Bronze Knife
INSERT INTO vendor_items VALUES (17081,17723447,621,2,0,0,0,0,0);	-- Brass Rod
INSERT INTO vendor_items VALUES (16583,17723447,2448,2,0,0,0,0,0);	-- Claymore
INSERT INTO vendor_items VALUES (17035,17723447,4363,2,0,0,0,0,0);	-- Mace
INSERT INTO vendor_items VALUES (17034,17723447,169,0,0,0,0,0,0);	-- Bronze Mace

-- Taza
INSERT INTO vendor_items VALUES (4881,17780868,10304,0,0,0,0,0,0);	-- Scroll of Sleepga
INSERT INTO vendor_items VALUES (4658,17780868,26244,0,0,0,0,0,0);	-- Scroll of Shell III
INSERT INTO vendor_items VALUES (4735,17780868,19200,0,0,0,0,0,0);	-- Scroll of Protectra III
INSERT INTO vendor_items VALUES (4739,17780868,14080,0,0,0,0,0,0);	-- Scroll of Shellra II
INSERT INTO vendor_items VALUES (4740,17780868,26244,0,0,0,0,0,0);	-- Scroll of Shellra III
INSERT INTO vendor_items VALUES (4685,17780868,15120,0,0,0,0,0,0);	-- Scroll of Barpetrify
INSERT INTO vendor_items VALUES (4686,17780868,9600,0,0,0,0,0,0);	-- Scroll of Barvirus
INSERT INTO vendor_items VALUES (4699,17780868,15120,0,0,0,0,0,0);	-- Scroll of Barpetra
INSERT INTO vendor_items VALUES (4700,17780868,9600,0,0,0,0,0,0);	-- Scroll of Barvira
INSERT INTO vendor_items VALUES (4867,17780868,18720,0,0,0,0,0,0);	-- Scroll of Sleep II
INSERT INTO vendor_items VALUES (4769,17780868,19932,0,0,0,0,0,0);	-- Scroll of Stone III
INSERT INTO vendor_items VALUES (4779,17780868,22682,0,0,0,0,0,0);	-- Scroll of Water III
INSERT INTO vendor_items VALUES (4764,17780868,27744,0,0,0,0,0,0);	-- Scroll of Aero III
INSERT INTO vendor_items VALUES (4754,17780868,33306,0,0,0,0,0,0);	-- Scroll of Fire III
INSERT INTO vendor_items VALUES (4759,17780868,39368,0,0,0,0,0,0);	-- Scroll of Blizzard III
INSERT INTO vendor_items VALUES (4774,17780868,45930,0,0,0,0,0,0);	-- Scroll of Thunder III

-- Thadiene
INSERT INTO vendor_items VALUES (17280,17719355,1575,1,0,0,1,0,0);	-- Boomerang
INSERT INTO vendor_items VALUES (17162,17719355,19630,1,0,0,1,0,0);	-- Great Bow
INSERT INTO vendor_items VALUES (17321,17719355,16,1,0,0,1,0,0);	-- Silver Arrow
INSERT INTO vendor_items VALUES (17154,17719355,7128,1,0,0,1,0,0);	-- Wrapped Bow
INSERT INTO vendor_items VALUES (17336,17719355,5,2,0,0,0,0,0);	-- Crossbow Bolt
INSERT INTO vendor_items VALUES (17322,17719355,126,2,0,0,0,0,0);	-- Fire Arrow
INSERT INTO vendor_items VALUES (17320,17719355,7,2,0,0,0,0,0);	-- Iron Arrow
INSERT INTO vendor_items VALUES (17153,17719355,482,2,0,0,0,0,0);	-- Self Bow
INSERT INTO vendor_items VALUES (17160,17719355,442,0,0,0,0,0,0);	-- Longbow
INSERT INTO vendor_items VALUES (17152,17719355,38,0,0,0,0,0,0);	-- Shortbow
INSERT INTO vendor_items VALUES (17318,17719355,3,0,0,0,0,0,0);	-- Wooden Arrow
INSERT INTO vendor_items VALUES (5029,17719355,4320,0,0,0,0,0,0);	-- Scroll of Battlefield Elegy

-- Theraisie
INSERT INTO vendor_items VALUES (21444,17776719,200,0,0,0,0,0,0);	-- Livid Broth
INSERT INTO vendor_items VALUES (21445,17776719,344,0,0,0,0,0,0);	-- Lyrical Broth
INSERT INTO vendor_items VALUES (21446,17776719,519,0,0,0,0,0,0);	-- Airy Broth
INSERT INTO vendor_items VALUES (21447,17776719,1016,0,0,0,0,0,0);	-- Crumbly Soil
INSERT INTO vendor_items VALUES (17922,17776719,1484,0,0,0,0,0,0);	-- Blackwater Broth
INSERT INTO vendor_items VALUES (21448,17776719,1747,0,0,0,0,0,0);	-- Pale Sap
INSERT INTO vendor_items VALUES (21498,17776719,1747,0,0,0,0,0,0);	-- Crackling Broth
INSERT INTO vendor_items VALUES (17920,17776719,2195,0,0,0,0,0,0);	-- Meaty Broth
INSERT INTO vendor_items VALUES (21497,17776719,2371,0,0,0,0,0,0);	-- Rapid Broth
INSERT INTO vendor_items VALUES (21499,17776719,2425,0,0,0,0,0,0);	-- Creepy Broth
INSERT INTO vendor_items VALUES (17921,17776719,2853,0,0,0,0,0,0);	-- Muddy Broth
INSERT INTO vendor_items VALUES (21449,17776719,3004,0,0,0,0,0,0);	-- Dire Broth
INSERT INTO vendor_items VALUES (17016,17776719,100,0,0,0,0,0,0);	-- Pet Food Alpha
INSERT INTO vendor_items VALUES (17017,17776719,200,0,0,0,0,0,0);	-- Pet Food Beta
INSERT INTO vendor_items VALUES (17018,17776719,350,0,0,0,0,0,0);	-- Pet Food Gamma
INSERT INTO vendor_items VALUES (17019,17776719,500,0,0,0,0,0,0);	-- Pet Food Delta
INSERT INTO vendor_items VALUES (17020,17776719,750,0,0,0,0,0,0);	-- Pet Food Epsilon
INSERT INTO vendor_items VALUES (17021,17776719,1000,0,0,0,0,0,0);	-- Pet Food Zeta
INSERT INTO vendor_items VALUES (17022,17776719,1500,0,0,0,0,0,0);	-- Pet Food Eta
INSERT INTO vendor_items VALUES (17023,17776719,2000,0,0,0,0,0,0);	-- Pet Food Theta
INSERT INTO vendor_items VALUES (19251,17776719,300,0,0,0,0,0,0);	-- Pet Roborant
INSERT INTO vendor_items VALUES (19252,17776719,250,0,0,0,0,0,0);	-- Pet Poultice

-- Tibelda
INSERT INTO vendor_items VALUES (4382,17735745,29,0,0,0,0,0,0);	-- Frost Turnip
INSERT INTO vendor_items VALUES (638,17735745,170,0,0,0,0,0,0);	-- Sage

-- Toji Mumosulah
INSERT INTO vendor_items VALUES (112,17801278,456,0,0,0,0,0,0);	-- Yellow Jar
INSERT INTO vendor_items VALUES (13199,17801278,95,0,0,0,0,0,0);	-- Blood Stone
INSERT INTO vendor_items VALUES (13076,17801278,3510,0,0,0,0,0,0);	-- Fang Necklace
INSERT INTO vendor_items VALUES (13321,17801278,1667,0,0,0,0,0,0);	-- Bone Earring
INSERT INTO vendor_items VALUES (17351,17801278,4747,0,0,0,0,0,0);	-- Gemshorn
INSERT INTO vendor_items VALUES (16993,17801278,69,0,0,0,0,0,0);	-- Peeled Crayfish
INSERT INTO vendor_items VALUES (16998,17801278,36,0,0,0,0,0,0);	-- Insect Paste
INSERT INTO vendor_items VALUES (17876,17801278,165,0,0,0,0,0,0);	-- Fish Broth
INSERT INTO vendor_items VALUES (17880,17801278,695,0,0,0,0,0,0);	-- Seedbed Soil
INSERT INTO vendor_items VALUES (1021,17801278,450,0,0,0,0,0,0);	-- Hatchet
INSERT INTO vendor_items VALUES (4987,17801278,328,0,0,0,0,0,0);	-- Scroll of Army's Paeon II
INSERT INTO vendor_items VALUES (4988,17801278,3312,0,0,0,0,0,0);	-- Scroll of Army's Paeon III

-- Tomasa
INSERT INTO vendor_items VALUES (4396,17748005,257,0,1,0,0,1,0);	-- Sausage Roll
INSERT INTO vendor_items VALUES (4409,17748005,73,0,1,0,0,1,0);	-- Hard-Boiled Egg
INSERT INTO vendor_items VALUES (4417,17748005,3036,0,1,0,0,1,0);	-- Egg Soup
INSERT INTO vendor_items VALUES (4442,17748005,368,0,1,0,0,1,0);	-- Pineapple Juice
INSERT INTO vendor_items VALUES (4391,17748005,22,0,2,0,0,0,0);	-- Bretzel
INSERT INTO vendor_items VALUES (4578,17748005,143,0,2,0,0,0,0);	-- Sausage
INSERT INTO vendor_items VALUES (4424,17748005,1012,0,2,0,0,0,0);	-- Melon Juice
INSERT INTO vendor_items VALUES (4499,17748005,92,0,0,0,0,0,0);	-- Iron Bread
INSERT INTO vendor_items VALUES (4436,17748005,294,0,0,0,0,0,0);	-- Baked Popoto
INSERT INTO vendor_items VALUES (4455,17748005,184,0,0,0,0,0,0);	-- Pebble Soup
INSERT INTO vendor_items VALUES (4509,17748005,10,0,0,0,0,0,0);	-- Distilled Water

-- Torapiont
INSERT INTO vendor_items VALUES (16411,17793036,11491,0,0,0,0,0,0);	-- Claws
INSERT INTO vendor_items VALUES (16451,17793036,7727,0,0,0,0,0,0);	-- Mythril Dagger
INSERT INTO vendor_items VALUES (16513,17793036,11588,0,0,0,0,0,0);	-- Tuck
INSERT INTO vendor_items VALUES (16584,17793036,37800,0,0,0,0,0,0);	-- Mythril Claymore
INSERT INTO vendor_items VALUES (16643,17793036,11040,0,0,0,0,0,0);	-- Battleaxe
INSERT INTO vendor_items VALUES (16705,17793036,4095,0,0,0,0,0,0);	-- Greataxe
INSERT INTO vendor_items VALUES (17050,17793036,333,0,0,0,0,0,0);	-- Willow Wand
INSERT INTO vendor_items VALUES (17051,17793036,1409,0,0,0,0,0,0);	-- Yew Wand
INSERT INTO vendor_items VALUES (17089,17793036,571,0,0,0,0,0,0);	-- Holly Staff
INSERT INTO vendor_items VALUES (17307,17793036,9,0,0,0,0,0,0);	-- Dart
INSERT INTO vendor_items VALUES (17336,17793036,5,0,0,0,0,0,0);	-- Crossbow Bolt
INSERT INTO vendor_items VALUES (17318,17793036,3,0,0,0,0,0,0);	-- Wooden Arrow
INSERT INTO vendor_items VALUES (17320,17793036,7,0,0,0,0,0,0);	-- Iron Arrow

-- Tya Padolih
INSERT INTO vendor_items VALUES (4716,17797255,4147,0,0,0,0,0,0);	-- Scroll of Regen
INSERT INTO vendor_items VALUES (4718,17797255,7516,0,0,0,0,0,0);	-- Scroll of Regen II
INSERT INTO vendor_items VALUES (4881,17797255,10752,0,0,0,0,0,0);	-- Scroll of Sleepga
INSERT INTO vendor_items VALUES (4690,17797255,29030,0,0,0,0,0,0);	-- Scroll of Baramnesia
INSERT INTO vendor_items VALUES (4691,17797255,29030,0,0,0,0,0,0);	-- Scroll of Baramnesra
INSERT INTO vendor_items VALUES (4744,17797255,5523,0,0,0,0,0,0);	-- Scroll of Invisible
INSERT INTO vendor_items VALUES (4745,17797255,2400,0,0,0,0,0,0);	-- Scroll of Sneak
INSERT INTO vendor_items VALUES (4746,17797255,1243,0,0,0,0,0,0);	-- Scroll of Deodorize
INSERT INTO vendor_items VALUES (4912,17797255,18032,0,0,0,0,0,0);	-- Scroll of Distract
INSERT INTO vendor_items VALUES (4914,17797255,25038,0,0,0,0,0,0);	-- Scroll of Frazzle

-- Uli Pehkowa
INSERT INTO vendor_items VALUES (644,17760337,1840,0,0,0,0,0,0);	-- Mythril Ore
INSERT INTO vendor_items VALUES (835,17760337,230,0,0,0,0,0,0);	-- Flax Flower
INSERT INTO vendor_items VALUES (699,17760337,5814,0,0,0,0,0,0);	-- Oak Log
INSERT INTO vendor_items VALUES (698,17760337,87,0,0,0,0,0,0);	-- Ash Log
INSERT INTO vendor_items VALUES (694,17760337,2599,0,0,0,0,0,0);	-- Chestnut Log
INSERT INTO vendor_items VALUES (640,17760337,11,0,0,0,0,0,0);	-- Copper Ore
INSERT INTO vendor_items VALUES (643,17760337,828,0,0,0,0,0,0);	-- Iron Ore
INSERT INTO vendor_items VALUES (4570,17760337,51,0,0,0,0,0,0);	-- Bird Egg
INSERT INTO vendor_items VALUES (833,17760337,18,0,0,0,0,0,0);	-- Moko Grass
INSERT INTO vendor_items VALUES (114,17760337,1840,0,0,0,0,0,0);	-- My First Magic Kit

-- Upih Khachla
INSERT INTO vendor_items VALUES (17313,17752098,1107,0,0,1,0,0,1);	-- Grenade
INSERT INTO vendor_items VALUES (4112,17752098,837,0,0,1,0,0,1);	-- Potion
INSERT INTO vendor_items VALUES (951,17752098,108,0,0,1,0,0,1);	-- Wijnruit
INSERT INTO vendor_items VALUES (636,17752098,119,0,0,2,0,0,0);	-- Chamomile
INSERT INTO vendor_items VALUES (4151,17752098,736,0,0,2,0,0,0);	-- Echo Drops
INSERT INTO vendor_items VALUES (4128,17752098,4445,0,0,2,0,0,0);	-- Ether
INSERT INTO vendor_items VALUES (4148,17752098,290,0,0,0,0,0,0);	-- Antidote
INSERT INTO vendor_items VALUES (1892,17752098,3960,0,0,0,0,0,0);	-- Desalinator
INSERT INTO vendor_items VALUES (622,17752098,44,0,0,0,0,0,0);	-- Dried Marjoram
INSERT INTO vendor_items VALUES (4150,17752098,2387,0,0,0,0,0,0);	-- Eye Drops
INSERT INTO vendor_items VALUES (605,17752098,180,0,0,0,0,0,0);	-- Pickaxe
INSERT INTO vendor_items VALUES (1893,17752098,3960,0,0,0,0,0,0);	-- Salinator
INSERT INTO vendor_items VALUES (1020,17752098,276,0,0,0,0,0,0);	-- Sickle
INSERT INTO vendor_items VALUES (1241,17752098,354,0,0,0,0,0,0);	-- Twinkle Powder

-- Valeriano
INSERT INTO vendor_items VALUES (4394,17719424,10,0,0,0,0,0,0);	-- Ginger Cookie
INSERT INTO vendor_items VALUES (17345,17719424,43,0,0,0,0,0,0);	-- Flute
INSERT INTO vendor_items VALUES (17347,17719424,990,0,0,0,0,0,0);	-- Piccolo
INSERT INTO vendor_items VALUES (5017,17719424,585,0,0,0,0,0,0);	-- Scroll of Scop's Operetta
INSERT INTO vendor_items VALUES (5018,17719424,16920,0,0,0,0,0,0);	-- Scroll of Puppet's Operetta
INSERT INTO vendor_items VALUES (5013,17719424,2916,0,0,0,0,0,0);	-- Scroll of Fowl Aubade
INSERT INTO vendor_items VALUES (5027,17719424,2059,0,0,0,0,0,0);	-- Scroll of Advancing March
INSERT INTO vendor_items VALUES (5072,17719424,90000,0,0,0,0,0,0);	-- Scroll of Goddess's Hymnus

-- Vattian
INSERT INTO vendor_items VALUES (916,17743923,855,0,0,0,0,0,0);	-- Cactuar Needle
INSERT INTO vendor_items VALUES (4412,17743923,299,0,0,0,0,0,0);	-- Thundermelon
INSERT INTO vendor_items VALUES (4491,17743923,184,0,0,0,0,0,0);	-- Watermelon

-- Vendavoq
INSERT INTO vendor_items VALUES (640,17727526,11,0,0,0,0,0,0);	-- Copper Ore
INSERT INTO vendor_items VALUES (4450,17727526,694,0,0,0,0,0,0);	-- Coral Fungus
INSERT INTO vendor_items VALUES (4375,17727526,4032,0,0,0,0,0,0);	-- Danceshroom
INSERT INTO vendor_items VALUES (1650,17727526,6500,0,0,0,0,0,0);	-- Kopparnickel Ore
INSERT INTO vendor_items VALUES (5165,17727526,736,0,0,0,0,0,0);	-- Movalpolos Water

-- Vichuel
INSERT INTO vendor_items VALUES (4571,17723487,90,0,0,0,0,0,0);	-- Beaugreens
INSERT INTO vendor_items VALUES (4363,17723487,39,0,0,0,0,0,0);	-- Faerie Apple
INSERT INTO vendor_items VALUES (691,17723487,54,0,0,0,0,0,0);	-- Maple Log

-- Victoire
INSERT INTO vendor_items VALUES (12432,17719389,1450,0,0,0,0,0,0);	-- Faceguard
INSERT INTO vendor_items VALUES (12464,17719389,1936,0,0,0,0,0,0);	-- Headgear
INSERT INTO vendor_items VALUES (12560,17719389,2230,0,0,0,0,0,0);	-- Scale Mail
INSERT INTO vendor_items VALUES (12592,17719389,2745,0,0,0,0,0,0);	-- Doublet
INSERT INTO vendor_items VALUES (12688,17719389,1190,0,0,0,0,0,0);	-- Scale Fng. Gnt.
INSERT INTO vendor_items VALUES (12720,17719389,1515,0,0,0,0,0,0);	-- Gloves
INSERT INTO vendor_items VALUES (12816,17719389,1790,0,0,0,0,0,0);	-- Scale Cuisses
INSERT INTO vendor_items VALUES (12848,17719389,2110,0,0,0,0,0,0);	-- Brais
INSERT INTO vendor_items VALUES (12944,17719389,1085,0,0,0,0,0,0);	-- Scale Greaves
INSERT INTO vendor_items VALUES (12976,17719389,1410,0,0,0,0,0,0);	-- Gaiters

-- Wata Khamazom
INSERT INTO vendor_items VALUES (17152,16994350,44,0,0,0,0,0,0);	-- Shortbow
INSERT INTO vendor_items VALUES (17153,16994350,536,0,0,0,0,0,0);	-- Self Bow
INSERT INTO vendor_items VALUES (17154,16994350,7920,0,0,0,0,0,0);	-- Wrapped Bow
INSERT INTO vendor_items VALUES (17160,16994350,492,0,0,0,0,0,0);	-- Longbow
INSERT INTO vendor_items VALUES (17162,16994350,21812,0,0,0,0,0,0);	-- Great Bow
INSERT INTO vendor_items VALUES (17318,16994350,4,0,0,0,0,0,0);	-- Wooden Arrow
INSERT INTO vendor_items VALUES (17320,16994350,8,0,0,0,0,0,0);	-- Iron Arrow
INSERT INTO vendor_items VALUES (17321,16994350,18,0,0,0,0,0,0);	-- Silver Arrow
INSERT INTO vendor_items VALUES (17322,16994350,140,0,0,0,0,0,0);	-- Fire Arrow
INSERT INTO vendor_items VALUES (17336,16994350,6,0,0,0,0,0,0);	-- Crossbow Bolt
INSERT INTO vendor_items VALUES (18258,16994350,248,0,0,0,0,0,0);	-- Throwing Tomahawk

-- Wije Tiren
INSERT INTO vendor_items VALUES (4148,17764459,290,0,0,0,0,0,0);	-- Antidote
INSERT INTO vendor_items VALUES (4509,17764459,10,0,0,0,0,0,0);	-- Distilled Water
INSERT INTO vendor_items VALUES (4151,17764459,728,0,0,0,0,0,0);	-- Echo Drops
INSERT INTO vendor_items VALUES (4128,17764459,4445,0,0,0,0,0,0);	-- Ether
INSERT INTO vendor_items VALUES (4150,17764459,2387,0,0,0,0,0,0);	-- Eye Drops
INSERT INTO vendor_items VALUES (4112,17764459,837,0,0,0,0,0,0);	-- Potion
INSERT INTO vendor_items VALUES (5014,17764459,98,0,0,0,0,0,0);	-- Scroll of Herb Pastoral

-- Yafaaf
INSERT INTO vendor_items VALUES (5577,16982100,1500,0,0,0,0,0,0);	-- Sutlac
INSERT INTO vendor_items VALUES (5592,16982100,450,0,0,0,0,0,0);	-- Imperial Coffee

-- Yafafa
INSERT INTO vendor_items VALUES (4503,17739823,184,0,0,0,0,0,0);	-- Buburimu Grape
INSERT INTO vendor_items VALUES (1120,17739823,1620,0,0,0,0,0,0);	-- Casablanca
INSERT INTO vendor_items VALUES (4359,17739823,220,0,0,0,0,0,0);	-- Dhalmel Meat
INSERT INTO vendor_items VALUES (614,17739823,72,0,0,0,0,0,0);	-- Mhaura Garlic
INSERT INTO vendor_items VALUES (4445,17739823,40,0,0,0,0,0,0);	-- Yagudo Cherry

-- Yoskolo
INSERT INTO vendor_items VALUES (4509,17780842,10,0,0,0,0,0,0);	-- Distilled Water
INSERT INTO vendor_items VALUES (4422,17780842,184,0,0,0,0,0,0);	-- Orange Juice
INSERT INTO vendor_items VALUES (4423,17780842,276,0,0,0,0,0,0);	-- Apple Juice
INSERT INTO vendor_items VALUES (4424,17780842,1012,0,0,0,0,0,0);	-- Melon Juice
INSERT INTO vendor_items VALUES (4441,17780842,855,0,0,0,0,0,0);	-- Grape Juice
INSERT INTO vendor_items VALUES (4442,17780842,368,0,0,0,0,0,0);	-- Pineapple Juice
INSERT INTO vendor_items VALUES (4556,17780842,5544,0,0,0,0,0,0);	-- Icecap Rolanberry
INSERT INTO vendor_items VALUES (5046,17780842,6380,0,0,0,0,0,0);	-- Scroll of Fire Carol
INSERT INTO vendor_items VALUES (5047,17780842,7440,0,0,0,0,0,0);	-- Scroll of Ice Carol
INSERT INTO vendor_items VALUES (5048,17780842,5940,0,0,0,0,0,0);	-- Scroll of Wind Carol
INSERT INTO vendor_items VALUES (5049,17780842,4600,0,0,0,0,0,0);	-- Scroll of Earth Carol
INSERT INTO vendor_items VALUES (5050,17780842,7920,0,0,0,0,0,0);	-- Scroll of Lightning Carol
INSERT INTO vendor_items VALUES (5051,17780842,5000,0,0,0,0,0,0);	-- Scroll of Water Carol
INSERT INTO vendor_items VALUES (5052,17780842,4200,0,0,0,0,0,0);	-- Scroll of Light Carol
INSERT INTO vendor_items VALUES (5053,17780842,8400,0,0,0,0,0,0);	-- Scroll of Dark Carol
INSERT INTO vendor_items VALUES (5078,17780842,60000,0,0,0,0,0,0);	-- Scroll of Sentinel's Scherzo

-- Yoyoroon
INSERT INTO vendor_items VALUES (2239,16994344,4940,0,0,0,0,0,0);	-- Tension Spring
INSERT INTO vendor_items VALUES (2243,16994344,4940,0,0,0,0,0,0);	-- Loudspeaker
INSERT INTO vendor_items VALUES (2246,16994344,4940,0,0,0,0,0,0);	-- Accelerator
INSERT INTO vendor_items VALUES (2251,16994344,4940,0,0,0,0,0,0);	-- Armor Plate
INSERT INTO vendor_items VALUES (2254,16994344,4940,0,0,0,0,0,0);	-- Stabilizer
INSERT INTO vendor_items VALUES (2258,16994344,4940,0,0,0,0,0,0);	-- Mana Jammer
INSERT INTO vendor_items VALUES (2262,16994344,4940,0,0,0,0,0,0);	-- Auto-Repair Kit
INSERT INTO vendor_items VALUES (2266,16994344,4940,0,0,0,0,0,0);	-- Mana Tank
INSERT INTO vendor_items VALUES (2240,16994344,9925,0,0,0,0,0,0);	-- Inhibitor
INSERT INTO vendor_items VALUES (2242,16994344,9925,0,0,0,0,0,0);	-- Mana Booster
INSERT INTO vendor_items VALUES (2247,16994344,9925,0,0,0,0,0,0);	-- Scope
INSERT INTO vendor_items VALUES (2250,16994344,9925,0,0,0,0,0,0);	-- Shock Absorber
INSERT INTO vendor_items VALUES (2255,16994344,9925,0,0,0,0,0,0);	-- Volt Gun
INSERT INTO vendor_items VALUES (2260,16994344,9925,0,0,0,0,0,0);	-- Stealth Screen
INSERT INTO vendor_items VALUES (2264,16994344,9925,0,0,0,0,0,0);	-- Damage Gauge
INSERT INTO vendor_items VALUES (2268,16994344,9925,0,0,0,0,0,0);	-- Mana Conserver

-- Zafif
INSERT INTO vendor_items VALUES (4612,16974280,23400,0,0,0,0,0,0);	-- Scroll of Cure IV
INSERT INTO vendor_items VALUES (4616,16974280,11200,0,0,0,0,0,0);	-- Scroll of Curaga II
INSERT INTO vendor_items VALUES (4617,16974280,19932,0,0,0,0,0,0);	-- Scroll of Curaga III
INSERT INTO vendor_items VALUES (4653,16974280,32000,0,0,0,0,0,0);	-- Scroll of Protect III
INSERT INTO vendor_items VALUES (4654,16974280,91116,0,0,0,0,0,0);	-- Scroll of Protect IV
INSERT INTO vendor_items VALUES (4736,16974280,85500,0,0,0,0,0,0);	-- Scroll of Protectra IV
INSERT INTO vendor_items VALUES (4629,16974280,35000,0,0,0,0,0,0);	-- Scroll of Holy
INSERT INTO vendor_items VALUES (4647,16974280,20000,0,0,0,0,0,0);	-- Scroll of Banishga II
INSERT INTO vendor_items VALUES (4625,16974280,2330,0,0,0,0,0,0);	-- Scroll of Silena
INSERT INTO vendor_items VALUES (4626,16974280,19200,0,0,0,0,0,0);	-- Scroll of Stona
INSERT INTO vendor_items VALUES (4627,16974280,13300,0,0,0,0,0,0);	-- Scroll of Viruna
INSERT INTO vendor_items VALUES (4628,16974280,8586,0,0,0,0,0,0);	-- Scroll of Cursna
INSERT INTO vendor_items VALUES (4868,16974280,77600,0,0,0,0,0,0);	-- Scroll of Dispell
INSERT INTO vendor_items VALUES (4720,16974280,27000,0,0,0,0,0,0);	-- Scroll of Flash
INSERT INTO vendor_items VALUES (4750,16974280,99375,0,0,0,0,0,0);	-- Scroll of Reraise III
INSERT INTO vendor_items VALUES (4715,16974280,28500,0,0,0,0,0,0);	-- Scroll of Reprisal

-- Zaira
INSERT INTO vendor_items VALUES (4862,17739806,114,0,0,0,0,0,0);	-- Scroll of Blind
INSERT INTO vendor_items VALUES (4838,17739806,360,0,0,0,0,0,0);	-- Scroll of Bio
INSERT INTO vendor_items VALUES (4828,17739806,82,0,0,0,0,0,0);	-- Scroll of Poison
INSERT INTO vendor_items VALUES (4861,17739806,2250,0,0,0,0,0,0);	-- Scroll of Sleep
INSERT INTO vendor_items VALUES (4767,17739806,61,0,0,0,0,0,0);	-- Scroll of Stone
INSERT INTO vendor_items VALUES (4777,17739806,140,0,0,0,0,0,0);	-- Scroll of Water
INSERT INTO vendor_items VALUES (4762,17739806,324,0,0,0,0,0,0);	-- Scroll of Aero
INSERT INTO vendor_items VALUES (4752,17739806,837,0,0,0,0,0,0);	-- Scroll of Fire
INSERT INTO vendor_items VALUES (4757,17739806,1584,0,0,0,0,0,0);	-- Scroll of Blizzard
INSERT INTO vendor_items VALUES (4772,17739806,3261,0,0,0,0,0,0);	-- Scroll of Thunder
INSERT INTO vendor_items VALUES (4847,17739806,1363,0,0,0,0,0,0);	-- Scroll of Shock
INSERT INTO vendor_items VALUES (4846,17739806,1827,0,0,0,0,0,0);	-- Scroll of Rasp
INSERT INTO vendor_items VALUES (4845,17739806,2250,0,0,0,0,0,0);	-- Scroll of Choke
INSERT INTO vendor_items VALUES (4844,17739806,3688,0,0,0,0,0,0);	-- Scroll of Frost
INSERT INTO vendor_items VALUES (4843,17739806,4644,0,0,0,0,0,0);	-- Scroll of Burn
INSERT INTO vendor_items VALUES (4848,17739806,6366,0,0,0,0,0,0);	-- Scroll of Drown

-- Zemedars
INSERT INTO vendor_items VALUES (12836,17735723,23316,0,1,0,0,1,0);	-- Iron Subligar
INSERT INTO vendor_items VALUES (12825,17735723,5003,0,1,0,0,1,0);	-- Lizard Trousers
INSERT INTO vendor_items VALUES (12962,17735723,14484,0,1,0,0,1,0);	-- Leggins
INSERT INTO vendor_items VALUES (12953,17735723,3162,0,1,0,0,1,0);	-- Lizard Ledelsens
INSERT INTO vendor_items VALUES (12301,17735723,31544,0,1,0,0,1,0);	-- Buckler
INSERT INTO vendor_items VALUES (12833,17735723,1840,0,2,0,0,0,0);	-- Brass Subligar
INSERT INTO vendor_items VALUES (12824,17735723,493,0,2,0,0,0,0);	-- Leather Trousers
INSERT INTO vendor_items VALUES (12961,17735723,1140,0,2,0,0,0,0);	-- Brass Leggins
INSERT INTO vendor_items VALUES (12952,17735723,309,0,2,0,0,0,0);	-- Leather Highboots
INSERT INTO vendor_items VALUES (12300,17735723,11076,0,2,0,0,0,0);	-- Targe
INSERT INTO vendor_items VALUES (12832,17735723,191,0,0,0,0,0,0);	-- Bronze Subligar
INSERT INTO vendor_items VALUES (12808,17735723,11592,0,0,0,0,0,0);	-- Chain Gose
INSERT INTO vendor_items VALUES (12960,17735723,117,0,0,0,0,0,0);	-- Bronze Leggins
INSERT INTO vendor_items VALUES (12936,17735723,7120,0,0,0,0,0,0);	-- Greaves
INSERT INTO vendor_items VALUES (12290,17735723,556,0,0,0,0,0,0);	-- Maple Shield
INSERT INTO vendor_items VALUES (12289,17735723,110,0,0,0,0,0,0);	-- Lauan Shield

-- Zhikkom
INSERT INTO vendor_items VALUES (16473,17739798,5713,0,1,0,0,1,0);	-- Kukri
INSERT INTO vendor_items VALUES (16537,17739798,31648,0,1,0,0,1,0);	-- Mythril Sword
INSERT INTO vendor_items VALUES (16545,17739798,21535,0,1,0,0,1,0);	-- Broadsword
INSERT INTO vendor_items VALUES (16513,17739798,11845,0,1,0,0,1,0);	-- Tuck
INSERT INTO vendor_items VALUES (16558,17739798,62560,0,1,0,0,1,0);	-- Falchion
INSERT INTO vendor_items VALUES (16536,17739798,7286,0,2,0,0,0,0);	-- Iron Sword
INSERT INTO vendor_items VALUES (16552,17739798,4163,0,2,0,0,0,0);	-- Scimitar
INSERT INTO vendor_items VALUES (16466,17739798,2231,0,0,0,0,0,0);	-- Knife
INSERT INTO vendor_items VALUES (16465,17739798,150,0,0,0,0,0,0);	-- Bronze Knife
INSERT INTO vendor_items VALUES (16405,17739798,106,0,0,0,0,0,0);	-- Cat Baghnakhs
INSERT INTO vendor_items VALUES (16535,17739798,246,0,0,0,0,0,0);	-- Bronze Sword
INSERT INTO vendor_items VALUES (16517,17739798,9406,0,0,0,0,0,0);	-- Degen
INSERT INTO vendor_items VALUES (16551,17739798,713,0,0,0,0,0,0);	-- Sapara

-- Zoby Quhyo
INSERT INTO vendor_items VALUES (626,17744005,234,0,0,0,0,0,0);	-- Black Pepper
INSERT INTO vendor_items VALUES (612,17744005,55,0,0,0,0,0,0);	-- Kazham Peppers
INSERT INTO vendor_items VALUES (4432,17744005,55,0,0,0,0,0,0);	-- Kazham Pineapple
INSERT INTO vendor_items VALUES (632,17744005,110,0,0,0,0,0,0);	-- Kukuru Bean
INSERT INTO vendor_items VALUES (4390,17744005,36,0,0,0,0,0,0);	-- Mithran Tomato
INSERT INTO vendor_items VALUES (630,17744005,88,0,0,0,0,0,0);	-- Ogre Pumpkin
INSERT INTO vendor_items VALUES (1411,17744005,1656,0,0,0,0,0,0);	-- Phalaenopsis

-- Zoreen
INSERT INTO vendor_items VALUES (4382,17760319,29,0,0,0,0,0,0);	-- Frost Turnip
INSERT INTO vendor_items VALUES (638,17760319,170,0,0,0,0,0,0);	-- Sage