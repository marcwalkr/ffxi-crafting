DROP TABLE IF EXISTS guilds;
CREATE TABLE guilds (
	guildid smallint(5) UNSIGNED NOT NULL,
    guild_name varchar(24) NOT NULL,
    npc_name varchar(24) NOT NULL,
    area varchar(12) NOT NULL,
    PRIMARY KEY (guildid, npc_name)
);

INSERT INTO guilds VALUES(514, "Bonecraft Guild", "Shih Tayuun", "WindWoods");
INSERT INTO guilds VALUES(516, "Clothcraft Guild", "Tilala", "Selbina");
INSERT INTO guilds VALUES(517, "Fishing Guild", "Babubu", "PortWind");
INSERT INTO guilds VALUES(518, "Fishing Guild", "Graegham", "Selbina");
INSERT INTO guilds VALUES(519, "Fishing Guild", "Mep Nhapopoluko", "BibikiBay");
INSERT INTO guilds VALUES(520, "Fishing Guild", "Rajmonda", "ShipToSelb");
INSERT INTO guilds VALUES(521, "Fishing Guild", "Lokhong", "Mhaura");
INSERT INTO guilds VALUES(522, "Fishing Guild", "Cehn Teyohngo", "OpenseaZah");
INSERT INTO guilds VALUES(523, "Fishing Guild", "Pashi Maccaleh", "OpenseaMha");
INSERT INTO guilds VALUES(524, "Fishing Guild", "Jidwahn", "SilvSeaNas");
INSERT INTO guilds VALUES(525, "Fishing Guild", "Yahliq", "SilvSeaZah");
INSERT INTO guilds VALUES(528, "Goldsmith Guild", "Yabby Tanmikey", "Mhaura");
INSERT INTO guilds VALUES(529, "Leathercraft Guild", "Kueh Igunahmori", "SSandOria");
INSERT INTO guilds VALUES(530, "Cooking Guild", "Kopopo", "WindWaters");
INSERT INTO guilds VALUES(531, "Smithing Guild", "Doggomehr", "NSandOria");
INSERT INTO guilds VALUES(532, "Smithing Guild", "Kamilah", "Mhaura");
INSERT INTO guilds VALUES(534, "Woodworking Guild", "Beugungel", "CpntLanding");
INSERT INTO guilds VALUES(5132, "Woodworking Guild", "Chaupire", "NSandOria");
INSERT INTO guilds VALUES(5152, "Clothcraft Guild", "Kuzah Hpirohpon", "WindWoods");
INSERT INTO guilds VALUES(5182, "Fishing Guild", "Mendoline", "Selbina");
INSERT INTO guilds VALUES(5262, "Alchemist Guild", "Maymunah", "BastokMine");
INSERT INTO guilds VALUES(5272, "Goldsmith Guild", "Visala", "BastokMark");
INSERT INTO guilds VALUES(5332, "Smithing Guild", "Amulya", "Metalworks");
INSERT INTO guilds VALUES(60417, "Tenshodo Merchant", "Akamafula", "LowJeuno");
INSERT INTO guilds VALUES(60418, "Chip Vendor", "Blabbivix", "PortBastok");
INSERT INTO guilds VALUES(60418, "Chip Vendor", "Gaudylox", "NSandOria");
INSERT INTO guilds VALUES(60418, "Chip Vendor", "Scavnix", "WindWalls");
INSERT INTO guilds VALUES(60419, "Tenshodo Merchant", "Jabbar", "PortBastok");
INSERT INTO guilds VALUES(60420, "Tenshodo Merchant", "Silver Owl", "PortBastok");
INSERT INTO guilds VALUES(60421, "Tenshodo Merchant", "Achika", "Norg");
INSERT INTO guilds VALUES(60422, "Tenshodo Merchant", "Chiyo", "Norg");
INSERT INTO guilds VALUES(60423, "Tenshodo Merchant", "Jirokichi", "Norg");
INSERT INTO guilds VALUES(60424, "Tenshodo Merchant", "Vuliaie", "Norg");
INSERT INTO guilds VALUES(60425, "Alchemy Guild", "Wahraga", "Whitegate");
INSERT INTO guilds VALUES(60426, "Fishing Guild", "Wahnid", "Whitegate");
INSERT INTO guilds VALUES(60427, "Smithing Guild", "Ndego", "AlZahbi");
INSERT INTO guilds VALUES(60428, "Woodworking Guild", "Dehbi Moshal", "AlZahbi");
INSERT INTO guilds VALUES(60429, "Goldsmithing Guild", "Bornahn", "AlZahbi");
INSERT INTO guilds VALUES(60430, "Clothcraft Guild", "Taten-Bilten", "AlZahbi");
INSERT INTO guilds VALUES(60431, "Tenshodo Merchant", "Tsutsuroon", "Nashmau");