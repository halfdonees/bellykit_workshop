SELECT `DATE`, `SYMBOL`, `OPEN`, `HIGH`, `LOW`, `CLOSE`, `VOLUME`,`ADJ_OPEN` FROM stock.tw_price 
where 
DATE > '2012-01-01'
and SYMBOL in (1101, 1102, 1216, 1301, 1303, 1326,
				1402, 1802, 2002, 2105, 2201, 2207,
				2311, 2324, 2801, 2880, 2881, 2882,
                2883, 2885, 2886, 2890, 2891, 2892,
                5880, 2912, 1722, 6505, 2303, 2330,
                2454, 2301, 2324, 2353, 2457, 2382,
                3231, 2409, 3008, 3481, 3673, 2412,
                2498, 3045, 4904, 2308, 2347, 2317,
                2354, 2474); 