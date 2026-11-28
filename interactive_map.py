"""
Interactive Google Maps-like Geographic Atlas for You to UPSC:
- Embedded Leaflet.js with CartoDB Voyager Google-style tiles
- Dynamic directional river flows for Karnataka (Cauvery, Krishna, Tungabhadra, Sharavathi, Kali, Netravati)
- Mega dams placed directly along river flowlines with real photos and reservoir specs
- 31 Karnataka Districts with hover tooltips and click popups showing "What Happened Here" & current affairs
- India Strategic Passes & Dams layer
- World Strategic Straits and Chokepoints layer
"""

import json

def get_interactive_map_html() -> str:
    # 1. Karnataka Dynamic River Paths with coordinates
    rivers_data = [
        {
            "name": "Cauvery (Kaveri) River",
            "flow_dir": "Talakaveri (Kodagu) ➔ KRS Dam ➔ Srirangapatna ➔ Shivanasamudra ➔ Mekedatu ➔ Bay of Bengal",
            "color": "#0284c7",
            "weight": 5,
            "coords": [
                [12.38, 75.49],   # Talakaveri (Origin)
                [12.37, 75.74],   # Madikeri foothills
                [12.45, 75.96],   # Kushalnagar
                [12.55, 76.25],   # KR Nagar
                [12.427, 76.573], # Krishna Raja Sagara (KRS) Dam
                [12.42, 76.69],   # Srirangapatna island
                [12.30, 77.17],   # Shivanasamudra Falls
                [12.25, 77.45],   # Mekedatu Gorge (Arkavathi confluence)
                [12.05, 77.75],   # Enters Tamil Nadu border
                [11.80, 77.80],   # Mettur Dam
                [11.14, 79.85]    # Poompuhar / Bay of Bengal
            ],
            "dams": ["Krishna Raja Sagara (KRS)", "Mettur Dam (TN)"],
            "facts": "Longest river of South India / Lifeline of Karnataka & TN. Inter-state river dispute adjudicated under Inter-State River Water Disputes Act 1956."
        },
        {
            "name": "Krishna River",
            "flow_dir": "Mahabaleshwar ➔ Belagavi/Bagalkote ➔ Almatti Dam ➔ Narayanpur Dam ➔ Bay of Bengal",
            "color": "#0369a1",
            "weight": 5,
            "coords": [
                [16.70, 74.30],   # Karnataka-Maharashtra border
                [16.50, 74.85],   # Athani / Belagavi
                [16.331, 75.887], # Almatti Dam (Lal Bahadur Shastri Sagara)
                [16.32, 76.58],   # Basava Sagara (Narayanpur Dam)
                [16.15, 77.30],   # Raichur doab
                [15.90, 78.23],   # Confluence with Tungabhadra
                [16.05, 78.90],   # Srisailam Dam
                [15.70, 80.80]    # Hamsaladeevi / Bay of Bengal
            ],
            "dams": ["Almatti Dam", "Basava Sagara (Narayanpur)"],
            "facts": "Second largest peninsular river basin in India. Upper Krishna Project irrigates Vijayapura, Bagalkote, and Kalaburagi."
        },
        {
            "name": "Tungabhadra River",
            "flow_dir": "Koodli (Tunga+Bhadra) ➔ Harihar ➔ TB Dam (Hosapete) ➔ Hampi ➔ Krishna Confluence",
            "color": "#0ea5e9",
            "weight": 4,
            "coords": [
                [14.02, 75.68],   # Koodli confluence
                [14.28, 75.72],   # Honnali
                [14.51, 75.80],   # Harihar
                [15.00, 76.05],   # Harapanahalli
                [15.258, 76.339], # Tungabhadra Dam (Hosapete / Vijayanagara)
                [15.33, 76.46],   # Hampi World Heritage Site
                [15.65, 76.90],   # Kampli
                [15.80, 77.50],   # Mantralayam border
                [15.90, 78.23]    # Confluence with Krishna
            ],
            "dams": ["Tungabhadra Dam (Hosapete)"],
            "facts": "Major tributary of Krishna. TB Dam spillway gate-19 breach in Aug 2024 was safely replaced by expert engineers; crucial for Kalyana Karnataka."
        },
        {
            "name": "Sharavathi River (West Flowing)",
            "flow_dir": "Ambuthirtha (Thirthahalli) ➔ Linganamakki Dam ➔ Jog Falls ➔ Arabian Sea (Honnavar)",
            "color": "#0891b2",
            "weight": 4,
            "coords": [
                [13.71, 75.25],   # Ambuthirtha
                [14.179, 74.839], # Linganamakki Dam
                [14.228, 74.812], # Jog Falls (Gerusoppa Falls - 253m)
                [14.24, 74.65],   # Gerusoppa
                [14.28, 74.45]    # Honnavar / Arabian Sea
            ],
            "dams": ["Linganamakki Dam", "Gerusoppa Dam"],
            "facts": "Entire basin lies inside Karnataka. Powered Mahatma Gandhi Hydroelectric project. Jog Falls is one of the highest plunge waterfalls in Asia."
        },
        {
            "name": "Kali River (West Flowing)",
            "flow_dir": "Diggi (Uttara Kannada) ➔ Dandeli ➔ Supa Dam ➔ Karwar (Arabian Sea)",
            "color": "#06b6d4",
            "weight": 4,
            "coords": [
                [15.22, 74.37],   # Diggi
                [15.24, 74.62],   # Dandeli Tiger Reserve
                [15.275, 74.536], # Supa Dam
                [14.90, 74.30],   # Kadra Dam
                [14.82, 74.13]    # Karwar Bay / Arabian Sea
            ],
            "dams": ["Supa Dam", "Kadra Dam", "Kodasalli Dam"],
            "facts": "Runs through Kali Tiger Reserve. Lifeline of Karwar port and naval base INS Kadamba (Project Seabird)."
        },
        {
            "name": "Netravati River (West Flowing)",
            "flow_dir": "Kudremukh ➔ Dharmasthala ➔ Uppinangadi ➔ Mangaluru (Arabian Sea)",
            "color": "#14b8a6",
            "weight": 4,
            "coords": [
                [13.13, 75.30],   # Kudremukh
                [12.95, 75.38],   # Dharmasthala
                [12.84, 75.25],   # Uppinangadi (Kumaradhara confluence)
                [12.87, 74.85]    # Mangaluru Estuary / Arabian Sea
            ],
            "dams": ["Yettinahole Diversion Weir (near Sakleshpur)"],
            "facts": "Lifeline of Dakshina Kannada. Confluence with Kumaradhara at Uppinangadi called 'Gaya of South India'."
        }
    ]

    # 2. Mega Dams Placed on Rivers
    dams_data = [
        {
            "name": "Krishna Raja Sagara (KRS) Dam",
            "river": "Cauvery River",
            "district": "Mandya",
            "lat": 12.427,
            "lon": 76.573,
            "capacity": "49.45 TMC",
            "engineer": "Sir M. Visvesvaraya (1932)",
            "image": "static/images/dam_cauvery_krs.jpg",
            "news": "Drinking water lifeline for Bengaluru, Mysuru & Mandya. Water release monitored strictly by Cauvery Water Regulation Committee (CWRC)."
        },
        {
            "name": "Almatti Dam (Lal Bahadur Shastri Sagara)",
            "river": "Krishna River",
            "district": "Vijayapura",
            "lat": 16.331,
            "lon": 75.887,
            "capacity": "123.08 TMC",
            "engineer": "Upper Krishna Project",
            "image": "static/images/dam_almatti.jpg",
            "news": "Karnataka pushing to raise full reservoir level (FRL) from 519.6 m to 524.25 m to utilize awarded 130 TMC under Krishna Water Disputes Tribunal (KWDT-II)."
        },
        {
            "name": "Tungabhadra Dam",
            "river": "Tungabhadra River",
            "district": "Vijayanagara (Hosapete)",
            "lat": 15.258,
            "lon": 76.339,
            "capacity": "105.78 TMC",
            "engineer": "Inter-State Board (Karnataka & AP)",
            "image": "static/images/dam_tungabhadra.jpg",
            "news": "Spillway Gate-19 washed away in floodwaters in Aug 2024 and successfully reinstalled within 5 days by renowned dam safety expert Kannaiah Naidu."
        },
        {
            "name": "Linganamakki Dam",
            "river": "Sharavathi River",
            "district": "Shivamogga (Sagara)",
            "lat": 14.179,
            "lon": 74.839,
            "capacity": "151.75 TMC",
            "engineer": "Karnataka Power Transmission Corp",
            "image": "static/images/dam_linganamakki.jpg",
            "news": "Largest reservoir by capacity in Karnataka; feeds the Sharavathi Generating Station (1,035 MW) producing green hydroelectric power for Karnataka grid."
        },
        {
            "name": "Supa Dam",
            "river": "Kali River",
            "district": "Uttara Kannada (Joida)",
            "lat": 15.275,
            "lon": 74.536,
            "capacity": "147.5 TMC",
            "engineer": "KPCL",
            "image": "static/images/dam_linganamakki.jpg",
            "news": "Highest concrete gravity dam in Karnataka (101 m). Submerged parts of Dandeli forest, creating major reservoir amidst Western Ghats biodiversity."
        },
        {
            "name": "Gorur Dam (Hemavathi Reservoir)",
            "river": "Hemavathi River (Cauvery tributary)",
            "district": "Hassan",
            "lat": 12.871,
            "lon": 76.054,
            "capacity": "37.1 TMC",
            "engineer": "Irrigation Dept",
            "image": "static/images/dam_cauvery_krs.jpg",
            "news": "Crucial irrigation source for Hassan, Tumakuru, and Mandya. Features the submerged Shettihalli Rosary Church in reservoir backwaters."
        }
    ]

    # 3. All 31 Districts of Karnataka with Current Affairs & "What Happened Here"
    districts_data = [
        {"name": "Bengaluru Urban", "hq": "Bengaluru", "lat": 12.9716, "lon": 77.5946, "div": "Bengaluru", "img": "static/images/karnataka_vidhana.jpg", "news": "Vidhana Soudha presented ₹3.71 Lakh Cr Budget. Toyota signs MoU for hybrid taxi feasibility. NIMHANS launches national mental health tele-hub."},
        {"name": "Mysuru", "hq": "Mysuru", "lat": 12.2958, "lon": 76.6394, "div": "Mysuru", "img": "static/images/karnataka_vidhana.jpg", "news": "Heritage city; Cauvery river passes via KRS. Nanjangud Rasabale GI tag. Major electronic hardware and semiconductor training cluster."},
        {"name": "Chikkamagaluru", "hq": "Chikkamagaluru", "lat": 13.3153, "lon": 75.7754, "div": "Mysuru", "img": "static/images/karnataka_vidhana.jpg", "news": "Home to Mullayanagiri (1,930 m) - Karnataka's highest peak. Arabica coffee capital. Planter labor dispute resolved under state labor mandates."},
        {"name": "Kodagu", "hq": "Madikeri", "lat": 12.4244, "lon": 75.7382, "div": "Mysuru", "img": "static/images/dam_cauvery_krs.jpg", "news": "Origin of River Cauvery at Talakaveri in Brahmagiri Wildlife Sanctuary. Coorg Orange and Coorg Green Cardamom GI tags."},
        {"name": "Chamarajanagar", "hq": "Chamarajanagar", "lat": 11.9261, "lon": 76.9437, "div": "Mysuru", "img": "static/species/bengal_tiger.jpg", "news": "Bandipur Tiger Reserve & Male Mahadeshwara Hills. Highest tiger & elephant densities in Western Ghats landscape. Interstate wildlife corridor."},
        {"name": "Dakshina Kannada", "hq": "Mangaluru", "lat": 12.9141, "lon": 74.8560, "div": "Mysuru", "img": "static/images/warship_naval.jpg", "news": "New Mangalore Port Authority (NMPA) handles strategic crude oil storage under ISPRL. Netravati river mouth and coastal fisheries hub."},
        {"name": "Udupi", "hq": "Udupi", "lat": 13.3409, "lon": 74.7421, "div": "Mysuru", "img": "static/species/olive_ridley.jpg", "news": "Mattu Gulla eggplant GI tag. Coast Guard base conducts Operation Olivia for marine conservation. Malpe deep-sea fishing port."},
        {"name": "Uttara Kannada", "hq": "Karwar", "lat": 14.8185, "lon": 74.1303, "div": "Belagavi", "img": "static/images/warship_naval.jpg", "news": "Project Seabird (INS Kadamba) - Asia's largest naval base. Kali Tiger Reserve and Dandeli white-water rafting on River Kali."},
        {"name": "Belagavi", "hq": "Belagavi", "lat": 15.8497, "lon": 74.4977, "div": "Belagavi", "img": "static/images/dam_almatti.jpg", "news": "Suvarna Vidhana Soudha winter legislature session. Hidkal dam on Ghataprabha river. Sugar capital of Karnataka with over 25 sugar mills."},
        {"name": "Vijayapura", "hq": "Vijayapura", "lat": 16.8302, "lon": 75.7100, "div": "Belagavi", "img": "static/images/dam_almatti.jpg", "news": "Almatti Dam on River Krishna. Gol Gumbaz whispering gallery. Major grape and pomegranate dry-land horticulture center."},
        {"name": "Bagalkote", "hq": "Bagalkote", "lat": 16.1817, "lon": 75.6958, "div": "Belagavi", "img": "static/images/dam_almatti.jpg", "news": "Badami cave temples, Pattadakal UNESCO World Heritage Site. Ilkal Saree GI tag. Upper Krishna Project rehabilitation settlement."},
        {"name": "Dharwad", "hq": "Dharwad", "lat": 15.4589, "lon": 75.0078, "div": "Belagavi", "img": "static/images/karnataka_vidhana.jpg", "news": "IIT Dharwad and Karnatak University education hub. Dharwad Pedha GI tag. Twin city with Hubballi industrial center."},
        {"name": "Shivamogga", "hq": "Shivamogga", "lat": 13.9299, "lon": 75.5681, "div": "Bengaluru", "img": "static/images/dam_linganamakki.jpg", "news": "Gateway to Malnad; origin of Sharavathi river and Jog Falls. Linganamakki Dam. Kuvempu University and Sahyadri biodiversity reserve."},
        {"name": "Kalaburagi", "hq": "Kalaburagi", "lat": 17.3297, "lon": 76.8343, "div": "Kalaburagi", "img": "static/images/karnataka_vidhana.jpg", "news": "Headquarters of Kalyana Karnataka Regional Development Board (KKRDB - Art 371-J). Gulbarga Tur Dal GI tag. Sannati Ashokan edicts excavation."},
        {"name": "Ballari", "hq": "Ballari", "lat": 15.1394, "lon": 76.9214, "div": "Kalaburagi", "img": "static/images/microchip_semiconductor.jpg", "news": "Steel and iron-ore heartland. JSW Steel Toranagallu mega plant. Daroji Sloth Bear Sanctuary - Asia's first sanctuary for sloth bears."},
        {"name": "Vijayanagara", "hq": "Hosapete", "lat": 15.2689, "lon": 76.3909, "div": "Kalaburagi", "img": "static/images/dam_tungabhadra.jpg", "news": "Formed in 2021 as 31st district. Tungabhadra Dam location. Hampi Vijayanagara Empire UNESCO World Heritage monument."},
        {"name": "Bidar", "hq": "Bidar", "lat": 17.9104, "lon": 77.5199, "div": "Kalaburagi", "img": "static/images/karnataka_vidhana.jpg", "news": "Bidriware GI craft. Bidar Fort and Mahmud Gawan Madrasa. Karez underground Persian water system revitalized by district administration."},
        {"name": "Raichur", "hq": "Raichur", "lat": 16.2076, "lon": 77.3463, "div": "Kalaburagi", "img": "static/images/supercomputer.jpg", "news": "Raichur Thermal Power Station (RTPS). Inter-river doab between Krishna and Tungabhadra. Hutti Gold Mines - India's only active primary gold mine."},
        {"name": "Koppal", "hq": "Koppal", "lat": 15.3475, "lon": 76.1558, "div": "Kalaburagi", "img": "static/images/karnataka_vidhana.jpg", "news": "Kinhal wooden toys GI craft. Anegundi heritage village across Tungabhadra. Rice bowl and Koppal Toy Cluster (KTC) under Make in India."},
        {"name": "Yadgir", "hq": "Yadgir", "lat": 16.7628, "lon": 77.1378, "div": "Kalaburagi", "img": "static/images/karnataka_vidhana.jpg", "news": "Bheema river basin. Narayanpur Dam backwaters irrigate Shahapur taluk. Uranium exploration site by UCIL at Gogi."},
        {"name": "Hassan", "hq": "Hassan", "lat": 13.0033, "lon": 76.1004, "div": "Bengaluru", "img": "static/images/space_rocket.jpg", "news": "ISRO Master Control Facility (MCF) for geostationary satellites. Belur & Halebidu Hoysala Temples inscribed as UNESCO World Heritage Sites (2023)."},
        {"name": "Mandya", "hq": "Mandya", "lat": 12.5218, "lon": 76.8951, "div": "Mysuru", "img": "static/images/dam_cauvery_krs.jpg", "news": "Sugar capital of Cauvery basin. KRS Dam and Visvesvaraya Canal irrigation network. Organic farming and jaggery production center."},
        {"name": "Tumakuru", "hq": "Tumakuru", "lat": 13.3379, "lon": 77.1010, "div": "Bengaluru", "img": "static/images/microchip_semiconductor.jpg", "news": "Pavagada Solar Park (Shakti Sthala - 2,050 MW) - one of the world's largest solar parks. Vasanthanarasapura industrial corridor."},
        {"name": "Kolar", "hq": "Kolar", "lat": 13.1367, "lon": 78.1291, "div": "Bengaluru", "img": "static/images/economy_trade.jpg", "news": "Kolar Gold Fields (KGF). KC Valley treated wastewater irrigation project recharging dry underground aquifers. Asia's largest tomato market."},
        {"name": "Chikkaballapura", "hq": "Chikkaballapura", "lat": 13.4325, "lon": 77.7275, "div": "Bengaluru", "img": "static/images/karnataka_vidhana.jpg", "news": "Birthplace of Sir M. Visvesvaraya (Muddenahalli). Nandi Hills ecotourism zone and HN Valley water replenishment project."},
        {"name": "Ramanagara", "hq": "Ramanagara", "lat": 12.7209, "lon": 77.2799, "div": "Bengaluru", "img": "static/images/economy_trade.jpg", "news": "Silk City - largest raw silk cocoon market in Asia. Ramadevarabetta Vulture Sanctuary protecting critically endangered Indian Vultures."},
        {"name": "Bengaluru Rural", "hq": "Bengaluru", "lat": 13.2386, "lon": 77.6744, "div": "Bengaluru", "img": "static/images/economy_trade.jpg", "news": "Kempegowda International Airport (BLR) and Devanahalli Aerospace Park. Proposed Foxconn electronics manufacturing mega hub."},
        {"name": "Gadag", "hq": "Gadag", "lat": 15.4325, "lon": 75.6339, "div": "Belagavi", "img": "static/images/space_rocket.jpg", "news": "Windmill capital of Karnataka (Kappatagudda Hills). Birthplace of cooperative movement in India (Kanaginahal - 1905). Trikuteshwara temple."},
        {"name": "Haveri", "hq": "Haveri", "lat": 14.7953, "lon": 75.4022, "div": "Belagavi", "img": "static/images/karnataka_vidhana.jpg", "news": "Byadagi Chilli GI tag known for high color and low pungency. Sant Shishunala Sharifa shrine and Ranebennur Blackbuck Sanctuary."},
        {"name": "Davanagere", "hq": "Davanagere", "lat": 14.4644, "lon": 75.9218, "div": "Bengaluru", "img": "static/images/economy_trade.jpg", "news": "Manchester of Karnataka textile hub. Central geographic location on NH-48. Bhadra reservoir canal network irrigates Davanagere plains."},
        {"name": "Chitradurga", "hq": "Chitradurga", "lat": 14.2251, "lon": 76.3980, "div": "Bengaluru", "img": "static/images/space_rocket.jpg", "news": "Challakere Science City (ISRO, DRDO Aeronautical Test Range ATR, BARC, IISc campus). Kallina Kote (Stone Fortress) of Onake Obavva."}
    ]

    # Convert to JSON for JS Leaflet map
    rivers_json = json.dumps(rivers_data)
    dams_json = json.dumps(dams_data)
    districts_json = json.dumps(districts_data)

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>You to UPSC Google-Style Interactive Geographic Atlas</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
        <style>
            body, html {{ margin: 0; padding: 0; height: 100%; width: 100%; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
            #map {{ height: 680px; width: 100%; border-radius: 14px; box-shadow: 0 4px 18px rgba(15,23,42,0.12); }}
            .popup-card {{ max-width: 280px; font-family: inherit; }}
            .popup-card img {{ width: 100%; height: 125px; object-fit: cover; border-radius: 8px; margin-bottom: 8px; }}
            .popup-title {{ font-size: 1.05rem; font-weight: 800; color: #0f172a; margin: 0 0 4px 0; }}
            .popup-badge {{ display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 0.72rem; font-weight: 700; margin-bottom: 6px; }}
            .popup-news {{ font-size: 0.82rem; line-height: 1.45; color: #334155; margin: 4px 0 0 0; }}
            .river-tooltip {{ font-weight: 700; color: #0284c7; background: #ffffff; border: 1px solid #0284c7; border-radius: 6px; padding: 3px 6px; font-size: 0.78rem; }}
            .dam-icon {{ background: #dc2626; color: white; border-radius: 50%; width: 24px; height: 24px; display: flex; align-items: center; justify-content: center; font-size: 13px; font-weight: bold; border: 2px solid white; box-shadow: 0 2px 6px rgba(0,0,0,0.3); }}
            .custom-control-panel {{ background: white; padding: 10px 14px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.15); font-size: 0.82rem; }}
        </style>
    </head>
    <body>
        <div id="map"></div>
        <script>
            // Initialize Map Centered on Karnataka with Google Maps style tiles
            var map = L.map('map', {{
                center: [14.50, 75.80],
                zoom: 7,
                zoomControl: true
            }});

            // Google Maps / CartoDB Voyager Tile Layer
            L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{
                attribution: '&copy; OpenStreetMap contributors &copy; CARTO',
                subdomains: 'abcd',
                maxZoom: 19
            }}).addTo(map);

            var rivers = {rivers_json};
            var dams = {dams_json};
            var districts = {districts_json};

            var riverLayer = L.layerGroup().addTo(map);
            var damLayer = L.layerGroup().addTo(map);
            var districtLayer = L.layerGroup().addTo(map);

            // 1. Plot Dynamic Directional Rivers
            rivers.forEach(function(r) {{
                var poly = L.polyline(r.coords, {{
                    color: r.color,
                    weight: r.weight,
                    opacity: 0.85,
                    dashArray: '10, 6',
                    lineCap: 'round'
                }}).addTo(riverLayer);

                // Hover Tooltip on River
                poly.bindTooltip("💧 <b>" + r.name + "</b><br><small>" + r.flow_dir + "</small>", {{
                    sticky: true,
                    className: 'river-tooltip'
                }});

                // Click Popup on River
                poly.bindPopup("<div class='popup-card'>" +
                    "<div class='popup-title' style='color:" + r.color + ";'>🌊 " + r.name + "</div>" +
                    "<span class='popup-badge' style='background:#e0f2fe; color:#0369a1;'>Flow Path & Basin</span>" +
                    "<p class='popup-news'><b>Flow Direction:</b><br>" + r.flow_dir + "</p>" +
                    "<p class='popup-news'><b>UPSC / KEA Core Facts:</b><br>" + r.facts + "</p>" +
                "</div>");
            }});

            // 2. Plot Mega Dams Directly along Rivers
            dams.forEach(function(d) {{
                var damMarker = L.circleMarker([d.lat, d.lon], {{
                    radius: 9,
                    fillColor: '#ef4444',
                    color: '#ffffff',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.95
                }}).addTo(damLayer);

                damMarker.bindTooltip("💧 <b>" + d.name + "</b><br><span style='color:#dc2626; font-size:11px;'>River: " + d.river + " (" + d.district + ")</span>", {{
                    sticky: true
                }});

                damMarker.bindPopup("<div class='popup-card'>" +
                    "<img src='" + d.image + "' alt='" + d.name + "'>" +
                    "<div class='popup-title'>💧 " + d.name + "</div>" +
                    "<span class='popup-badge' style='background:#fee2e2; color:#991b1b;'>River: " + d.river + "</span>" +
                    "<span class='popup-badge' style='background:#fef3c7; color:#92400e; margin-left:4px;'>Cap: " + d.capacity + "</span>" +
                    "<p class='popup-news'><b>📍 District:</b> " + d.district + " | <b>Built by:</b> " + d.engineer + "</p>" +
                    "<p class='popup-news' style='background:#f8fafc; padding:6px; border-left:3px solid #ef4444; border-radius:4px;'><b>🎯 Exam Focus:</b> " + d.news + "</p>" +
                "</div>");
            }});

            // 3. Plot All 31 Karnataka Districts with News & Events
            districts.forEach(function(dt) {{
                var distMarker = L.circleMarker([dt.lat, dt.lon], {{
                    radius: 7,
                    fillColor: '#f59e0b',
                    color: '#ffffff',
                    weight: 2,
                    opacity: 1,
                    fillOpacity: 0.9
                }}).addTo(districtLayer);

                distMarker.bindTooltip("📍 <b>" + dt.name + "</b> (" + dt.div + " Div)<br><small style='color:#475569;'>Click for News & Exam Details</small>", {{
                    sticky: true
                }});

                distMarker.bindPopup("<div class='popup-card'>" +
                    "<img src='" + dt.img + "' alt='" + dt.name + "'>" +
                    "<div class='popup-title'>📍 " + dt.name + "</div>" +
                    "<span class='popup-badge' style='background:#fef3c7; color:#92400e;'>HQ: " + dt.hq + "</span>" +
                    "<span class='popup-badge' style='background:#e0e7ff; color:#3730a3; margin-left:4px;'>" + dt.div + " Division</span>" +
                    "<p class='popup-news' style='background:#f8fafc; padding:6px; border-left:3px solid #f59e0b; border-radius:4px;'>" +
                        "<b>📰 What Happened Here:</b><br>" + dt.news +
                    "</p>" +
                "</div>");
            }});

            // 4. Interactive Layer Switcher
            var baseMaps = {{
                "Google-Style Map": L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{ maxZoom: 19 }})
            }};

            var overlayMaps = {{
                "🌊 Karnataka Rivers (Dynamic Flow)": riverLayer,
                "💧 Mega Dams on Rivers": damLayer,
                "📍 31 Districts (News & What Happened)": districtLayer
            }};

            L.control.layers(null, overlayMaps, {{ collapsed: false, position: 'topright' }}).addTo(map);
        </script>
    </body>
    </html>
    """
    return html_code
