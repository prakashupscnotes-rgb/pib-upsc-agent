"""
Comprehensive UPSC & KEA Geographic Atlas & Hotspot Database:
- Karnataka Complete Atlas (All 31 Districts, Rivers, Mega Dams, National Parks, Peaks)
- India National Atlas (Major Rivers, Dams, Himalayan Passes, Prominent Peaks)
- World Strategic Geography (World Peaks, Mountain Ranges, Global Straits, Ocean Currents, Vegetation Biomes)
"""

KARNATAKA_DISTRICTS = [
    {"name": "Bengaluru Urban", "hq": "Bengaluru", "division": "Bengaluru", "facts": "Silicon Valley of India; highest population density, IT/BT capital, NIMHANS, ISRO HQ."},
    {"name": "Bengaluru Rural", "hq": "Doddaballapura", "division": "Bengaluru", "facts": "Kempegowda International Airport (Devanahalli); silk and horticulture hub."},
    {"name": "Ramanagara", "hq": "Ramanagara", "division": "Bengaluru", "facts": "Silk City (Reshme Nagara); Closepet granites, Ramadevarabetta Vulture Sanctuary."},
    {"name": "Kolar", "hq": "Kolar", "division": "Bengaluru", "facts": "Land of Gold (KGF); leading milk and tomato producing district."},
    {"name": "Chikkaballapura", "hq": "Chikkaballapura", "division": "Bengaluru", "facts": "Birthplace of Sir M. Visvesvaraya (Muddenahalli); Nandi Hills."},
    {"name": "Tumakuru", "hq": "Tumakuru", "division": "Bengaluru", "facts": "Kalpataru Nadu (Coconut land); Pavagada Mega Solar Park (2,050 MW), Siddaganga Matha."},
    {"name": "Shivamogga", "hq": "Shivamogga", "division": "Bengaluru", "facts": "Gateway of Malnad; Jog Falls (Sharavathi river), Linganamakki Dam, Kuvempu's Kuppalli."},
    {"name": "Chitradurga", "hq": "Chitradurga", "division": "Bengaluru", "facts": "Fort City (Kallina Kote / 7-ring fort); Onake Obavva legacy, wind power hub, Vani Vilasa Sagara."},
    {"name": "Davanagere", "hq": "Davanagere", "division": "Bengaluru", "facts": "Manchester of Karnataka; famous Davanagere Benne Dosa, textile center on Tungabhadra."},
    {"name": "Mysuru", "hq": "Mysuru", "division": "Mysuru", "facts": "Heritage Capital of Karnataka; Mysuru Palace, Chamundi Hill, KRS Dam (Brindavan Gardens)."},
    {"name": "Mandya", "hq": "Mandya", "division": "Mysuru", "facts": "Sugar City (Sakkare Nadu); Ranganathittu Bird Sanctuary, Shivanasamudra Falls."},
    {"name": "Hassan", "hq": "Hassan", "division": "Mysuru", "facts": "Architecture capital; Hoysala temples of Belur and Halebidu (UNESCO World Heritage), Gorur Dam."},
    {"name": "Chikkamagaluru", "hq": "Chikkamagaluru", "division": "Mysuru", "facts": "Coffee Land of India; Mullayanagiri (highest peak in Karnataka, 1,930 m), Kudremukh, Bhadra Reserve."},
    {"name": "Kodagu", "hq": "Madikeri", "division": "Mysuru", "facts": "Kashmir of Karnataka; birthplace of River Kaveri (Talakaveri), coffee, pepper, martial culture."},
    {"name": "Dakshina Kannada", "hq": "Mangaluru", "division": "Mysuru", "facts": "Cradle of Indian Banking; New Mangalore Port (NMPT), Netravati river mouth, coastal trade."},
    {"name": "Udupi", "hq": "Udupi", "division": "Mysuru", "facts": "Krishna Matha; Malpe Beach and St. Mary's Island (columnar basaltic lava geological monument)."},
    {"name": "Chamarajanagar", "hq": "Chamarajanagar", "division": "Mysuru", "facts": "Southernmost district; Bandipur National Park, BRT Tiger Reserve, Male Mahadeshwara Hills."},
    {"name": "Belagavi", "hq": "Belagavi", "division": "Belagavi", "facts": "Second capital (Suvarna Vidhana Soudha); Kittur Rani Chennamma legacy, Hidkal Dam on Ghataprabha."},
    {"name": "Bagalkote", "hq": "Bagalkote", "division": "Belagavi", "facts": "Cradle of temple architecture; Badami cave temples, Aihole, Pattadakal (UNESCO World Heritage)."},
    {"name": "Vijayapura", "hq": "Vijayapura", "division": "Belagavi", "facts": "Adil Shahi heritage; Gol Gumbaz (whispering gallery), Almatti Dam (Lal Bahadur Shastri Reservoir)."},
    {"name": "Dharwad", "hq": "Dharwad", "division": "Belagavi", "facts": "Cultural & educational capital; Dharwad Peda, Karnatak University, IIT Dharwad."},
    {"name": "Gadag", "hq": "Gadag-Betageri", "division": "Belagavi", "facts": "First Co-operative movement in Asia (Kanaginahal); Western Chalukya temples, printing press hub."},
    {"name": "Haveri", "hq": "Haveri", "division": "Belagavi", "facts": "Cardamom garland city (Yelakki Ooru); Byadgi Chilli (GI tag), Santa Shishunala Sharifa shrine."},
    {"name": "Uttara Kannada", "hq": "Karwar", "division": "Belagavi", "facts": "Largest forest district; Kali river, Supa Dam, Kaiga Atomic Power Station, Dandeli-Anshi Tiger Reserve."},
    {"name": "Ballari", "hq": "Ballari", "division": "Kalaburagi", "facts": "Iron ore capital; Sandur Manganese & Iron Ores, historical fort."},
    {"name": "Vijayanagara", "hq": "Hosapete", "division": "Kalaburagi", "facts": "31st District of Karnataka (carved from Ballari); UNESCO World Heritage Hampi, Tungabhadra Dam."},
    {"name": "Koppal", "hq": "Koppal", "division": "Kalaburagi", "facts": "Kinhal craft (GI tag); Anegundi (Kishkindha in Ramayana), rice bowl on Tungabhadra."},
    {"name": "Raichur", "hq": "Raichur", "division": "Kalaburagi", "facts": "Raichur Doab (fertile land between Krishna & Tungabhadra); Raichur Thermal Power Station (RTPS)."},
    {"name": "Kalaburagi", "hq": "Kalaburagi", "division": "Kalaburagi", "facts": "Tur Bowl of Karnataka (Kalaburagi Red Gram GI tag); Bahmani capital, Gulbarga Fort, Central University."},
    {"name": "Yadgir", "hq": "Yadgir", "division": "Kalaburagi", "facts": "Uranium deposits in Gogi; Shorapur Sansthana, Krishna and Bhima river confluence."},
    {"name": "Bidar", "hq": "Bidar", "division": "Kalaburagi", "facts": "Crown of Karnataka; Bidriware metallic craft (GI tag), Mahmud Gawan Madrasa, Gurudwara Nanak Jhira."}
]

KARNATAKA_RIVERS_DAMS = [
    {"name": "KRS Dam (Krishna Raja Sagara)", "river": "Kaveri", "lat": 12.42, "lon": 76.57, "district": "Mandya", "facts": "Built by Sir M. Visvesvaraya under Nalvadi Krishnaraja Wadiyar (1932); Brindavan Gardens."},
    {"name": "Almatti Dam (Lal Bahadur Shastri Res.)", "river": "Krishna", "lat": 16.33, "lon": 75.88, "district": "Vijayapura/Bagalkote", "facts": "Main reservoir of the Upper Krishna Project (UKP); key irrigation lifeline of Northern Karnataka."},
    {"name": "Tungabhadra Dam (Pampa Sagara)", "river": "Tungabhadra", "lat": 15.26, "lon": 76.34, "district": "Vijayanagara", "facts": "Interstate project with Andhra Pradesh; irrigates Raichur, Ballari, and Koppal."},
    {"name": "Linganamakki Dam", "river": "Sharavathi", "lat": 14.19, "lon": 74.84, "district": "Shivamogga", "facts": "Feeds Mahatma Gandhi Hydroelectric Project and Sharavathi Generating Station; near Jog Falls."},
    {"name": "Supa Dam", "river": "Kali", "lat": 15.28, "lon": 74.53, "district": "Uttara Kannada", "facts": "Second largest dam in Karnataka; concrete gravity dam powering Kali Hydroelectric Project."},
    {"name": "Gorur Dam", "river": "Hemavathi", "lat": 12.78, "lon": 76.05, "district": "Hassan", "facts": "Constructed across River Hemavathi, an important tributary of Kaveri."},
    {"name": "Kabini Dam", "river": "Kabini", "lat": 11.97, "lon": 76.35, "district": "Mysuru", "facts": "Located near HD Kote; crucial drinking water supply for Bengaluru and Mysuru; rich wildlife catchment."},
    {"name": "Vani Vilasa Sagara (Mari Kanive)", "river": "Vedavathi", "lat": 13.98, "lon": 76.47, "district": "Chitradurga", "facts": "Oldest modern dam in Karnataka (1907); built by Mysore royalty before independence."}
]

KARNATAKA_NATIONAL_PARKS = [
    {"name": "Bandipur National Park", "lat": 11.66, "lon": 76.62, "type": "Tiger Reserve", "facts": "Established under Project Tiger in 1973; part of Nilgiri Biosphere Reserve; highest tiger and elephant density."},
    {"name": "Nagarahole National Park", "lat": 12.02, "lon": 76.15, "type": "Tiger Reserve", "facts": "Also known as Rajiv Gandhi NP; Kabini river separates it from Bandipur; major Asiatic elephant habitat."},
    {"name": "Kudremukh National Park", "lat": 13.21, "lon": 75.25, "type": "National Park", "facts": "Shola-grassland ecosystem in the Western Ghats; iron ore mining permanently banned by Supreme Court."},
    {"name": "Anshi National Park (Kali Tiger Reserve)", "lat": 15.00, "lon": 74.37, "type": "Tiger Reserve", "facts": "Dense evergreen rainforest along Kali river; home to rare Black Panther (melanistic leopard)."},
    {"name": "Bannerghatta National Park", "lat": 12.80, "lon": 77.57, "type": "Biological Park", "facts": "Located just 22 km south of Bengaluru; hosts India's first butterfly park and elephant sanctuary."}
]

INDIA_PASSES_PEAKS_DAMS = [
    {"name": "Tehri Dam (Uttarakhand)", "category": "Mega Dam", "lat": 30.37, "lon": 78.48, "facts": "Highest dam in India (260.5 m); rock and earth-fill embankment on the Bhagirathi river."},
    {"name": "Bhakra Nangal Dam (Himachal/Punjab)", "category": "Mega Dam", "lat": 31.41, "lon": 76.43, "facts": "Concrete gravity dam on the Sutlej river; reservoir is Gobind Sagar."},
    {"name": "Sardar Sarovar Dam (Gujarat)", "category": "Mega Dam", "lat": 21.83, "lon": 73.74, "facts": "Gravity dam on Narmada River; provides irrigation to Gujarat and Rajasthan."},
    {"name": "Hirakud Dam (Odisha)", "category": "Mega Dam", "lat": 21.52, "lon": 83.87, "facts": "Longest earthen dam in the world (25.8 km) built across River Mahanadi."},
    {"name": "Zoji La Pass", "category": "Himalayan Pass", "lat": 34.28, "lon": 75.50, "facts": "Strategic mountain pass in Ladakh (3,528 m); connects Srinagar with Kargil and Leh; Zojila Tunnel underway."},
    {"name": "Shipki La Pass", "category": "Himalayan Pass", "lat": 31.81, "lon": 78.74, "facts": "Himachal Pradesh border pass with Tibet; River Sutlej enters India through this gorge."},
    {"name": "Nathu La Pass", "category": "Himalayan Pass", "lat": 27.38, "lon": 88.83, "facts": "Sikkim border pass (4,310 m) with Tibet; offshoot of historic Old Silk Route; reopened for trade in 2006."},
    {"name": "Lipulekh Pass", "category": "Himalayan Pass", "lat": 30.23, "lon": 81.04, "facts": "Tri-junction between India (Uttarakhand), Nepal, and China; Kailash Mansarovar pilgrimage route."},
    {"name": "Kanchenjunga (8,586 m)", "category": "Peak", "lat": 27.70, "lon": 88.14, "facts": "Third highest mountain in the world; highest in sovereign India; UNESCO Mixed World Heritage Site."},
    {"name": "Anamudi (2,695 m)", "category": "Peak", "lat": 10.17, "lon": 77.06, "facts": "Highest peak in Western Ghats and entire South India; located in Eravikulam National Park, Kerala."}
]

WORLD_GEOGRAPHY_HOTSPOTS = [
    {"name": "Mount Everest (8,848.86 m)", "category": "World Peak", "lat": 27.98, "lon": 86.92, "facts": "Highest peak on Earth; located in Mahalangur Himal sub-range of the Himalayas on Nepal-China border."},
    {"name": "Aconcagua (6,961 m)", "category": "World Peak", "lat": -32.65, "lon": -70.01, "facts": "Highest peak in the Western and Southern Hemispheres; located in the Andes range (Argentina)."},
    {"name": "Mount Kilimanjaro (5,895 m)", "category": "World Peak", "lat": -3.06, "lon": 37.35, "facts": "Highest free-standing mountain in the world; dormant stratovolcano in Tanzania, Africa."},
    {"name": "Strait of Malacca", "category": "Strategic Strait", "lat": 2.50, "lon": 101.50, "facts": "Main maritime corridor between the Indian and Pacific Oceans; handles over 25% of global traded goods."},
    {"name": "Bab-el-Mandeb Strait", "category": "Strategic Strait", "lat": 12.58, "lon": 43.33, "facts": "Connects Red Sea to Gulf of Aden; Yemen and Djibouti coastlines; critical Suez Canal maritime gate."},
    {"name": "Strait of Hormuz", "category": "Strategic Strait", "lat": 26.56, "lon": 56.25, "facts": "World's most critical oil transit chokepoint between Persian Gulf and Gulf of Oman (Iran / Oman)."},
    {"name": "Strait of Gibraltar", "category": "Strategic Strait", "lat": 35.96, "lon": -5.60, "facts": "Connects Atlantic Ocean to Mediterranean Sea; separates Spain (Europe) from Morocco (Africa)."},
    {"name": "Gulf Stream & North Atlantic Drift", "category": "Ocean Current", "lat": 35.00, "lon": -60.00, "facts": "Powerful warm current originating in Gulf of Mexico; keeps ports of Western & Northern Europe ice-free in winter."},
    {"name": "Peru / Humboldt Current", "category": "Ocean Current", "lat": -15.00, "lon": -80.00, "facts": "Cold current along Western South America; responsible for creating the hyper-arid Atacama Desert; disrupted by El Niño."},
    {"name": "Benguela Current", "category": "Ocean Current", "lat": -25.00, "lon": 12.00, "facts": "Cold ocean current along the southwest coast of Africa; directly creates the Namib Desert desiccation."}
]

WORLD_VEGETATION_BIOMES = [
    {
        "biome": "Tropical Rainforest (Selvas)",
        "regions": "Amazon Basin, Congo Basin, Indo-Malayan realm, Western Ghats (India)",
        "climate": "High temperatures (25-30°C) and heavy rainfall throughout the year (>200 cm); no dry season.",
        "characteristics": "Multi-layered dense canopy (Emergent, Canopy, Understory, Forest Floor); highest terrestrial biodiversity; epiphytes and lianas abundant; laterite soils prone to heavy leaching."
    },
    {
        "biome": "Savanna / Tropical Grassland",
        "regions": "Llanos (Venezuela), Campos (Brazil), African Savannas, parts of Deccan Plateau",
        "climate": "Distinct alternating wet and dry seasons; annual rainfall 75-150 cm.",
        "characteristics": "Coarse tall grasses (elephant grass) with scattered drought-resistant deciduous trees (acacias, baobabs); 'Big Game Country' supporting huge herbivore-carnivore food webs."
    },
    {
        "biome": "Mediterranean Biome",
        "regions": "Mediterranean coast, Central California, Central Chile, Cape Province (South Africa), SW Australia",
        "climate": "Dry hot summers and mild, rainy winters; influenced by shifting subtropical high-pressure belts.",
        "characteristics": "Sclerophyllous vegetation with thick waxy leaves, gnarled bark (chaparral, maquis, cork oak); world's orchard known for citrus fruits, olives, viticulture (grapes)."
    },
    {
        "biome": "Taiga / Boreal Coniferous Forest",
        "regions": "Circumpolar belt across Northern Eurasia (Siberia) and North America (Canada, Alaska)",
        "climate": "Extremely cold prolonged winters and short mild summers; low precipitation mostly as snow.",
        "characteristics": "Monoculture stands of needle-leaved evergreen softwoods (pine, spruce, fir, larch); acidic, nutrient-poor Podzol soils; world's leading source of softwood pulp and timber."
    },
    {
        "biome": "Tundra Biome",
        "regions": "Arctic fringe north of Arctic Circle, tree line in Eurasia and North America",
        "climate": "Polar climate with freezing temperatures most of the year; continuous daylight in short summer.",
        "characteristics": "Treeless biome; presence of permanently frozen subsoil (Permafrost); dwarf shrubs, sedges, mosses, and lichens (reindeer moss); fauna includes musk ox, arctic fox, caribou."
    }
]
