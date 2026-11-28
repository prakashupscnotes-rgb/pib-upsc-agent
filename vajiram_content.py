FEATURED_HERO_CARDS = [
    {
        "title": "International Day for the Abolition of Slavery",
        "category": "Social Justice & Human Rights",
        "gs_paper": "GS-2",
        "image_url": "https://images.unsplash.com/photo-1532629345422-7515f3d16bb6?auto=format&fit=crop&w=800&q=80",
        "summary": "Focuses on eradicating contemporary forms of slavery, such as human trafficking, forced labour, child exploitation, and modern indentured servitude.",
        "prelims": "• UN General Assembly resolution 317(IV) adopted Convention for Suppression of Traffic in Persons.\\n• Observed annually on December 2.",
        "mains": "Critical for GS-2 Fundamental Rights (Articles 23 and 24 of the Indian Constitution) and global anti-trafficking compliance."
    },
    {
        "title": "Iwo Jima & Western Pacific Mapping",
        "category": "Places in News / Maritime",
        "gs_paper": "GS-1 / Prelims",
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
        "summary": "Volcanic island in the Volcano Islands group of Japan, South of Tokyo. Historic World War II battleground and strategic naval surveillance point.",
        "prelims": "• Located in the Western Pacific Ocean, ~1,200 km south of Tokyo.\\n• Officially named Iwo To by the Geospatial Information Authority of Japan.",
        "mains": "Strategic chokepoints and island defense doctrine in the Indo-Pacific theatre."
    },
    {
        "title": "G V Mavalankar (First Speaker of Lok Sabha)",
        "category": "Polity & Constitutional History",
        "gs_paper": "GS-2",
        "image_url": "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=800&q=80",
        "summary": "Known affectionately as 'Dadasaheb', Ganesh Vasudev Mavalankar was the first Speaker of the Lok Sabha (1952–1956) who established parliamentary precedents.",
        "prelims": "• President of Central Legislative Assembly (1946) & Speaker of Constituent Assembly (Legislative).\\n• Established Parliamentary Committees: Public Accounts & Estimates.",
        "mains": "Evolution of the Office of Speaker, parliamentary independence, and constitutional neutrality."
    },
    {
        "title": "KN-23 Tactical Ballistic Missile",
        "category": "Defence & International Security",
        "gs_paper": "GS-3",
        "image_url": "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?auto=format&fit=crop&w=800&q=80",
        "summary": "Solid-fuel quasi-ballistic missile capable of flying on a depressed trajectory with terminal maneuverability to evade regional missile defense shields.",
        "prelims": "• Estimated range: 450 to 600 km.\\n• Quasi-ballistic trajectory similar to the Russian Iskander-M and Indian Pralay missile.",
        "mains": "Proliferation of short-range ballistic missiles (SRBMs) and implications for regional deterrence."
    },
    {
        "title": "INS Vindhyagiri (Project 17A Stealth Frigate)",
        "category": "Defence & Indigenisation",
        "gs_paper": "GS-3",
        "image_url": "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=800&q=80",
        "summary": "Sixth stealth guided-missile frigate constructed under Project 17A by Garden Reach Shipbuilders & Engineers (GRSE), named after the Karnataka mountain range.",
        "prelims": "• Equipped with BrahMos supersonic cruise missiles & Barak-8 SAM.\\n• Named after Vindhyagiri peak in Shravanabelagola, Karnataka.",
        "mains": "Atmanirbhar Bharat in naval defence production, blue-water capability, and Indo-Pacific maritime readiness."
    },
    {
        "title": "ICCAT (Conservation of Atlantic Tunas)",
        "category": "Environment & International Bodies",
        "gs_paper": "GS-3",
        "image_url": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80",
        "summary": "Inter-governmental fishery organization responsible for the conservation of tunas and tuna-like species in the Atlantic Ocean and adjacent seas.",
        "prelims": "• Established in 1966 under the International Convention for the Conservation of Atlantic Tunas.\\n• Secretariat: Madrid, Spain.",
        "mains": "Sustainable marine fisheries management, UN Convention on Law of the Sea (UNCLOS), and multilateral conservation."
    }
]

def get_article_thumbnail(title: str, content: str = "", subject: str = "", pillar: str = "") -> str:
    """Intelligently returns a high-quality educational image matching the article topic."""
    text = f"{title} {content} {subject} {pillar}".lower()

    if any(k in text for k in ["naval", "navy", "maritime", "frigate", "warship", "submarine", "coast guard", "ezhimala", "fleet"]):
        return "https://images.unsplash.com/photo-1544620347-c4fd4a3d5957?auto=format&fit=crop&w=800&q=80"
    if any(k in text for k in ["missile", "defence", "drdo", "army", "air force", "weapon", "radar", "artillery"]):
        return "https://images.unsplash.com/photo-1579783902614-a3fb3927b675?auto=format&fit=crop&w=800&q=80"
    if any(k in text for k in ["island", "iwo jima", "red sea", "bab-el-mandeb", "strait", "ocean", "sea", "port", "shipping"]):
        return "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80"
    if any(k in text for k in ["parliament", "mavalankar", "constitution", "speaker", "lok sabha", "rajya sabha", "election", "commission", "nhrc", "court", "judge"]):
        return "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=800&q=80"
    if any(k in text for k in ["tiger", "elephant", "leopard", "wildlife", "animal", "sanctuary", "national park", "forest", "species", "biodiversity"]):
        return "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?auto=format&fit=crop&w=800&q=80"
    if any(k in text for k in ["tuna", "fish", "marine", "iccat", "ocean", "aquatic", "dolphin", "turtle"]):
        return "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80"
    if any(k in text for k in ["space", "isro", "rocket", "satellite", "gaganyaan", "nasa", "moon", "lunar", "orbit"]):
        return "https://images.unsplash.com/photo-1541185933-ef5d8ed016c2?auto=format&fit=crop&w=800&q=80"
    if any(k in text for k in ["health", "hospital", "patient", "disease", "nimhans", "tb", "tuberculosis", "medical", "doctor"]):
        return "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=800&q=80"
    if any(k in text for k in ["trade", "export", "import", "economy", "gdp", "market access", "usd", "tax", "gst", "cbic", "finance", "rbi"]):
        return "https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&w=800&q=80"
    if any(k in text for k in ["karnataka", "chikkamagaluru", "bengaluru", "mullayanagiri", "western ghats", "kea"]):
        return "https://images.unsplash.com/photo-1596176530529-78163a4f7af2?auto=format&fit=crop&w=800&q=80"
    if any(k in text for k in ["slavery", "social justice", "women", "girl", "child", "welfare", "empowerment", "ambedkar"]):
        return "https://images.unsplash.com/photo-1532629345422-7515f3d16bb6?auto=format&fit=crop&w=800&q=80"

    return "https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=800&q=80"


SPECIES_IN_NEWS = [
    {
        "name": "Bengal Tiger (Panthera tigris)",
        "scientific_name": "Panthera tigris tigris",
        "image_url": "https://images.unsplash.com/photo-1561731216-c3a4d99437d5?auto=format&fit=crop&w=800&q=80",
        "iucn_status": "Endangered",
        "iucn_badge_color": "#dc2626",
        "wpa_schedule": "Schedule I (Highest Protection)",
        "cites": "Appendix I",
        "habitat": "Tropical rainforests, evergreen forests, and mangrove swamps. Key Reserves: Bandipur & Nagarahole (Karnataka), Corbett (Uttarakhand), Sundarbans (West Bengal).",
        "why_in_news": "Completion of 50+ years of Project Tiger, NTCA corridor surveillance, and human-wildlife conflict resolution frameworks in Karnataka Western Ghats."
    },
    {
        "name": "Asian Elephant (Elephas maximus)",
        "scientific_name": "Elephas maximus indicus",
        "image_url": "https://images.unsplash.com/photo-1557050543-4d5f4e07ef46?auto=format&fit=crop&w=800&q=80",
        "iucn_status": "Endangered",
        "iucn_badge_color": "#dc2626",
        "wpa_schedule": "Schedule I",
        "cites": "Appendix I",
        "habitat": "Dry and moist deciduous forests, grasslands. India hosts ~60% of wild Asian elephants. Karnataka has the highest elephant population in India.",
        "why_in_news": "Ministry of Environment notification of interstate elephant corridors across Karnataka, Tamil Nadu, and Kerala; Gaja Utsav celebrations."
    },
    {
        "name": "Snow Leopard (Panthera uncia)",
        "scientific_name": "Panthera uncia",
        "image_url": "https://images.unsplash.com/photo-1548767797-d8c844163c4c?auto=format&fit=crop&w=800&q=80",
        "iucn_status": "Vulnerable",
        "iucn_badge_color": "#ea580c",
        "wpa_schedule": "Schedule I",
        "cites": "Appendix I",
        "habitat": "Alpine and subalpine zones in Ladakh, Himachal Pradesh, Uttarakhand, Sikkim, and Arunachal Pradesh. Key Reserve: Hemis National Park (Ladakh).",
        "why_in_news": "First-ever Snow Leopard Population Assessment in India (SPAI) conducted by Wildlife Institute of India (WII), reporting 718 individuals."
    },
    {
        "name": "Olive Ridley Sea Turtle (Lepidochelys olivacea)",
        "scientific_name": "Lepidochelys olivacea",
        "image_url": "https://images.unsplash.com/photo-1518467166778-b88f373ffec7?auto=format&fit=crop&w=800&q=80",
        "iucn_status": "Vulnerable",
        "iucn_badge_color": "#ea580c",
        "wpa_schedule": "Schedule I",
        "cites": "Appendix I",
        "habitat": "Warm waters of the Pacific, Atlantic, and Indian Oceans. Mass nesting (Arribada) at Gahirmatha Marine Sanctuary and Rushikulya river mouth in Odisha.",
        "why_in_news": "Coast Guard initiates 'Operation Olivia' to safeguard annual mass nesting along the Odisha and Andhra Pradesh coastlines."
    },
    {
        "name": "Great Indian Bustard (Ardeotis nigriceps)",
        "scientific_name": "Ardeotis nigriceps",
        "image_url": "https://images.unsplash.com/photo-1575550959106-5a7defe28b56?auto=format&fit=crop&w=800&q=80",
        "iucn_status": "Critically Endangered",
        "iucn_badge_color": "#991b1b",
        "wpa_schedule": "Schedule I",
        "cites": "Appendix I",
        "habitat": "Dry grasslands and scrublands of Rajasthan and Gujarat. Desert National Park (Jaisalmer). Flagship grassland species.",
        "why_in_news": "Supreme Court appointed expert committee on undergrounding overhead high-voltage power transmission cables to prevent fatal bird collisions."
    },
    {
        "name": "Ganges River Dolphin (Platanista gangetica)",
        "scientific_name": "Platanista gangetica",
        "image_url": "https://images.unsplash.com/photo-1570481662006-a3a1374699e8?auto=format&fit=crop&w=800&q=80",
        "iucn_status": "Endangered",
        "iucn_badge_color": "#dc2626",
        "wpa_schedule": "Schedule I",
        "cites": "Appendix I",
        "habitat": "Freshwater river systems of Ganga, Brahmaputra, and Meghna rivers in India, Nepal, and Bangladesh. Key Sanctuary: Vikramshila Dolphin Sanctuary, Bihar.",
        "why_in_news": "Project Dolphin launched under Wildlife Institute of India to deploy acoustic monitoring and protect India's National Aquatic Animal."
    }
]

PLACES_IN_NEWS = [
    {
        "name": "Bab-el-Mandeb & Red Sea",
        "lat": 12.58,
        "lon": 43.33,
        "region": "Middle East / Horn of Africa",
        "importance": "Crucial maritime choke point connecting the Red Sea to the Gulf of Aden and the Indian Ocean. Security of commercial shipping lanes against maritime threats.",
        "upsc_kea_facts": "Bordered by Yemen (Arabian Peninsula) and Djibouti & Eritrea (East Africa). Handles ~12% of total global seaborne trade."
    },
    {
        "name": "Strait of Hormuz",
        "lat": 26.56,
        "lon": 56.25,
        "region": "Persian Gulf",
        "importance": "World's most critical crude oil transit choke point connecting the Persian Gulf to the Gulf of Oman and Arabian Sea.",
        "upsc_kea_facts": "Bordered by Iran to the north and Oman / UAE to the south. Roughly 21 million barrels of crude oil pass through daily."
    },
    {
        "name": "Prayagraj (Triveni Sangam)",
        "lat": 25.43,
        "lon": 81.84,
        "region": "Uttar Pradesh, India",
        "importance": "Holy confluence of sacred rivers Ganga, Yamuna, and the subterranean Saraswati. Host to the grand Maha Kumbh 2026.",
        "upsc_kea_facts": "Historic city formerly known as Allahabad. Home to the Ashokan Pillar with inscriptions by Samudragupta (Prayag Prashasti by Harishena)."
    },
    {
        "name": "Indian Naval Academy, Ezhimala",
        "lat": 12.01,
        "lon": 75.21,
        "region": "Kannur District, Kerala",
        "importance": "Premier initial officer training establishment of the Indian Navy and Coast Guard. President Droupadi Murmu reviewed the Autumn Term Passing Out Parade.",
        "upsc_kea_facts": "Overlooks the Arabian Sea and Mount Deli. Historic capital of the ancient Mooshika dynasty."
    },
    {
        "name": "NIMHANS & Bengaluru",
        "lat": 12.93,
        "lon": 77.59,
        "region": "Karnataka, India",
        "importance": "National Institute of Mental Health and Neurosciences (NIMHANS) inaugurated advanced spectral CT brain health facility.",
        "upsc_kea_facts": "Designated as an Institute of National Importance by an Act of Parliament (2012). Leader in India's National Tele-Mental Health Programme (Tele-MANAS)."
    },
    {
        "name": "Chikkamagaluru & Western Ghats",
        "lat": 13.31,
        "lon": 75.77,
        "region": "Karnataka, India",
        "importance": "Coffee heartland of India; birthplace of Indian coffee at Baba Budan Giri. Key biodiversity hotspot along the Western Ghats.",
        "upsc_kea_facts": "Mullayanagiri, located in Chikkamagaluru, is the highest peak in Karnataka (1,930 m). High relevance for KEA Geography and Karnataka State Affairs."
    },
    {
        "name": "Vaishali",
        "lat": 25.98,
        "lon": 85.12,
        "region": "Bihar, India",
        "importance": "PM inaugurated major railway and infrastructure projects. Ancient capital of the Licchavis, recognized as one of the world's earliest republics.",
        "upsc_kea_facts": "Venue of the Second Buddhist Council (383 BCE). Associated with Lord Mahavira's birthplace and Lord Buddha's last sermon."
    }
]

DAILY_QUIZ_QUESTIONS = [
    {
        "id": 1,
        "question": "With reference to the National Human Rights Commission (NHRC) of India, consider the following statements:\n1. It is a constitutional body established under Article 338 of the Indian Constitution.\n2. The Chairperson of the NHRC must be a retired Chief Justice of India or a Judge of the Supreme Court.\n3. The recommendations made by the Commission are binding upon the central and state governments.",
        "options": [
            "A) 1 and 2 only",
            "B) 2 only",
            "C) 2 and 3 only",
            "D) 1, 2 and 3"
        ],
        "correct_index": 1,
        "explanation": "Statement 1 is incorrect: NHRC is a STATUTORY body established under the Protection of Human Rights Act (PHRA), 1993, not a constitutional body.\nStatement 2 is correct: Under the 2019 amendment, a person who has been Chief Justice of India OR a Judge of the Supreme Court can be appointed as Chairperson.\nStatement 3 is incorrect: The recommendations of the NHRC are advisory/recommendatory in nature, not legally binding."
    },
    {
        "id": 2,
        "question": "The Bab-el-Mandeb Strait, frequently mentioned in international news regarding maritime commercial transit, connects which two water bodies?",
        "options": [
            "A) Persian Gulf and Gulf of Oman",
            "B) Red Sea and Gulf of Aden",
            "C) Mediterranean Sea and Black Sea",
            "D) Java Sea and Indian Ocean"
        ],
        "correct_index": 1,
        "explanation": "The Bab-el-Mandeb Strait connects the Red Sea (to the north-west) to the Gulf of Aden and the Indian Ocean (to the south-east). It is bordered by Yemen in the Arabian Peninsula and Djibouti and Eritrea in East Africa."
    },
    {
        "id": 3,
        "question": "Regarding the Indian Ocean Rim Association (IORA), which of the following statements is/are correct?\n1. It was established in 1997 based on the vision of Nelson Mandela.\n2. Its Coordinating Secretariat is permanently based in New Delhi, India.\n3. Pakistan and China are full member states of IORA.",
        "options": [
            "A) 1 only",
            "B) 1 and 2 only",
            "C) 2 and 3 only",
            "D) 1, 2 and 3"
        ],
        "correct_index": 0,
        "explanation": "Statement 1 is correct: IORA was established in March 1997 following a keynote address by Nelson Mandela in 1995 advocating for an Indian Ocean regional cooperation rim.\nStatement 2 is incorrect: The IORA Secretariat is located in Ebene, Mauritius (not New Delhi).\nStatement 3 is incorrect: Pakistan is not a member of IORA. China is a Dialogue Partner, not a full member state."
    },
    {
        "id": 4,
        "question": "In the context of Karnataka State Current Affairs (KEA Exam), Mullayanagiri peak is located in which district?",
        "options": [
            "A) Kodagu",
            "B) Chikkamagaluru",
            "C) Shivamogga",
            "D) Hassan"
        ],
        "correct_index": 1,
        "explanation": "Mullayanagiri is the highest peak in Karnataka, standing at an elevation of 1,930 metres (6,330 ft). It is situated in the Chandra Drona / Baba Budan Giri Range of the Western Ghats in Chikkamagaluru district."
    },
    {
        "id": 5,
        "question": "Under the Dr. Ambedkar Medical Aid Scheme implemented by the Dr. Ambedkar Foundation (DAF), what is the maximum financial assistance provided to eligible SC/ST patients?",
        "options": [
            "A) ₹ 1.00 Lakh",
            "B) ₹ 2.50 Lakh",
            "C) ₹ 3.50 Lakh",
            "D) ₹ 5.00 Lakh"
        ],
        "correct_index": 2,
        "explanation": "Under the revised guidelines of the Dr. Ambedkar Medical Aid Scheme administered by the Dr. Ambedkar Foundation (Ministry of Social Justice and Empowerment), financial assistance of up to ₹ 3.50 Lakh is provided to SC and ST patients suffering from serious life-threatening diseases requiring surgery/specialized treatment."
    }
]
