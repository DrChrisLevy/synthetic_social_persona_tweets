"""Tests for persona-modifier mappings to ensure logical consistency."""

import pytest
from generate_posts import (
    sample_modifiers, 
    sample_account, 
    PERSONAS_BY_TYPE, 
    MODIFIERS_BY_ACCOUNT_TYPE
)


class TestPersonaModifierMappings:
    """Test that personas get appropriate modifiers based on their characteristics."""
    
    def test_teen_personas_get_teenager_life_stage(self):
        """Teen personas should always get 'teenager' life stage."""
        teen_personas = [
            "anxiety_ridden_high_schooler",
            "competitive_teenage_athlete", 
            "theatre_kid_and_proud"
        ]
        
        for persona in teen_personas:
            modifiers = sample_modifiers("individual", persona)
            assert modifiers["life_stage"] == "teenager", f"{persona} should have teenager life stage"
            assert modifiers["education_level"] in ["high_school_dropout", "high_school_grad"], f"{persona} should have high school education"
    
    def test_student_personas_get_college_life_stage(self):
        """Student personas should get 'college_student' life stage."""
        student_personas = ["art_student_with_strong_opinions"]
        
        for persona in student_personas:
            modifiers = sample_modifiers("individual", persona)
            assert modifiers["life_stage"] == "college_student", f"{persona} should have college_student life stage"
            assert modifiers["education_level"] in ["some_college", "college_degree"], f"{persona} should have college-level education"
    
    def test_professional_personas_get_young_professional_life_stage(self):
        """Professional personas should get 'young_professional' life stage."""
        professional_personas = [
            "burned_out_corporate_lawyer",
            "enthusiastic_kindergarten_teacher",
            "struggling_freelance_designer", 
            "tech_bro_with_startup_dreams",
            "nurse_working_night_shifts"
        ]
        
        for persona in professional_personas:
            modifiers = sample_modifiers("individual", persona)
            assert modifiers["life_stage"] == "young_professional", f"{persona} should have young_professional life stage"
            
            # Check education levels are appropriate for professionals
            if "lawyer" in persona:
                assert modifiers["education_level"] == "graduate_degree", f"{persona} should have graduate degree"
            elif "teacher" in persona:
                assert modifiers["education_level"] in ["college_degree", "graduate_degree"], f"{persona} should have college+ education"
            else:
                assert modifiers["education_level"] in ["college_degree", "some_college"], f"{persona} should have college-level education"
    
    def test_parent_personas_get_parent_life_stage(self):
        """Parent personas should get 'parent' life stage and family topics."""
        parent_personas = [
            "helicopter_mom_of_twins",
            "single_dad_juggling_work_life", 
            "homeschooling_parent_activist"
        ]
        
        for persona in parent_personas:
            modifiers = sample_modifiers("individual", persona)
            assert modifiers["life_stage"] == "parent", f"{persona} should have parent life stage"
            assert modifiers["primary_topic"] == "family_kids", f"{persona} should focus on family topics"
    
    def test_middle_aged_personas_get_middle_aged_life_stage(self):
        """Middle-aged personas should get 'middle_aged' life stage."""
        middle_aged_personas = [
            "midlife_crisis_divorcee",
            "wine_mom_book_club_president", 
            "weekend_warrior_mountain_biker",
            "conspiracy_theory_uncle"
        ]
        
        for persona in middle_aged_personas:
            modifiers = sample_modifiers("individual", persona)
            assert modifiers["life_stage"] == "middle_aged", f"{persona} should have middle_aged life stage"
            
            # Special case: conspiracy theory uncle should have right-leaning politics
            if "conspiracy" in persona:
                assert modifiers["political_leaning"] in ["far_right_extremist", "conservative_republican"], f"{persona} should have right-leaning politics"
    
    def test_retired_personas_get_retired_life_stage(self):
        """Retired personas should get 'retired' life stage."""
        retired_personas = [
            "facebook_grandma_oversharer",
            "retired_professor_still_teaching",
            "grumpy_boomer_hates_technology"
        ]
        
        for persona in retired_personas:
            modifiers = sample_modifiers("individual", persona)
            assert modifiers["life_stage"] == "retired", f"{persona} should have retired life stage"
            
            # Special case: professor should have graduate degree
            if "professor" in persona:
                assert modifiers["education_level"] == "graduate_degree", f"{persona} should have graduate degree"
            
            # Special case: boomer should have conservative politics
            if "boomer" in persona:
                assert modifiers["political_leaning"] in ["conservative_republican", "far_right_extremist"], f"{persona} should have conservative politics"
    
    def test_anxiety_persona_gets_anxious_communication(self):
        """Anxiety-ridden high schooler should get anxious communication style."""
        modifiers = sample_modifiers("individual", "anxiety_ridden_high_schooler")
        assert modifiers["communication_style"] == "anxious_oversharing", "Anxiety persona should have anxious communication"
    
    def test_athlete_persona_gets_achievement_topics(self):
        """Competitive athlete should focus on achievements."""
        modifiers = sample_modifiers("individual", "competitive_teenage_athlete")
        assert modifiers["primary_topic"] == "achievements_bragging", "Athlete persona should focus on achievements"


class TestAccountTypeModifiers:
    """Test that each account type gets only appropriate modifiers."""
    
    def test_individual_account_modifiers(self):
        """Individual accounts should only get individual-specific modifiers."""
        expected_categories = {
            "communication_style", "posting_mood", "education_level", 
            "political_leaning", "life_stage", "primary_topic"
        }
        
        modifiers = sample_modifiers("individual", "some_random_persona")
        assert set(modifiers.keys()) == expected_categories, "Individual accounts should have correct modifier categories"
    
    def test_brand_business_account_modifiers(self):
        """Brand business accounts should only get business-specific modifiers."""
        expected_categories = {
            "brand_voice", "marketing_style", "business_stage", 
            "target_audience", "content_focus"
        }
        
        modifiers = sample_modifiers("brand_business", "some_business")
        assert set(modifiers.keys()) == expected_categories, "Business accounts should have correct modifier categories"
    
    def test_influencer_account_modifiers(self):
        """Influencer accounts should only get influencer-specific modifiers."""
        expected_categories = {
            "influencer_persona", "content_style", "follower_relationship", "monetization_approach"
        }
        
        modifiers = sample_modifiers("influencer_public_figure", "some_influencer")
        assert set(modifiers.keys()) == expected_categories, "Influencer accounts should have correct modifier categories"
    
    def test_media_news_account_modifiers(self):
        """Media news accounts should only get media-specific modifiers."""
        expected_categories = {
            "editorial_stance", "reporting_style", "audience_tone", "content_priority"
        }
        
        modifiers = sample_modifiers("media_news", "some_news_outlet")
        assert set(modifiers.keys()) == expected_categories, "Media accounts should have correct modifier categories"
    
    def test_bot_account_modifiers(self):
        """Bot accounts should only get bot-specific modifiers."""
        expected_categories = {
            "bot_personality", "response_pattern", "content_type"
        }
        
        modifiers = sample_modifiers("bot", "some_bot")
        assert set(modifiers.keys()) == expected_categories, "Bot accounts should have correct modifier categories"
    
    def test_spam_scam_account_modifiers(self):
        """Spam/scam accounts should only get scam-specific modifiers."""
        expected_categories = {
            "scam_approach", "writing_quality", "target_vulnerability"
        }
        
        modifiers = sample_modifiers("spam_scam", "some_scam")
        assert set(modifiers.keys()) == expected_categories, "Spam accounts should have correct modifier categories"
    
    def test_meme_account_modifiers(self):
        """Meme accounts should only get meme-specific modifiers."""
        expected_categories = {
            "humor_style", "meme_format", "target_demographic", "content_freshness"
        }
        
        modifiers = sample_modifiers("creative_meme", "some_meme_account")
        assert set(modifiers.keys()) == expected_categories, "Meme accounts should have correct modifier categories"


class TestAccountGeneration:
    """Test the complete account generation process."""
    
    def test_sample_account_returns_valid_structure(self):
        """Generated accounts should have correct structure."""
        account = sample_account()
        
        # Check required keys exist
        assert "account_type" in account
        assert "persona" in account  
        assert "modifiers" in account
        
        # Check account type is valid
        assert account["account_type"] in [
            "individual", "brand_business", "influencer_public_figure", 
            "media_news", "bot", "spam_scam", "creative_meme"
        ]
        
        # Check persona matches account type
        assert account["persona"] in PERSONAS_BY_TYPE[account["account_type"]]
        
        # Check modifiers match account type
        expected_modifiers = set(MODIFIERS_BY_ACCOUNT_TYPE[account["account_type"]].keys())
        actual_modifiers = set(account["modifiers"].keys())
        assert actual_modifiers == expected_modifiers
    
    def test_multiple_account_generation_consistency(self):
        """Generate multiple accounts and verify consistency."""
        for _ in range(50):  # Test with many samples
            account = sample_account()
            
            # Verify structure
            assert len(account) == 3
            assert isinstance(account["modifiers"], dict)
            
            # If it's an individual account, verify persona-modifier logic
            if account["account_type"] == "individual":
                persona = account["persona"]
                modifiers = account["modifiers"]
                
                # Check life stage consistency
                if any(word in persona for word in ["high_schooler", "teenage", "theatre_kid"]):
                    assert modifiers["life_stage"] == "teenager"
                elif "student" in persona:
                    assert modifiers["life_stage"] == "college_student"
                elif any(word in persona for word in ["lawyer", "teacher", "designer", "tech_bro", "nurse"]):
                    assert modifiers["life_stage"] == "young_professional"
                elif any(word in persona for word in ["mom", "dad", "parent"]) and "wine_mom" not in persona:
                    assert modifiers["life_stage"] == "parent"
                    assert modifiers["primary_topic"] == "family_kids"
                elif any(word in persona for word in ["midlife", "wine_mom", "weekend_warrior", "conspiracy", "uncle"]):
                    assert modifiers["life_stage"] == "middle_aged"
                elif any(word in persona for word in ["grandma", "retired", "boomer"]):
                    assert modifiers["life_stage"] == "retired"


class TestSystemPromptGeneration:
    """Test system prompt generation for different account types."""
    
    def test_system_prompt_contains_persona_info(self):
        """System prompt should contain persona and modifier information."""
        from generate_posts import generate_system_prompt
        
        account = {
            "account_type": "individual",
            "persona": "burned_out_corporate_lawyer",
            "modifiers": {
                "communication_style": "sarcastic_witty",
                "life_stage": "young_professional",
                "education_level": "graduate_degree"
            }
        }
        
        prompt = generate_system_prompt(account)
        
        # Check key elements are present
        assert "Burned Out Corporate Lawyer" in prompt
        assert "Individual" in prompt
        assert "Sarcastic Witty" in prompt
        assert "Young Professional" in prompt
        assert "Graduate Degree" in prompt
        assert "50-100 realistic social media posts" in prompt
    
    def test_system_prompt_account_type_specific_sections(self):
        """System prompt should have account-type-specific sections."""
        from generate_posts import generate_system_prompt
        
        # Test individual account
        individual_account = {
            "account_type": "individual", 
            "persona": "test",
            "modifiers": {"communication_style": "casual_friendly"}
        }
        individual_prompt = generate_system_prompt(individual_account)
        assert "PERSONALITY & STYLE:" in individual_prompt
        
        # Test business account
        business_account = {
            "account_type": "brand_business",
            "persona": "test", 
            "modifiers": {"brand_voice": "professional_corporate"}
        }
        business_prompt = generate_system_prompt(business_account)
        assert "BRAND CHARACTERISTICS:" in business_prompt