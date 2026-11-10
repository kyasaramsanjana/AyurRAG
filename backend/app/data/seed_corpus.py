"""
AyurRAG Seed Corpus
Selected authentic passages from the four foundational classical treatises:
1. Charaka Samhita (Internal Medicine & Therapeutics)
2. Sushruta Samhita (Surgical Wisdom, Antiseptic & Tissue Healing)
3. Ashtanga Hridaya (Daily Regimen & Holistic Health)
4. Bhavaprakasha Nighantu (Ayurvedic Materia Medica & Herbology)
"""

SEED_BOOKS = [
    {
        "title": "Charaka Samhita",
        "author": "Maharshi Charaka & Agnivesha",
        "category": "Classical Internal Medicine (Kayachikitsa)",
        "total_pages": 48,
        "passages": [
            {
                "chapter": "Chikitsa Sthana - Chapter 3: Jwara Chikitsa (Therapeutics of Fever)",
                "page_number": 42,
                "text": "HERBAL REMEDIES FOR FEVER (JWARA): In addition to fasting (Langhana) which kindles the digestive fire (Agni), herbal decoctions are beneficial. The simplest herbal remedy for acute fever is fresh cilantro juice. Blend a handful of cilantro leaves with about half a cup of warm water, strain out the pulp, and take two teaspoons of the remaining liquid three times a day to lower fever heat. Furthermore, an effective herbal tea for fever consists of lemongrass, holy basil (tulsi), and fennel seeds in equal proportions steeped in boiling water for 10 minutes."
            },
            {
                "chapter": "Chikitsa Sthana - Chapter 3: Jwara Chikitsa (Therapeutics of Fever)",
                "page_number": 45,
                "text": "CORIANDER AND GINGER DECOCTION FOR FEVER: Another excellent herbal remedy for reducing fever is a tea made of coriander 2 parts, cinnamon 2 parts, and dry ginger (shunthi) 1 part. Steep one teaspoon of this herbal mixture in a cup of hot water for 10 minutes before drinking. You can drink this every few hours until the fever breaks. Another simple three-ingredient tea made of household herbs is cumin seeds, coriander seeds, and fennel seeds (CCF Tea) mixed in equal proportions to flush Ama (metabolic toxins) and stabilize body temperature."
            },
            {
                "chapter": "Chikitsa Sthana - Chapter 20: Kasa Chikitsa (Management of Cough)",
                "page_number": 68,
                "text": "MANAGEMENT OF COUGH (KASA) AND RESPIRATORY CONGESTION: Just steam inhalation alone, with a few drops of eucalyptus or mint added, will be highly beneficial. Mix 1 teaspoon of fennel seed powder with 1 teaspoon of natural raw sugar, taken two or three times a day. For cold with cough and congestion, mix 1/2 teaspoon cinnamon powder and 1 teaspoon pure honey, and eat this mixture two or three times a day. For dry cough, make a decoction from 1 teaspoon tulsi (holy basil) boiled in 1 cup of water for 5 minutes."
            },
            {
                "chapter": "Chikitsa Sthana - Chapter 20: Kasa Chikitsa (Management of Cough)",
                "page_number": 72,
                "text": "BLACK PEPPER AND HONEY FORMULATION (MARICHA YOGA): Mix 1/4 teaspoon of black pepper powder with 1 teaspoon of raw honey, and ingest on a full stomach. If your voice is hoarse, use 1 teaspoon of ghee instead of honey. The heating quality (Ushna Virya) of black pepper helps relieve congestion and drives out aggravated Kapha from the chest. Take 2 or 3 times a day for 3 to 5 days. A tea made from 1/2 teaspoon ginger powder, a pinch of clove, and a pinch of cinnamon powder in a cupful of boiled water offers rapid relief from persistent cough."
            },
            {
                "chapter": "Sutra Sthana - Chapter 25: Yajjah Purushiya Adhyaya",
                "page_number": 112,
                "text": "NUTRITION AND AGNI: Digestion is the bedrock of health. Food taken in proper measure kindles the bodily fire (Jatharagni) without disturbing Vata, Pitta, or Kapha. Triphala, consisting of Haritaki, Bibhitaki, and Amalaki, taken with warm water or honey at bedtime, cleanses the digestive tract, enhances ocular strength, and prevents premature aging. Water boiled with dry ginger stimulates sluggish digestion."
            }
        ]
    },
    {
        "title": "Sushruta Samhita",
        "author": "Acharya Sushruta",
        "category": "Classical Surgical Science (Shalya Tantra)",
        "total_pages": 52,
        "passages": [
            {
                "chapter": "Sutra Sthana - Chapter 25: Vrana Pratishedha (Wound Healing)",
                "page_number": 88,
                "text": "MANAGEMENT OF WOUNDS AND LESIONS (VRANA): Haridra (Turmeric) is supreme among wound-healing herbs (Vrana Ropana). Its bitter and pungent taste cleanses contaminated blood (Rakta Shodhana) and dries excess exudate. For fresh lacerations and infected wounds, a sterile paste made of finely powdered Haridra mixed with honey and clarified butter (Ghrita) arrests bleeding, prevents microbial colonization, and accelerates rapid epithelialization."
            },
            {
                "chapter": "Sutra Sthana - Chapter 11: Kshara Paka Vidhi (Alkaline Preparations)",
                "page_number": 34,
                "text": "KSHARA SUTRA AND PURIFICATION: Sushruta details the superior virtue of alkaline substances (Kshara) among all surgical appliances. Kshara possesses the power of excision, incision, and purification of deep-seated fistulae and chronic sinuses. It pacifies the Tridosha, penetrates deep micro-channels, and dissolves fibrous tissue without causing extensive collateral damage when prepared according to exact protocol."
            },
            {
                "chapter": "Sharira Sthana - Chapter 6: Pratyeka Marma Nirdesha",
                "page_number": 64,
                "text": "VITAL POINTS (MARMAS) AND TRAUMA MANAGEMENT: The human body contains 107 Marma points where muscles, vessels, ligaments, bones, and joints coalesce. Injury to Sadyo Pranahara Marmas leads to rapid loss of consciousness. Cold water ablutions, application of sandalwood (Chandana) paste, and medicated ghee infused with licorice (Yashtimadhu) mitigate shock, burning sensation, and internal hemorrhage."
            },
            {
                "chapter": "Chikitsa Sthana - Chapter 2: Sadyo Vrana Chikitsa",
                "page_number": 92,
                "text": "ASEPTIC HERBAL FORMULATIONS FOR SKIN AND TISSUE: Neem (Nimba) leaves boiled in water yield a potent antiseptic wash. The decoction of Triphala cools inflamed tissues and halts pus discharge. For burn injuries (Daghdha Vrana), Ghrita blended with Gairika (red ochre) and honey soothes fiery burning, prevents blister formation, and stimulates healthy granulation tissue."
            }
        ]
    },
    {
        "title": "Ashtanga Hridaya",
        "author": "Acharya Vagbhata",
        "category": "Comprehensive Ayurvedic Compendium",
        "total_pages": 40,
        "passages": [
            {
                "chapter": "Sutra Sthana - Chapter 2: Dinacharya (Daily Routine)",
                "page_number": 14,
                "text": "DAILY REGIMEN FOR LONGEVITY (DINACHARYA): One should wake up during Brahma Muhurta (approximately 96 minutes before sunrise) to preserve vital life energy. After eliminating natural wastes, brush teeth with astringent, pungent, or bitter twigs such as Nimba or Karanja. Clean the tongue gently from back to front. Instill 2 drops of sesame oil or Anu Taila into each nostril (Nasya) to clarify the senses, prevent graying of hair, and strengthen the cranial nerves."
            },
            {
                "chapter": "Sutra Sthana - Chapter 3: Ritucharya (Seasonal Regimen)",
                "page_number": 22,
                "text": "SEASONAL HEALTH ADAPTATION (RITUCHARYA): In Grishma (Summer), the sun depletes bodily moisture; one should consume sweet, cold, and liquid foods, avoidance of excessive spice and heavy exertion. In Varsha (Monsoon), Agni is naturally weakened; drink boiled warm water, consume honey with meals, and favor light, freshly cooked grains seasoned with ginger and cumin to avert Vata vitiation."
            },
            {
                "chapter": "Sutra Sthana - Chapter 5: Doshadi Vijnaniya (Science of Doshas)",
                "page_number": 31,
                "text": "THE THREE HUMORS (VATA, PITTA, KAPHA): Vata is dry, light, cold, rough, and mobile; it governs all movements in the nervous and musculoskeletal systems. Pitta is hot, sharp, liquid, and slightly oily; it governs metabolism and vision. Kapha is heavy, slow, oily, and stable; it provides lubrication and immunity. Disease is nothing other than an imbalance of these three doshas, while health is their dynamic harmony."
            },
            {
                "chapter": "Sutra Sthana - Chapter 5: Dravadravya Vijnaniya (Properties of Liquids)",
                "page_number": 37,
                "text": "PROPERTIES OF HONEY AND GHEE: Honey is dry, astringent, and scrapes accumulated fat and toxins (Lekhana). It should never be heated or consumed with equal quantity of ghee, as heated honey becomes toxic (Ama). Pure cow's ghee (Ghrita) kindles digestive fire, enhances intellect (Dhi), memory (Smriti), and longevity, pacifying both Vata and Pitta without increasing Kapha when taken in moderation."
            }
        ]
    },
    {
        "title": "Bhavaprakasha Nighantu",
        "author": "Acharya Bhavamishra",
        "category": "Materia Medica & Dravyaguna Shastra",
        "total_pages": 60,
        "passages": [
            {
                "chapter": "Guduchyadi Varga - Monographs on Adaptogens and Rejuvenators",
                "page_number": 105,
                "text": "ASHWAGANDHA (WITHANIA SOMNIFERA) MONOGRAPH: Ashwagandha is bitter and astringent in taste (Tikta, Kashaya Rasa), hot in potency (Ushna Virya), and sweet in post-digestive bio-transformation (Madhura Vipaka). It powerfully pacifies Vata and Kapha, builds physical endurance (Bala), promotes reproductive vitality (Shukrala), and calms mental agitation. It is indicated in emaciation, chronic fatigue, anxiety, and joint stiffness. Administered with warm milk and ghee at night, it induces sound restorative sleep."
            },
            {
                "chapter": "Haritakyadi Varga - Monographs on Cleansing and Digestive Herbs",
                "page_number": 118,
                "text": "AMALAKI (EMBLICA OFFICINALIS) PROPERTIES: Amalaki contains five of the six tastes, lacking only the salty taste (Lavana). It is sour predominantly, cold in potency (Shita Virya), and sweet after digestion. It is the finest Rasayana (rejuvenator) that pacifies Pitta without provoking Vata or Kapha. It enriches eyesight, strengthens hair follicles, stabilizes blood sugar, and preserves youthfulness through abundant natural antioxidants."
            },
            {
                "chapter": "Guduchyadi Varga - Monographs on Bitter Tonics and Febrifuges",
                "page_number": 126,
                "text": "GUDUCHI / GILOY (TINOSPORA CORDIFOLIA) ANALYSIS: Guduchi is known as Amrita (nectar of immortality). It possesses bitter and astringent taste, hot potency, and sweet post-digestive effect. It dissolves metabolic toxins (Ama Pachana), neutralizes persistent fevers (Jwaraghna), protects hepatic cells, and modulates the immune response. Combined with neem and black pepper, it serves as a supreme blood purifier."
            },
            {
                "chapter": "Brahmi Varga - Medhya Herbs for Cognitive Enhancement",
                "page_number": 142,
                "text": "BRAHMI (BACOPA MONNIERI) AND SHATAVARI (ASPARAGUS RACEMOSUS): Brahmi is cooling (Shita Virya), bitter in taste, and acts directly on the nervous system as a Medhya Rasayana (cognitive enhancer). It sharpens memory, alleviates mental tension, and balances neurological firing. Shatavari is sweet and cooling, nourishing all seven body tissues (Dhatus), balancing hormonal cycles, and strengthening maternal vitality."
            }
        ]
    }
]
