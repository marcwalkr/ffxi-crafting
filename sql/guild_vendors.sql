DROP TABLE IF EXISTS guild_vendors;
CREATE TABLE guild_vendors (
    guildid smallint UNSIGNED PRIMARY KEY,
    npcid int UNSIGNED NOT NULL,
    category varchar(20) NOT NULL
);

-- Alchemy  
INSERT INTO guild_vendors VALUES (5262, 17735714, "Alchemy"); -- Maymunah (Bastok Mines) Alchemist Guild (S)
INSERT INTO guild_vendors VALUES (60425, 16982103, "Alchemy"); -- Wahraga (Alchemy Guild) Aht Urhgan Whitegate

-- Bonecraft
INSERT INTO guild_vendors VALUES (514, 17764406, "Bonecraft"); -- Shih Tayuun (Bonecraft Guild) Windurst Woods (S)

-- Clothcraft
INSERT INTO guild_vendors VALUES (5152, 17764401, "Clothcraft"); -- Kuzah Hpirohpon (Windurst Woods) Clothcraft Guild (S)
INSERT INTO guild_vendors VALUES (516, 17793053, "Clothcraft"); -- Tilala (Clothcraft Guild) Selbina (S)
INSERT INTO guild_vendors VALUES (60430, 16974282, "Clothcraft"); -- Taten-Bilten (Clothcraft Guild) Al Zahbi

-- Cooking
INSERT INTO guild_vendors VALUES (530, 17752141, "Cooking"); -- Kopopo (Windurst Waters) Cooking Guild (S)

-- Fishing
INSERT INTO guild_vendors VALUES (517, 17760306, "Fishing"); -- Babubu (Port Windurst) Fishing Guild
INSERT INTO guild_vendors VALUES (518, 17793038, "Fishing"); -- Graegham (Selbina) Fishing Guild (S)
INSERT INTO guild_vendors VALUES (5182, 17793037, "Fishing"); -- Mendoline (Selbina) Fishing Guild (S)
INSERT INTO guild_vendors VALUES (519, 16793987, "Fishing"); -- Mep Nhapopoluko (Bibiki Bay) Fishing Guild
INSERT INTO guild_vendors VALUES (520, 17678362, "Fishing"); -- Rajmonda (Ship bound for Selbina) Fishing Guild
INSERT INTO guild_vendors VALUES (521, 17682457, "Fishing"); -- Lokhong (Ship bound for Mhaura) Fishing Guild
INSERT INTO guild_vendors VALUES (522, 16965677, "Fishing"); -- Cehn Teyohngo (Open sea route to Al Zahbi) Fishing Guild
INSERT INTO guild_vendors VALUES (523, 16969773, "Fishing"); -- Pashi Maccaleh (Open sea route to Mhaura) Fishing Guild
INSERT INTO guild_vendors VALUES (524, 17014831, "Fishing"); -- Jidwahn (Silver Sea route to Nashmau) Fishing Guild
INSERT INTO guild_vendors VALUES (525, 17018927, "Fishing"); -- Yahliq (Silver Sea route to Al Zahbi) Fishing Guild
INSERT INTO guild_vendors VALUES (60426, 16982101, "Fishing"); -- Wahnid (Fishing Guild) Aht Urhgan Whitegate

-- Goldsmithing
INSERT INTO guild_vendors VALUES (5272, 17739789, "Goldsmithing"); -- Visala (Goldsmith Guild) Bastok Markets (S)
INSERT INTO guild_vendors VALUES (528, 17797131, "Goldsmithing"); -- Yabby Tanmikey (Goldsmith Guild) Mhaura (S)
INSERT INTO guild_vendors VALUES (60429, 16974283, "Goldsmithing"); -- Bornahn (Goldsmithing Guild) Al Zahbi

-- Leathercraft
INSERT INTO guild_vendors VALUES (529, 17719384, "Leathercraft"); -- Kueh Igunahmori (Leathercraft Guild) Southern San d'Oria (S)

-- Smithing
INSERT INTO guild_vendors VALUES (531, 17723439, "Smithing"); -- Doggomehr (Northern San d'Oria) Smithing Guild (S)
INSERT INTO guild_vendors VALUES (532, 17797135, "Smithing"); -- Kamilah (Mhaura) Smithing Guild (S)
INSERT INTO guild_vendors VALUES (5332, 17747970, "Smithing"); -- Amulya (Metalworks) Smithing Guild (S)
INSERT INTO guild_vendors VALUES (60427, 16974284, "Smithing"); -- Ndego (Smithing Guild) Al Zahbi

-- Woodworking
INSERT INTO guild_vendors VALUES (5132, 17723432, "Woodworking"); -- Chaupire (Northern San d'Oria) Woodworking Guild (S)
INSERT INTO guild_vendors VALUES (534, 16785754, "Woodworking"); -- Beugungel (Carpenter's Landing) Woodworking Guild
INSERT INTO guild_vendors VALUES (60428, 16974285, "Woodworking"); -- Dehbi Moshal (Woodworking Guild) Al Zahbi

-- Tenshodo
INSERT INTO guild_vendors VALUES (60417, 17780857, "Tenshodo"); -- Akamafula (Lower Jeuno) Tenshodo Merchent
INSERT INTO guild_vendors VALUES (60419, 17743882, "Tenshodo"); -- Jabbar (Port Bastok) Tenshodo Merchant
INSERT INTO guild_vendors VALUES (60420, 16839222, "Tenshodo"); -- Silver Owl (Port Bastok) Tenshodo Merchant
INSERT INTO guild_vendors VALUES (60421, 17809447, "Tenshodo"); -- Achika (Norg) Tenshodo Merchant
INSERT INTO guild_vendors VALUES (60422, 17809448, "Tenshodo"); -- Chiyo (Norg) Tenshodo Merchant
INSERT INTO guild_vendors VALUES (60423, 17809446, "Tenshodo"); -- Jirokichi (Norg) Tenshodo Merchant
INSERT INTO guild_vendors VALUES (60424, 17809445, "Tenshodo"); -- Vuliaie (Norg) Tenshodo Merchant
INSERT INTO guild_vendors VALUES (60431, 16994370, "Tenshodo"); -- Tsutsuroon (Tenshodo Merchant) Nashmau