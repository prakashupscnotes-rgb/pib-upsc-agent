"""
You to UPSC Portal Content Engine:
Official educational knowledge base reflecting user's YouTube channel '@youtoupsc'
and handwritten KEA & UPSC exam framework (Static 8-10 Q + Dynamic 20-25 Q).
"""

# Channel Branding Details
CHANNEL_NAME = "You to Upsc"
CHANNEL_HANDLE = "@youtoupsc"
CHANNEL_TAGLINE = "From Aspiration to Action"
CHANNEL_URL = "https://www.youtube.com/@youtoupsc"

# STATIC CORNER [8-10 Questions Weightage in KEA & UPSC]
STATIC_MODULES = {
    "karnataka_budget": {
        "title": "Karnataka State Budget 2026-27 Core Benchmarks",
        "weightage": "High Yield (KEA 4-5 Questions)",
        "pointers": [
            "• Total Budget Outlay: Estimated at over ₹3.71 Lakh Crore, focusing on human capital and regional infrastructure.",
            "• GSDP Growth: Karnataka GSDP projected to expand at 7.5% - 8.2%, driven by services and high-tech manufacturing.",
            "• Fiscal Prudence: Fiscal deficit pegged within the 3.0% limit stipulated by the Karnataka Fiscal Responsibility Act (KFRA).",
            "• Sectoral Thrust: Heavy outlays for Bengaluru suburban rail, irrigation networks in Upper Krishna & Kalasa-Banduri projects.",
            "• Kalyana Karnataka (Article 371-J): Special development allocation of ₹5,000 Crore administered through KKRDB."
        ]
    },
    "karnataka_economic_survey": {
        "title": "Karnataka Economic Survey Key Findings",
        "weightage": "High Yield (KEA 3-4 Questions)",
        "pointers": [
            "• Tertiary Sector Leadership: Services sector accounts for over 64% of Karnataka's Gross State Value Added (GSVA).",
            "• IT & Biotechnology Hub: Karnataka contributes over 40% of India's total software and electronic service exports.",
            "• Agriculture & Allied: Primary sector employs ~42% of workforce; agro-climatic zones range from coastal to northern dry zones.",
            "• Forest Cover: Western Ghats corridor represents one of the world's eight 'hottest hotspots' of biological diversity.",
            "• Renewable Energy Benchmark: Karnataka ranks among India's top states in installed solar (Pavagada Solar Park) and wind capacity."
        ]
    },
    "karnataka_schemes": {
        "title": "Karnataka Core State Welfare Schemes (Guarantee Framework)",
        "weightage": "High Yield (KEA 4-6 Questions)",
        "pointers": [
            "• Gruha Lakshmi: Direct benefit transfer (DBT) of ₹2,000 per month to women heads of eligible households.",
            "• Yuva Nidhi: Unemployment assistance of ₹3,000/month for degree holders and ₹1,500/month for diploma holders (up to 2 years).",
            "• Shakti Scheme: Free bus transportation for women and transgenders in non-premium KSRTC, BMTC, NWKRTC, and KKRTC buses.",
            "• Anna Bhagya: Supply of 10 kg of food grains per person per month to BPL and Antyodaya cardholders (DBT cash component for 5 kg).",
            "• Gruha Jyothi: Up to 200 units of free domestic electricity per month for registered residential households."
        ]
    },
    "central_schemes": {
        "title": "Central Government Flagship Schemes in News",
        "weightage": "High Yield (UPSC & KEA)",
        "pointers": [
            "• SVAMITVA Scheme: Nodal Ministry: Panchayati Raj. Drone-based survey to issue digitized Property Cards in rural Abadi lands.",
            "• WDC-PMKSY 2.0: Watershed Development Component under Ministry of Rural Development; achieved 89% financial utilization benchmark.",
            "• Dr. Ambedkar Medical Aid Scheme: Up to ₹3.50 Lakh financial assistance for SC/ST patients suffering from life-threatening ailments.",
            "• PM-KISAN: Income support of ₹6,000/year in three equal installments to all landholding farmer families via Aadhaar-seeded bank accounts."
        ]
    }
}

# ACCURATE SPECIES & WILDLIFE IN NEWS (With Real Animal Photography & Official IUCN Tags)
SPECIES_IN_NEWS = [
    {
        "name": "Bengal Tiger (Panthera tigris)",
        "scientific_name": "Panthera tigris tigris",
        "image_url": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?auto=format&fit=crop&w=800&q=80",
        "iucn_status": "Endangered",
        "iucn_badge_color": "#dc2626",
        "wpa_schedule": "Schedule I (Highest Protection)",
        "cites": "Appendix I",
        "karnataka_link": "Karnataka is one of India's premier tiger states with 563+ tigers across Bandipur, Nagarahole, BRT, Bhadra, and Kali Tiger Reserves.",
        "why_in_news": "Celebration of 50+ years of Project Tiger, NTCA national corridor census, and AI-enabled thermal anti-poaching camera surveillance in Bandipur."
    },
    {
        "name": "Asian Elephant (Elephas maximus)",
        "scientific_name": "Elephas maximus indicus",
        "image_url": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?auto=format&fit=crop&w=800&q=80",
        "iucn_status": "Endangered",
        "iucn_badge_color": "#dc2626",
        "wpa_schedule": "Schedule I",
        "cites": "Appendix I",
        "karnataka_link": "Karnataka hosts India's highest elephant population (~6,395 wild elephants). Key habitat includes Mysore Elephant Reserve and Nilgiri Biosphere Reserve.",
        "why_in_news": "Notification of interstate jumbo movement corridors connecting Karnataka, Kerala, and Tamil Nadu; railway sensor deployment to curb elephant-train collisions."
    },
    {
        "name": "Snow Leopard (Panthera uncia)",
        "scientific_name": "Panthera uncia",
        "image_url": "https://images.unsplash.com/photo-1548767797-d8c844163c4c?auto=format&fit=crop&w=800&q=80",
        "iucn_status": "Vulnerable",
        "iucn_badge_color": "#ea580c",
        "wpa_schedule": "Schedule I",
        "cites": "Appendix I",
        "karnataka_link": "High-altitude mountain indicator species found across Ladakh, Himachal Pradesh, Uttarakhand, Sikkim, and Arunachal Pradesh.",
        "why_in_news": "First-ever systematic Snow Leopard Population Assessment in India (SPAI) conducted by Wildlife Institute of India (WII), confirming 718 individuals."
    },
    {
        "name": "Olive Ridley Sea Turtle (Lepidochelys olivacea)",
        "scientific_name": "Lepidochelys olivacea",
        "image_url": "https://images.unsplash.com/photo-1518467166778-b88f373ffec7?auto=format&fit=crop&w=800&q=80",
        "iucn_status": "Vulnerable",
        "iucn_badge_color": "#ea580c",
        "wpa_schedule": "Schedule I",
        "cites": "Appendix I",
        "karnataka_link": "Occasional nesting observed along the Uttara Kannada and Udupi coastlines; major mass nesting (Arribada) occurs at Gahirmatha, Odisha.",
        "why_in_news": "Indian Coast Guard initiates annual 'Operation Olivia' with interceptor boats and TED (Turtle Excluder Devices) to protect synchronized mass nesting."
    },
    {
        "name": "Ganges River Dolphin (Platanista gangetica)",
        "scientific_name": "Platanista gangetica",
        "image_url": "https://images.unsplash.com/photo-1570481662006-a3a1374699e8?auto=format&fit=crop&w=800&q=80",
        "iucn_status": "Endangered",
        "iucn_badge_color": "#dc2626",
        "wpa_schedule": "Schedule I",
        "cites": "Appendix I",
        "karnataka_link": "Freshwater river dolphin inhabiting Ganga-Brahmaputra-Meghna and Karnaphuli-Sangu river systems. India's National Aquatic Animal.",
        "why_in_news": "Launch of hydrophone acoustic detection systems under Project Dolphin across Bihar's Vikramshila Gangetic Dolphin Sanctuary."
    }
]

# PLACES IN NEWS & INTERACTIVE GEOGRAPHY HOTSPOTS
PLACES_IN_NEWS = [
    {
        "name": "Bab-el-Mandeb & Red Sea",
        "lat": 12.58,
        "lon": 43.33,
        "region": "Middle East / Horn of Africa",
        "importance": "Vital maritime choke point connecting the Red Sea to the Gulf of Aden and the Indian Ocean. Critical for global container shipping and energy trade.",
        "upsc_kea_facts": "Bordered by Yemen to the north-east and Djibouti & Eritrea to the south-west. Connects Suez Canal route with Indian Ocean."
    },
    {
        "name": "Strait of Hormuz",
        "lat": 26.56,
        "lon": 56.25,
        "region": "Persian Gulf",
        "importance": "World's most critical crude oil transit passage connecting Persian Gulf with Gulf of Oman and Arabian Sea.",
        "upsc_kea_facts": "Bordered by Iran (north) and Oman & UAE (south). Handles approximately 21 million barrels of crude oil daily."
    },
    {
        "name": "Prayagraj (Triveni Sangam)",
        "lat": 25.43,
        "lon": 81.84,
        "region": "Uttar Pradesh, India",
        "importance": "Sacred confluence of Ganga, Yamuna, and subterranean Saraswati rivers. Venue of Maha Kumbh 2026.",
        "upsc_kea_facts": "Historical site of Samudragupta's Prayag Prashasti (composed by Harishena) inscribed on an Ashokan sandstone pillar."
    },
    {
        "name": "Indian Naval Academy, Ezhimala",
        "lat": 12.01,
        "lon": 75.21,
        "region": "Kannur District, Kerala",
        "importance": "Premier officer training academy for the Indian Navy and Coast Guard. President Droupadi Murmu reviewed the Autumn Passing Out Parade.",
        "upsc_kea_facts": "Located near Mount Deli along the Arabian Sea. Ancient capital of the Mooshika kings."
    },
    {
        "name": "Chikkamagaluru & Western Ghats",
        "lat": 13.31,
        "lon": 75.77,
        "region": "Karnataka, India",
        "importance": "Coffee capital of India (Baba Budan Giri). Center of ecological debates regarding Western Ghats Kasturirangan report.",
        "upsc_kea_facts": "Home to Mullayanagiri (1,930 m), the highest peak in Karnataka. High weightage for KEA Geography questions."
    },
    {
        "name": "NIMHANS & Bengaluru",
        "lat": 12.93,
        "lon": 77.59,
        "region": "Karnataka, India",
        "importance": "National Institute of Mental Health and Neurosciences inaugurated India's most advanced spectral CT brain health facility.",
        "upsc_kea_facts": "Conferred Institute of National Importance status by Parliament in 2012. Nodal agency for the National Tele-Mental Health Programme (Tele-MANAS)."
    },
    {
        "name": "Vaishali",
        "lat": 25.98,
        "lon": 85.12,
        "region": "Bihar, India",
        "importance": "PM dedicated mega infrastructure and railway works. Historical capital of the Licchavis, hailed as one of the world's earliest republics.",
        "upsc_kea_facts": "Held the Second Buddhist Council in 383 BCE. Birthplace of Lord Mahavira (Kundagrama, Vaishali)."
    }
]

# INTERACTIVE PRACTICE QUIZ (Aligned with User's YouTube Channel "You to UPSC")
DAILY_QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "Regarding the Karnataka State Budget 2026-27 (KEA Exam Focus), which statutory body is responsible for monitoring regional allocations under Article 371-J for the Kalyana Karnataka region?",
        "options": [
            "A) Karnataka State Finance Commission (KSFC)",
            "B) Kalyana Karnataka Region Development Board (KKRDB)",
            "C) State Planning Board of Karnataka",
            "D) NITI Aayog Regional Council"
        ],
        "correct_index": 1,
        "explanation": "The Kalyana Karnataka Region Development Board (KKRDB), established under Article 371-J of the Constitution, administers special development funds allocated in the State Budget for the 7 backward northeastern districts of Karnataka."
    },
    {
        "id": 2,
        "question": "Which of the following mountain peaks is the HIGHEST peak in the state of Karnataka?",
        "options": [
            "A) Kudremukh",
            "B) Mullayanagiri",
            "C) Pushpagiri (Kumaraparvatha)",
            "D) Brahmagiri"
        ],
        "correct_index": 1,
        "explanation": "Mullayanagiri, located in the Chandra Drona / Baba Budan Giri range of Chikkamagaluru district, is the highest peak in Karnataka at 1,930 metres (6,330 ft)."
    },
    {
        "id": 3,
        "question": "Under the 'Shakti Scheme' launched by the Government of Karnataka, which category of bus services provides free transportation to women beneficiaries?",
        "options": [
            "A) Airavat Club Class and Flybus",
            "B) Non-premium ordinary and express state transport buses (KSRTC, BMTC, NWKRTC, KKRTC)",
            "C) All interstate luxury private sleeper buses",
            "D) Bengaluru Metro Rail (Namma Metro) only"
        ],
        "correct_index": 1,
        "explanation": "The Shakti Scheme provides 100% free bus travel to domicile women and girl students across Karnataka in ordinary and express city/rural state transport services (KSRTC, BMTC, NWKRTC, KKRTC), excluding luxury premium services like Airavat and Ambari."
    },
    {
        "id": 4,
        "question": "With reference to the National Human Rights Commission (NHRC) of India, which of the following statements is/are correct?\n1. It was established as a statutory body under the Protection of Human Rights Act, 1993.\n2. A retired Judge of the Supreme Court can be appointed as its Chairperson.\n3. It has the power to punish violators of human rights directly with imprisonment.",
        "options": [
            "A) 1 and 2 only",
            "B) 2 and 3 only",
            "C) 1 only",
            "D) 1, 2 and 3"
        ],
        "correct_index": 0,
        "explanation": "Statements 1 and 2 are correct. NHRC is a statutory body under PHRA 1993. Under the 2019 amendment, either a retired Chief Justice of India OR a retired Supreme Court Judge can head it. Statement 3 is incorrect: NHRC does not possess judicial punitive powers; its recommendations are advisory."
    },
    {
        "id": 5,
        "question": "The Bab-el-Mandeb Strait, frequently in current affairs due to maritime commerce security in the Red Sea, directly connects:",
        "options": [
            "A) Persian Gulf and Gulf of Oman",
            "B) Red Sea and Gulf of Aden",
            "C) Mediterranean Sea and Black Sea",
            "D) Arabian Sea and Bay of Bengal"
        ],
        "correct_index": 1,
        "explanation": "Bab-el-Mandeb connects the Red Sea to the Gulf of Aden and the Indian Ocean. It is bounded by Yemen on the Arabian Peninsula and Djibouti and Eritrea on the Horn of Africa."
    }
]
