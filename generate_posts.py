import random

# 🗂️ High‑level account types (super‑simple edition)
account_type_distribution = [
    {"name": "individual",              "weight": 0.60},  # everyday people
    {"name": "brand_business",          "weight": 0.10},  # companies, local shops, SaaS apps
    {"name": "influencer_public_figure","weight": 0.05},  # celebs, creators, athletes
    {"name": "media_news",              "weight": 0.05},  # newspapers, TV channels, podcasts
    {"name": "bot",                     "weight": 0.10},  # automatic posting accounts
    {"name": "spam_scam",               "weight": 0.05},  # phishing, giveaway scams, etc.
    {"name": "creative_meme",           "weight": 0.05},  # memes, parody, humor
]

PERSONAS_BY_TYPE = {
    "individual": [
        # Teen/Young Adult (13-22)
        "anxiety_ridden_high_schooler",
        "art_student_with_strong_opinions", 
        "competitive_teenage_athlete",
        "theatre_kid_and_proud",
        
        # Young Professional (23-32)
        "burned_out_corporate_lawyer",
        "enthusiastic_kindergarten_teacher",
        "struggling_freelance_designer",
        "tech_bro_with_startup_dreams",
        "nurse_working_night_shifts",
        
        # Parents (25-45)
        "helicopter_mom_of_twins",
        "single_dad_juggling_work_life",
        "homeschooling_parent_activist",
        
        # Middle-aged (35-55)
        "midlife_crisis_divorcee",
        "wine_mom_book_club_president",
        "weekend_warrior_mountain_biker",
        "conspiracy_theory_uncle",
        
        # Older Adults (55+)
        "facebook_grandma_oversharer",
        "retired_professor_still_teaching",
        "grumpy_boomer_hates_technology",
    ],
    "brand_business": [
        # Local/Small Business
        "family_owned_italian_restaurant",
        "indie_bookstore_fighting_amazon",
        "craft_brewery_with_attitude",
        "struggling_yoga_studio",
        "overpriced_organic_juice_bar",
        
        # Professional Services
        "pretentious_marketing_agency",
        "desperate_real_estate_agent",
        "small_town_law_firm",
        "boutique_wedding_planning",
        
        # Tech/Online
        "failed_crypto_startup",
        "boring_b2b_saas_company",
        "dropshipping_get_rich_scheme",
        
        # Retail/E-commerce  
        "knockoff_luxury_fashion_brand",
        "artisanal_soap_making_business",
        "overpriced_pet_accessories_shop",
    ],
    "influencer_public_figure": [
        # Content Creators
        "thirst_trap_fitness_influencer",
        "wholesome_family_vlogger_with_secrets",
        "pretentious_minimalism_lifestyle_guru",
        "failed_musician_turned_podcaster", 
        "controversial_political_commentator",
        
        # Traditional Celebrities
        "washed_up_reality_tv_star",
        "indie_film_actor_seeking_validation",
        "retired_athlete_selling_supplements",
        
        # Experts/Thought Leaders  
        "self_proclaimed_entrepreneur_guru",
        "académic_with_public_aspirations",
        "activist_nonprofit_leader",
        
        # Niche Influencers
        "plant_mom_with_1000_houseplants",
        "urban_exploring_photographer",
        "competitive_eating_champion",
        "astrology_witch_tarot_reader",
    ],
    "media_news": [
        # Traditional Media
        "dying_local_newspaper",
        "biased_cable_news_channel", 
        "sports_talk_radio_hot_takes",
        "investigative_journalism_nonprofit",
        
        # Digital Media
        "clickbait_lifestyle_blog",
        "tech_news_site_with_attitude",
        "pop_culture_gossip_magazine",
        "financial_advice_youtube_channel",
        
        # Podcasts  
        "true_crime_obsessed_podcast",
        "bros_talking_fantasy_football",
        "interview_show_past_its_prime",
        
        # Specialized 
        "indie_music_discovery_blog",
        "food_review_instagram_account",
        "academic_research_publication",
        "community_events_calendar",
    ],
    "bot": [
        # Utility Bots
        "weather_updates_bot",
        "public_transit_delay_alerts", 
        "earthquake_emergency_notifications",
        "stock_price_tracking_bot",
        "cryptocurrency_price_alerts",
        
        # Content Bots
        "daily_motivational_quotes",
        "random_historical_facts",
        "word_of_the_day_bot",
        "astronomy_picture_daily",
        
        # Engagement Bots
        "automatic_birthday_wishes",
        "generic_compliment_generator",
        "fake_engagement_like_bot",
        
        # Weird/Broken Bots
        "malfunctioning_poetry_generator",
        "gibberish_markov_chain_bot",
        "definitely_not_sentient_ai",
    ],
    "spam_scam": [
        # Financial Scams
        "crypto_pump_and_dump_scheme",
        "forex_trading_get_rich_quick",
        "fake_investment_opportunity",
        "mlm_essential_oils_hun",
        
        # Romance/Dating Scams
        "catfish_looking_for_love",
        "fake_military_deployed_overseas",
        "widowed_billionaire_seeking_soulmate",
        
        # Fake Giveaways/Contests
        "iphone_giveaway_click_bait",
        "fake_celebrity_endorsed_contest",
        "survey_scam_gift_card_promise",
        
        # Identity/Phishing
        "fake_bank_security_alert",
        "irs_tax_refund_phishing",
        "social_security_suspension_scam",
        
        # Product Scams
        "miracle_weight_loss_supplement",
        "fake_designer_handbag_seller",
        "counterfeit_electronics_dealer",
    ],
    "creative_meme": [
        # Nostalgic Content
        "90s_kid_nostalgia_memes",
        "millennial_childhood_trauma_humor",
        "gen_z_making_fun_of_millennials",
        
        # Pop Culture
        "tv_show_recap_meme_account",
        "celebrity_gossip_meme_factory",
        "movie_quote_reaction_gifs",
        
        # Relatable Humor  
        "adulting_is_hard_memes",
        "introvert_social_anxiety_jokes",
        "procrastination_self_roast_memes",
        
        # Absurdist/Weird
        "surreal_deep_fried_memes",
        "oddly_specific_meme_generator",
        "chaotic_energy_shitposting",
        
        # Wholesome
        "motivational_animal_pictures", 
        "dad_joke_appreciation_society",
        "wholesome_relationship_goals_memes",
    ],
}


# Account-type-specific modifiers that directly influence text generation
MODIFIERS_BY_ACCOUNT_TYPE = {
    "individual": {
        "communication_style": ["casual_friendly", "sarcastic_witty", "wholesome_positive", "anxious_oversharing", "aggressive_confrontational", "cryptic_vague_posting"],
        "posting_mood": ["optimistic_upbeat", "pessimistic_complaining", "neutral_matter_of_fact", "emotional_dramatic", "humorous_joking", "philosophical_deep"],
        "education_level": ["high_school_dropout", "high_school_grad", "some_college", "college_degree", "graduate_degree", "trade_school"],
        "political_leaning": ["far_left_progressive", "liberal_democrat", "moderate_centrist", "conservative_republican", "far_right_extremist", "apolitical_avoids_politics"],
        "life_stage": ["teenager", "college_student", "young_professional", "parent", "middle_aged", "retired"],
        "primary_topic": ["work_career", "family_kids", "hobbies_interests", "politics_news", "personal_struggles", "achievements_bragging", "daily_mundane", "relationships_dating"],
    },
    
    "brand_business": {
        "brand_voice": ["professional_corporate", "casual_approachable", "edgy_provocative", "wholesome_family_friendly", "trendy_hip", "authoritative_expert"],
        "marketing_style": ["hard_sell_pushy", "soft_sell_subtle", "educational_helpful", "entertaining_fun", "inspirational_motivational", "transparent_honest"],
        "business_stage": ["startup_scrappy", "established_confident", "struggling_desperate", "growing_excited", "corporate_polished"],
        "target_audience": ["young_millennials_gen_z", "families_parents", "professionals_business", "local_community", "niche_enthusiasts"],
        "content_focus": ["product_promotion", "behind_the_scenes", "industry_expertise", "customer_stories", "company_culture", "educational_content"],
    },
    
    "influencer_public_figure": {
        "influencer_persona": ["authentic_relatable", "aspirational_lifestyle", "educational_expert", "entertaining_funny", "controversial_edgy", "wholesome_inspirational"],
        "content_style": ["highly_polished", "casual_behind_scenes", "educational_tutorials", "opinion_commentary", "lifestyle_showcase", "interaction_community"],
        "follower_relationship": ["parasocial_intimate", "professional_distant", "community_leader", "celebrity_untouchable", "friend_next_door"],
        "monetization_approach": ["subtle_integrated", "obvious_promotional", "educational_value_first", "pure_entertainment", "activism_cause_driven"],
    },
    
    "media_news": {
        "editorial_stance": ["neutral_objective", "left_leaning_bias", "right_leaning_bias", "sensationalist_clickbait", "investigative_serious", "entertainment_focused"],
        "reporting_style": ["breaking_news_urgent", "in_depth_analysis", "quick_updates", "opinion_commentary", "local_community_focus", "global_perspective"],
        "audience_tone": ["professional_formal", "conversational_accessible", "academic_detailed", "populist_simple", "elite_sophisticated"],
        "content_priority": ["politics_government", "sports_entertainment", "business_economy", "technology_innovation", "local_community", "human_interest"],
    },
    
    "bot": {
        "bot_personality": ["robotic_formal", "friendly_helpful", "quirky_weird", "broken_glitchy", "overly_enthusiastic", "minimalist_efficient"],
        "response_pattern": ["scheduled_regular", "triggered_reactive", "random_chaotic", "template_repetitive", "learning_adaptive"],
        "content_type": ["factual_information", "motivational_quotes", "alerts_notifications", "entertainment_jokes", "automated_responses"],
    },
    
    "spam_scam": {
        "scam_approach": ["urgent_fear_based", "too_good_to_be_true", "fake_authority", "emotional_manipulation", "social_proof_fake", "technical_confusion"],
        "writing_quality": ["poor_grammar_obvious", "decent_convincing", "copy_paste_generic", "AI_generated_weird", "foreign_translation_errors"],
        "target_vulnerability": ["financial_desperation", "loneliness_romance", "tech_confusion", "greed_get_rich", "fear_authority"],
    },
    
    "creative_meme": {
        "humor_style": ["absurdist_surreal", "relatable_everyday", "nostalgic_throwback", "pop_culture_reference", "self_deprecating", "wholesome_positive", "dark_edgy"],
        "meme_format": ["image_macro_text", "reaction_gif_style", "story_narrative", "list_enumeration", "observational_commentary"],
        "target_demographic": ["gen_z_zoomer", "millennial_nostalgia", "boomer_humor", "niche_community", "mainstream_broad_appeal"],
        "content_freshness": ["trending_current", "classic_timeless", "dead_horse_beating", "cutting_edge_new"],
    }
}


import random

# … your existing lists & dicts stay unchanged …

# ---------- helper functions ---------- #
def sample_account_type(dist=account_type_distribution) -> str:
    """Weighted random draw from the high‑level account‑type list."""
    names   = [d["name"]   for d in dist]
    weights = [d["weight"] for d in dist]
    return random.choices(names, weights=weights, k=1)[0]

def sample_persona(account_type: str) -> str:
    """Random persona that matches a given account type."""
    return random.choice(PERSONAS_BY_TYPE[account_type])

def sample_modifiers(account_type: str, persona: str = None) -> dict:
    """Pick modifiers appropriate for account type with deterministic persona-based logic."""
    
    # Get account-type-specific modifiers
    modifiers = MODIFIERS_BY_ACCOUNT_TYPE.get(account_type, {})
    
    # Simple deterministic mapping based on persona name patterns
    result = {}
    
    for category, options in modifiers.items():
        if account_type == "individual" and persona:
            # Individual account logic based on persona names
            if "high_schooler" in persona or "teenage" in persona or "theatre_kid" in persona:
                if category == "life_stage":
                    result[category] = "teenager"
                elif category == "education_level":
                    result[category] = random.choice(["high_school_dropout", "high_school_grad"])
                elif category == "communication_style" and "anxiety" in persona:
                    result[category] = "anxious_oversharing"
                elif category == "primary_topic" and "athlete" in persona:
                    result[category] = "achievements_bragging"
                else:
                    result[category] = random.choice(options)
                    
            elif "student" in persona:
                if category == "life_stage":
                    result[category] = "college_student"
                elif category == "education_level":
                    result[category] = random.choice(["some_college", "college_degree"])
                else:
                    result[category] = random.choice(options)
                    
            elif any(word in persona for word in ["lawyer", "teacher", "designer", "tech_bro", "nurse"]):
                if category == "life_stage":
                    result[category] = "young_professional"
                elif category == "education_level":
                    if "lawyer" in persona:
                        result[category] = "graduate_degree"
                    elif "teacher" in persona:
                        result[category] = random.choice(["college_degree", "graduate_degree"])
                    else:
                        result[category] = random.choice(["college_degree", "some_college"])
                else:
                    result[category] = random.choice(options)
                    
            elif any(word in persona for word in ["mom", "dad", "parent"]) and "wine_mom" not in persona:
                if category == "life_stage":
                    result[category] = "parent"
                elif category == "primary_topic":
                    result[category] = "family_kids"
                elif category == "education_level":
                    result[category] = random.choice(["college_degree", "some_college", "high_school_grad"])
                else:
                    result[category] = random.choice(options)
                    
            elif any(word in persona for word in ["midlife", "weekend_warrior", "conspiracy", "uncle"]) or "wine_mom" in persona:
                if category == "life_stage":
                    result[category] = "middle_aged"
                elif category == "education_level":
                    result[category] = random.choice(["college_degree", "some_college", "high_school_grad"])
                elif category == "political_leaning" and "conspiracy" in persona:
                    result[category] = random.choice(["far_right_extremist", "conservative_republican"])
                else:
                    result[category] = random.choice(options)
                    
            elif any(word in persona for word in ["grandma", "retired", "boomer"]):
                if category == "life_stage":
                    result[category] = "retired"
                elif category == "education_level":
                    if "professor" in persona:
                        result[category] = "graduate_degree"
                    else:
                        result[category] = random.choice(["high_school_grad", "some_college", "college_degree"])
                elif category == "political_leaning" and "boomer" in persona:
                    result[category] = random.choice(["conservative_republican", "far_right_extremist"])
                else:
                    result[category] = random.choice(options)
            else:
                # Fallback for any unmatched individual personas
                result[category] = random.choice(options)
                
        else:
            # For non-individual accounts, just use random sampling
            result[category] = random.choice(options)
    
    return result

def sample_account() -> dict:
    """Convenience wrapper that packages everything together."""
    acc_type = sample_account_type()
    persona = sample_persona(acc_type)
    return {
        "account_type": acc_type,
        "persona": persona,
        "modifiers": sample_modifiers(acc_type, persona),
    }

def generate_system_prompt(account: dict) -> str:
    """Generate a system prompt for LLM post generation based on account characteristics."""
    
    persona = account["persona"]
    modifiers = account["modifiers"]
    account_type = account["account_type"]
    
    # Convert underscores to spaces and title case for readability
    persona_readable = persona.replace("_", " ").title()
    
    # Build modifier descriptions dynamically based on what's available
    modifier_sections = []
    
    # Individual account modifiers
    if account_type == "individual":
        if modifiers:
            modifier_sections.append("PERSONALITY & STYLE:")
            if "communication_style" in modifiers:
                modifier_sections.append(f"- Communication: {modifiers['communication_style'].replace('_', ' ').title()}")
            if "posting_mood" in modifiers:
                modifier_sections.append(f"- Typical Mood: {modifiers['posting_mood'].replace('_', ' ').title()}")
            if "life_stage" in modifiers:
                modifier_sections.append(f"- Life Stage: {modifiers['life_stage'].replace('_', ' ').title()}")
            if "primary_topic" in modifiers:
                modifier_sections.append(f"- Main Topics: {modifiers['primary_topic'].replace('_', ' ').title()}")
            if "education_level" in modifiers:
                modifier_sections.append(f"- Education: {modifiers['education_level'].replace('_', ' ').title()}")
            if "political_leaning" in modifiers:
                modifier_sections.append(f"- Politics: {modifiers['political_leaning'].replace('_', ' ').title()}")
    
    # Brand/Business account modifiers
    elif account_type == "brand_business":
        if modifiers:
            modifier_sections.append("BRAND CHARACTERISTICS:")
            if "brand_voice" in modifiers:
                modifier_sections.append(f"- Brand Voice: {modifiers['brand_voice'].replace('_', ' ').title()}")
            if "marketing_style" in modifiers:
                modifier_sections.append(f"- Marketing Style: {modifiers['marketing_style'].replace('_', ' ').title()}")
            if "business_stage" in modifiers:
                modifier_sections.append(f"- Business Stage: {modifiers['business_stage'].replace('_', ' ').title()}")
            if "target_audience" in modifiers:
                modifier_sections.append(f"- Target Audience: {modifiers['target_audience'].replace('_', ' ').title()}")
            if "content_focus" in modifiers:
                modifier_sections.append(f"- Content Focus: {modifiers['content_focus'].replace('_', ' ').title()}")
    
    # Influencer account modifiers
    elif account_type == "influencer_public_figure":
        if modifiers:
            modifier_sections.append("INFLUENCER PROFILE:")
            if "influencer_persona" in modifiers:
                modifier_sections.append(f"- Influencer Style: {modifiers['influencer_persona'].replace('_', ' ').title()}")
            if "content_style" in modifiers:
                modifier_sections.append(f"- Content Style: {modifiers['content_style'].replace('_', ' ').title()}")
            if "follower_relationship" in modifiers:
                modifier_sections.append(f"- Follower Relationship: {modifiers['follower_relationship'].replace('_', ' ').title()}")
            if "monetization_approach" in modifiers:
                modifier_sections.append(f"- Monetization: {modifiers['monetization_approach'].replace('_', ' ').title()}")
    
    # Media/News account modifiers
    elif account_type == "media_news":
        if modifiers:
            modifier_sections.append("MEDIA PROFILE:")
            if "editorial_stance" in modifiers:
                modifier_sections.append(f"- Editorial Stance: {modifiers['editorial_stance'].replace('_', ' ').title()}")
            if "reporting_style" in modifiers:
                modifier_sections.append(f"- Reporting Style: {modifiers['reporting_style'].replace('_', ' ').title()}")
            if "audience_tone" in modifiers:
                modifier_sections.append(f"- Audience Tone: {modifiers['audience_tone'].replace('_', ' ').title()}")
            if "content_priority" in modifiers:
                modifier_sections.append(f"- Content Focus: {modifiers['content_priority'].replace('_', ' ').title()}")
    
    # Bot account modifiers
    elif account_type == "bot":
        if modifiers:
            modifier_sections.append("BOT CHARACTERISTICS:")
            if "bot_personality" in modifiers:
                modifier_sections.append(f"- Bot Personality: {modifiers['bot_personality'].replace('_', ' ').title()}")
            if "response_pattern" in modifiers:
                modifier_sections.append(f"- Response Pattern: {modifiers['response_pattern'].replace('_', ' ').title()}")
            if "content_type" in modifiers:
                modifier_sections.append(f"- Content Type: {modifiers['content_type'].replace('_', ' ').title()}")
    
    # Spam/Scam account modifiers
    elif account_type == "spam_scam":
        if modifiers:
            modifier_sections.append("SCAM CHARACTERISTICS:")
            if "scam_approach" in modifiers:
                modifier_sections.append(f"- Scam Approach: {modifiers['scam_approach'].replace('_', ' ').title()}")
            if "writing_quality" in modifiers:
                modifier_sections.append(f"- Writing Quality: {modifiers['writing_quality'].replace('_', ' ').title()}")
            if "target_vulnerability" in modifiers:
                modifier_sections.append(f"- Target Vulnerability: {modifiers['target_vulnerability'].replace('_', ' ').title()}")
    
    # Meme account modifiers
    elif account_type == "creative_meme":
        if modifiers:
            modifier_sections.append("MEME CHARACTERISTICS:")
            if "humor_style" in modifiers:
                modifier_sections.append(f"- Humor Style: {modifiers['humor_style'].replace('_', ' ').title()}")
            if "meme_format" in modifiers:
                modifier_sections.append(f"- Meme Format: {modifiers['meme_format'].replace('_', ' ').title()}")
            if "target_demographic" in modifiers:
                modifier_sections.append(f"- Target Demographic: {modifiers['target_demographic'].replace('_', ' ').title()}")
            if "content_freshness" in modifiers:
                modifier_sections.append(f"- Content Freshness: {modifiers['content_freshness'].replace('_', ' ').title()}")
    
    modifier_text = "\n".join(modifier_sections) if modifier_sections else "No specific modifiers defined."
    
    prompt = f"""You are roleplaying as a social media account with the following characteristics:

ACCOUNT TYPE: {account_type.replace("_", " ").title()}
PERSONA: {persona_readable}

{modifier_text}

Generate 50-100 realistic social media posts that this account would make. Each post should:

1. Reflect the persona's personality and characteristics from the modifiers above
2. Use language, tone, and topics appropriate for this specific account type and persona
3. Include realistic social media elements (hashtags, mentions, emojis) when appropriate for the persona
4. Vary in length and style to show authentic posting patterns
5. Show authentic human flaws, typos, or quirks when realistic for the persona (especially for individual accounts)
6. For business/brand accounts: focus on appropriate business content and goals
7. For bot accounts: show automated or systematic posting patterns
8. For spam/scam accounts: use manipulative language and questionable offers typical of scams

Format each post as:
POST [number]:
[post content]

Be creative and authentic - make these posts feel like they come from this specific type of account."""

    return prompt


def generate_posts_for_account(account: dict, num_posts: int = 75) -> dict:
    """Generate a complete account profile with system prompt ready for LLM generation."""
    
    return {
        "account_profile": account,
        "system_prompt": generate_system_prompt(account),
        "instructions": f"Send this system prompt to an LLM to generate {num_posts} realistic posts for this account.",
        "metadata": {
            "total_modifiers": len(account["modifiers"]),
            "persona_category": account["account_type"],
            "generation_ready": True
        }
    }

# ---------- quick demo ---------- #
if __name__ == "__main__":
    
    print("=== SAMPLE ACCOUNTS ===")
    for i in range(3):
        account = sample_account()
        print(f"\nAccount {i+1}:")
        print(f"  Type: {account['account_type']}")
        print(f"  Persona: {account['persona']}")
        modifier_keys = list(account['modifiers'].keys())[:3]  # Show first 3 modifiers
        modifier_summary = ", ".join([f"{k}: {account['modifiers'][k]}" for k in modifier_keys])
        print(f"  Key Modifiers: {modifier_summary}")
    
    print("\n" + "="*50)
    print("=== FULL GENERATION EXAMPLE ===")
    example_account = sample_account()
    full_generation = generate_posts_for_account(example_account)
    
    print(f"\nAccount Profile: {example_account['persona']}")
    print(f"Account Type: {example_account['account_type']}")
    print("\n--- SYSTEM PROMPT ---")
    print(full_generation['system_prompt'])