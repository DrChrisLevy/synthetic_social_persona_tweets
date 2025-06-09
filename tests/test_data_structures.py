"""Tests for data structure integrity and consistency."""

from generate_posts import ACCOUNT_DATA


class TestDataStructureIntegrity:
    """Test that all data structures are properly defined and consistent."""

    def test_account_type_distribution_sums_to_one(self):
        """Account type weights should sum to approximately 1.0."""
        total_weight = sum(
            ACCOUNT_DATA[account_type]["weight"] for account_type in ACCOUNT_DATA.keys()
        )
        assert abs(total_weight - 1.0) < 0.001, (
            f"Weights sum to {total_weight}, should be 1.0"
        )

    def test_account_type_distribution_has_required_fields(self):
        """Each account type should have name and weight."""
        for account_type, data in ACCOUNT_DATA.items():
            assert "weight" in data, (
                f"Account type '{account_type}' missing 'weight' field"
            )
            assert isinstance(data["weight"], (int, float)), (
                f"Weight should be numeric for '{account_type}'"
            )
            assert data["weight"] > 0, f"Weight should be positive for '{account_type}'"

    def test_personas_by_type_covers_all_account_types(self):
        """All account types should have personas defined."""
        for account_type, data in ACCOUNT_DATA.items():
            assert "personas" in data, (
                f"Account type '{account_type}' missing 'personas' field"
            )

    def test_modifiers_by_account_type_covers_all_account_types(self):
        """All account types should have modifiers defined."""
        for account_type, data in ACCOUNT_DATA.items():
            assert "modifiers" in data, (
                f"Account type '{account_type}' missing 'modifiers' field"
            )

    def test_all_persona_lists_not_empty(self):
        """Each account type should have at least one persona."""
        for account_type, data in ACCOUNT_DATA.items():
            personas = data["personas"]
            assert len(personas) > 0, f"Account type '{account_type}' has no personas"
            assert all(isinstance(persona, str) for persona in personas), (
                f"All personas should be strings in '{account_type}'"
            )

    def test_all_modifier_lists_not_empty(self):
        """Each account type should have at least one modifier category."""
        for account_type, data in ACCOUNT_DATA.items():
            modifiers = data["modifiers"]
            assert len(modifiers) > 0, (
                f"Account type '{account_type}' has no modifier categories"
            )

            for category, options in modifiers.items():
                assert len(options) > 0, (
                    f"Modifier category '{category}' in '{account_type}' has no options"
                )
                assert all(isinstance(option, str) for option in options), (
                    f"All modifier options should be strings in '{account_type}.{category}'"
                )

    def test_persona_names_follow_conventions(self):
        """Persona names should follow naming conventions."""
        for account_type, data in ACCOUNT_DATA.items():
            personas = data["personas"]
            for persona in personas:
                # Should be lowercase with underscores
                assert persona.islower() or "_" in persona, (
                    f"Persona '{persona}' should be lowercase with underscores"
                )
                # Should not start or end with underscore
                assert not persona.startswith("_"), (
                    f"Persona '{persona}' should not start with underscore"
                )
                assert not persona.endswith("_"), (
                    f"Persona '{persona}' should not end with underscore"
                )
                # Should not have double underscores
                assert "__" not in persona, (
                    f"Persona '{persona}' should not have double underscores"
                )

    def test_modifier_option_names_follow_conventions(self):
        """Modifier option names should follow naming conventions."""
        for account_type, data in ACCOUNT_DATA.items():
            modifiers = data["modifiers"]
            for category, options in modifiers.items():
                for option in options:
                    # Should be lowercase with underscores
                    assert option.islower() or "_" in option, (
                        f"Modifier '{option}' in '{account_type}.{category}' should be lowercase with underscores"
                    )
                    # Should not start or end with underscore
                    assert not option.startswith("_"), (
                        f"Modifier '{option}' should not start with underscore"
                    )
                    assert not option.endswith("_"), (
                        f"Modifier '{option}' should not end with underscore"
                    )


class TestPersonaKeywordConsistency:
    """Test that persona names contain appropriate keywords for their categorization."""

    def test_individual_personas_have_appropriate_keywords(self):
        """Individual personas should have keywords that match their life stage logic."""
        individual_personas = ACCOUNT_DATA["individual"]["personas"]

        # Define expected keyword patterns
        teen_keywords = ["high_schooler", "teenage", "theatre_kid"]
        student_keywords = ["student"]
        professional_keywords = ["lawyer", "teacher", "designer", "tech_bro", "nurse"]
        parent_keywords = ["mom", "dad", "parent"]
        middle_aged_keywords = [
            "midlife",
            "wine_mom",
            "weekend_warrior",
            "conspiracy",
            "uncle",
        ]
        retired_keywords = ["grandma", "retired", "boomer"]

        all_expected_keywords = (
            teen_keywords
            + student_keywords
            + professional_keywords
            + parent_keywords
            + middle_aged_keywords
            + retired_keywords
        )

        for persona in individual_personas:
            # Each individual persona should contain at least one expected keyword
            has_expected_keyword = any(
                keyword in persona for keyword in all_expected_keywords
            )
            assert has_expected_keyword, (
                f"Individual persona '{persona}' should contain at least one categorizing keyword"
            )

    def test_brand_personas_sound_like_businesses(self):
        """Brand personas should sound like actual businesses."""
        brand_personas = ACCOUNT_DATA["brand_business"]["personas"]

        # Common business keywords
        business_keywords = [
            "restaurant",
            "bookstore",
            "brewery",
            "studio",
            "bar",
            "agency",
            "agent",
            "firm",
            "planning",
            "startup",
            "company",
            "scheme",
            "brand",
            "business",
            "shop",
            "store",
        ]

        for persona in brand_personas:
            has_business_keyword = any(
                keyword in persona for keyword in business_keywords
            )
            assert has_business_keyword, (
                f"Brand persona '{persona}' should contain business-related keywords"
            )

    def test_bot_personas_contain_bot_keyword(self):
        """Bot personas should contain 'bot' in their name."""
        bot_personas = ACCOUNT_DATA["bot"]["personas"]

        for persona in bot_personas:
            bot_related_keywords = [
                "bot",
                "alerts",
                "quotes",
                "facts",
                "wishes",
                "generator",
                "daily",
                "picture",
                "word",
                "ai",
                "notifications",
                "updates",
                "tracking",
                "price",
                "motivational",
                "historical",
                "astronomy",
                "birthday",
                "compliment",
                "engagement",
                "poetry",
                "gibberish",
                "sentient",
            ]
            has_bot_keyword = any(
                keyword in persona for keyword in bot_related_keywords
            )
            assert has_bot_keyword, (
                f"Bot persona '{persona}' should contain bot-related keywords"
            )

    def test_spam_personas_sound_like_scams(self):
        """Spam/scam personas should contain scam-related keywords."""
        spam_personas = ACCOUNT_DATA["spam_scam"]["personas"]

        scam_keywords = [
            "pump",
            "scheme",
            "fake",
            "scam",
            "phishing",
            "giveaway",
            "investment",
            "mlm",
            "catfish",
            "military",
            "billionaire",
            "contest",
            "bank",
            "irs",
            "security",
            "miracle",
            "counterfeit",
            "crypto",
            "forex",
            "opportunity",
            "essential",
            "oils",
            "hun",
            "deployed",
            "overseas",
            "widowed",
            "soulmate",
            "iphone",
            "celebrity",
            "endorsed",
            "survey",
            "promise",
            "alert",
            "refund",
            "suspension",
            "weight",
            "loss",
            "supplement",
            "designer",
            "handbag",
            "seller",
            "dealer",
            "electronics",
        ]

        for persona in spam_personas:
            has_scam_keyword = any(keyword in persona for keyword in scam_keywords)
            assert has_scam_keyword, (
                f"Spam persona '{persona}' should contain scam-related keywords"
            )


class TestModifierCategories:
    """Test that modifier categories are appropriate for each account type."""

    def test_individual_modifier_categories_are_personal(self):
        """Individual accounts should have personal modifier categories."""
        individual_modifiers = ACCOUNT_DATA["individual"]["modifiers"]

        expected_categories = {
            "communication_style",
            "posting_mood",
            "education_level",
            "political_leaning",
            "life_stage",
            "primary_topic",
        }

        assert set(individual_modifiers.keys()) == expected_categories, (
            "Individual accounts should have personal modifier categories"
        )

    def test_business_modifier_categories_are_business_focused(self):
        """Business accounts should have business-focused modifier categories."""
        business_modifiers = ACCOUNT_DATA["brand_business"]["modifiers"]

        expected_categories = {
            "brand_voice",
            "marketing_style",
            "business_stage",
            "target_audience",
            "content_focus",
        }

        assert set(business_modifiers.keys()) == expected_categories, (
            "Business accounts should have business modifier categories"
        )

    def test_influencer_modifier_categories_are_influencer_focused(self):
        """Influencer accounts should have influencer-focused modifier categories."""
        influencer_modifiers = ACCOUNT_DATA["influencer_public_figure"]["modifiers"]

        expected_categories = {
            "influencer_persona",
            "content_style",
            "follower_relationship",
            "monetization_approach",
        }

        assert set(influencer_modifiers.keys()) == expected_categories, (
            "Influencer accounts should have influencer modifier categories"
        )

    def test_modifier_categories_dont_overlap_inappropriately(self):
        """Account types shouldn't share inappropriate modifier categories."""
        individual_mods = set(ACCOUNT_DATA["individual"]["modifiers"].keys())
        business_mods = set(ACCOUNT_DATA["brand_business"]["modifiers"].keys())
        influencer_mods = set(
            ACCOUNT_DATA["influencer_public_figure"]["modifiers"].keys()
        )

        # These should not overlap
        assert len(individual_mods & business_mods) == 0, (
            "Individual and business modifiers should not overlap"
        )
        assert len(individual_mods & influencer_mods) == 0, (
            "Individual and influencer modifiers should not overlap"
        )
        assert len(business_mods & influencer_mods) == 0, (
            "Business and influencer modifiers should not overlap"
        )
