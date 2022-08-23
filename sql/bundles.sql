DROP TABLE IF EXISTS bundles;
CREATE TABLE bundles (
    unbundled_id smallint(5) UNSIGNED PRIMARY KEY,
    bundled_id smallint(5) UNSIGNED NOT NULL,
    trade_item_id smallint(5) UNSIGNED NOT NULL
);

INSERT INTO bundles VALUES (21307,6199,948); -- Achiyalabopa Arrow
INSERT INTO bundles VALUES (21306,6200,948); -- Adlivun Arrow
INSERT INTO bundles VALUES (19195,5819,948); -- Antlion Arrow
INSERT INTO bundles VALUES (18154,4221,948); -- Beetle Arrow
INSERT INTO bundles VALUES (21295,6418,948); -- Beryllium Arrow
INSERT INTO bundles VALUES (21309,6137,948); -- Chapuli Arrow
INSERT INTO bundles VALUES (18159,4224,948); -- Demon Arrow
INSERT INTO bundles VALUES (21300,6417,948); -- Divine Arrow
INSERT INTO bundles VALUES (21302,6269,948); -- Eminent Arrow
INSERT INTO bundles VALUES (19800,5912,948); -- Gargouille Arrow
INSERT INTO bundles VALUES (18156,4222,948); -- Horn Arrow
INSERT INTO bundles VALUES (17320,4225,948); -- Iron Arrow
INSERT INTO bundles VALUES (17325,5332,948); -- Kabura Arrow
INSERT INTO bundles VALUES (21308,6138,948); -- Mantid Arrow
INSERT INTO bundles VALUES (21301,6414,948); -- Porxie Arrow
INSERT INTO bundles VALUES (21304,6202,948); -- Raaz Arrow
INSERT INTO bundles VALUES (21303,6280,948); -- Ra'Kaznar Arrow
INSERT INTO bundles VALUES (21310,6419,948); -- Raetic Arrow
INSERT INTO bundles VALUES (19182,5871,948); -- Ruszor Arrow
INSERT INTO bundles VALUES (18155,4223,948); -- Scorpion Arrow
INSERT INTO bundles VALUES (17321,4226,948); -- Silver Arrow
INSERT INTO bundles VALUES (18158,5333,948); -- Sleep Arrow
INSERT INTO bundles VALUES (21305,6201,948); -- Tulfaire Arrow


INSERT INTO bundles VALUES (21314,6278,948); -- Abrasion Bolt
INSERT INTO bundles VALUES (21321,6203,948); -- Achiyalabopa Bolt
INSERT INTO bundles VALUES (18148,5335,948); -- Acid Bolt
INSERT INTO bundles VALUES (19801,5913,948); -- Adaman Bolt
INSERT INTO bundles VALUES (21320,6204,948); -- Adlivun Bolt
INSERT INTO bundles VALUES (22285,6428,948); -- Beryllium Bolt
INSERT INTO bundles VALUES (21318,6206,948); -- Bismuth Bolt
INSERT INTO bundles VALUES (18150,5334,948); -- Blind Bolt
INSERT INTO bundles VALUES (18151,5339,948); -- Bloody Bolt
INSERT INTO bundles VALUES (17339,4227,948); -- Bronze Bolt
INSERT INTO bundles VALUES (21322,6140,948); -- Damascus Bolt
INSERT INTO bundles VALUES (19183,5872,948); -- Dark Adaman Bolt
INSERT INTO bundles VALUES (19196,5820,948); -- Darkling Bolt
INSERT INTO bundles VALUES (17338,4229,948); -- Darksteel Bolt
INSERT INTO bundles VALUES (21312,6427,948); -- Divine Bolt
INSERT INTO bundles VALUES (21316,6270,948); -- Eminent Bolt
INSERT INTO bundles VALUES (19197,5821,948); -- Fusion Bolt
INSERT INTO bundles VALUES (21313,6310,948); -- Gashing Bolt
INSERT INTO bundles VALUES (18153,5336,948); -- Holy Bolt
INSERT INTO bundles VALUES (21324,6139,948); -- Midrium Bolt
INSERT INTO bundles VALUES (21323,6141,948); -- Oxidant Bolt
INSERT INTO bundles VALUES (17337,4228,948); -- Mythril Bolt
INSERT INTO bundles VALUES (21315,6279,948); -- Righteous Bolt
INSERT INTO bundles VALUES (18149,5337,948); -- Sleep Bolt
INSERT INTO bundles VALUES (21319,6205,948); -- Titanium Bolt
INSERT INTO bundles VALUES (18152,5338,948); -- Venom Bolt

INSERT INTO bundles VALUES (21337,6207,948); -- Achiyalabopa Bullet
INSERT INTO bundles VALUES (19803,5915,948); -- Adaman Bullet
INSERT INTO bundles VALUES (21336,6208,948); -- Adlivun Bullet
INSERT INTO bundles VALUES (21333,6210,948); -- Bismuth Bullet
INSERT INTO bundles VALUES (17340,5363,948); -- Bullet
INSERT INTO bundles VALUES (17343,5359,948); -- Bronze Bullet
INSERT INTO bundles VALUES (21338,6143,948); -- Damascus Bullet
INSERT INTO bundles VALUES (19184,5873,948); -- Dark Adaman Bullet
INSERT INTO bundles VALUES (21330,6311,948); -- Decimating Bullet
INSERT INTO bundles VALUES (21328,6437,948); -- Divine Bullet
INSERT INTO bundles VALUES (19198,5822,948); -- Dweomer Bullet
INSERT INTO bundles VALUES (21331,6271,948); -- Eminent Bullet
INSERT INTO bundles VALUES (17312,5353,948); -- Iron Bullet
INSERT INTO bundles VALUES (21339,6142,948); -- Midrium Bullet
INSERT INTO bundles VALUES (19199,5823,948); -- Oberon's Bullet
INSERT INTO bundles VALUES (19802,5914,948); -- Orichalcum Bullet
INSERT INTO bundles VALUES (17341,5340,948); -- Silver Bullet
INSERT INTO bundles VALUES (18160,5341,948); -- Spartan Bullet
INSERT INTO bundles VALUES (18723,5416,948); -- Steel Bullet
INSERT INTO bundles VALUES (21335,6209,948); -- Titanium Bullet

INSERT INTO bundles VALUES (2176,5402,948); -- Fire Card
INSERT INTO bundles VALUES (2177,5403,948); -- Ice Card
INSERT INTO bundles VALUES (2178,5404,948); -- Wind Card
INSERT INTO bundles VALUES (2179,5405,948); -- Earth Card
INSERT INTO bundles VALUES (2180,5406,948); -- Thunder Card
INSERT INTO bundles VALUES (2181,5407,948); -- Water Card
INSERT INTO bundles VALUES (2182,5408,948); -- Light Card
INSERT INTO bundles VALUES (2183,5409,948); -- Dark Card
INSERT INTO bundles VALUES (2974,5870,948); -- Trump Card
;
INSERT INTO bundles VALUES (2973,5869,951); -- Chonofuda
INSERT INTO bundles VALUES (8804,6266,951); -- Furusumi
INSERT INTO bundles VALUES (1173,5312,951); -- Hiraishin
INSERT INTO bundles VALUES (2643,5864,951); -- Jinko
INSERT INTO bundles VALUES (1182,5315,951); -- Jusatsu
INSERT INTO bundles VALUES (2642,5863,951); -- Kabenro
INSERT INTO bundles VALUES (1185,5316,951); -- Kaginawa
INSERT INTO bundles VALUES (1167,5310,951); -- Kawahori-Ogi
INSERT INTO bundles VALUES (1191,5318,951); -- Kodoku
INSERT INTO bundles VALUES (2971,5867,951); -- Inoshishinofuda
INSERT INTO bundles VALUES (1170,5311,951); -- Makibishi
INSERT INTO bundles VALUES (1176,5313,951); -- Mizu-Deppo
INSERT INTO bundles VALUES (2970,5866,951); -- Mokujin
INSERT INTO bundles VALUES (8803,6265,951); -- Ranka
INSERT INTO bundles VALUES (2644,5865,951); -- Ryuno
INSERT INTO bundles VALUES (1188,5317,951); -- Sairui-Ran
INSERT INTO bundles VALUES (2553,5417,951); -- Sanjaku-Tenugui
INSERT INTO bundles VALUES (1179,5314,951); -- Shihei
INSERT INTO bundles VALUES (2972,5868,951); -- Shikanofuda
INSERT INTO bundles VALUES (1194,5319,951); -- Shinobi-Tabi
INSERT INTO bundles VALUES (2555,5734,951); -- Soshi
INSERT INTO bundles VALUES (1164,5309,951); -- Tsurara
INSERT INTO bundles VALUES (1161,5308,951); -- Uchitake

INSERT INTO bundles VALUES (17301,6299,951); -- Shuriken
INSERT INTO bundles VALUES (17302,6297,951); -- Juji Shuriken
INSERT INTO bundles VALUES (17303,6298,951); -- Manji Shuriken
INSERT INTO bundles VALUES (17304,6302,951); -- Fuma Shuriken
INSERT INTO bundles VALUES (18712,6300,951); -- Koga Shuriken
INSERT INTO bundles VALUES (19783,6303,951); -- Iga Shuriken
INSERT INTO bundles VALUES (21351,6304,951); -- Roppo Shuriken
INSERT INTO bundles VALUES (21352,6305,951); -- Roppo Shuriken +1
INSERT INTO bundles VALUES (21355,6308,951); -- Hachiya Shuriken
INSERT INTO bundles VALUES (21356,6309,951); -- Suppa Shuriken
INSERT INTO bundles VALUES (21353,6306,951); -- Happo Shuriken
INSERT INTO bundles VALUES (21354,6307,951); -- Happo Shuriken +1
INSERT INTO bundles VALUES (21357,6301,951); -- Togakushi Shuriken
INSERT INTO bundles VALUES (22276,6447,951); -- Sasuke Shuriken
INSERT INTO bundles VALUES (22277,6448,951); -- Sasuke Shuriken +1
