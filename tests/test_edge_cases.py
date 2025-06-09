"""Tests for edge cases and error handling."""

import pytest

from generate_posts import (
    generate_posts_for_account,
    generate_system_prompt,
    sample_account_type,
    sample_modifiers,
    sample_persona,
)


class TestEdgeCases:
    """Test edge cases and error handling."""

    def test_sample_modifiers_with_invalid_account_type(self):
        """Should handle invalid account types gracefully."""
        modifiers = sample_modifiers("invalid_account_type", "some_persona")
        assert modifiers == {}, "Invalid account type should return empty modifiers"

    def test_sample_modifiers_with_none_persona(self):
        """Should handle None persona gracefully."""
        modifiers = sample_modifiers("individual", None)
        assert len(modifiers) > 0, (
            "Should still return modifiers even with None persona"
        )
        assert "life_stage" in modifiers, "Should have required modifier categories"

    def test_sample_modifiers_with_empty_persona(self):
        """Should handle empty persona string gracefully."""
        modifiers = sample_modifiers("individual", "")
        assert len(modifiers) > 0, (
            "Should still return modifiers even with empty persona"
        )
        # Should fall back to random sampling for unmatched persona

    def test_sample_modifiers_with_unknown_persona(self):
        """Should handle unknown persona names gracefully."""
        modifiers = sample_modifiers("individual", "completely_unknown_persona_12345")
        assert len(modifiers) > 0, "Should still return modifiers for unknown persona"
        # Should fall back to random sampling

    def test_sample_persona_with_invalid_account_type(self):
        """Should handle invalid account types."""
        with pytest.raises(KeyError):
            sample_persona("invalid_account_type")

    def test_system_prompt_with_missing_modifiers(self):
        """Should handle accounts with missing modifier categories."""
        account = {
            "account_type": "individual",
            "persona": "test_persona",
            "modifiers": {
                "communication_style": "casual_friendly"
                # Missing other expected modifiers
            },
        }

        prompt = generate_system_prompt(account)
        assert "test persona" in prompt.lower(), (
            "Should still generate prompt with partial modifiers"
        )
        assert "Communication Style: Casual Friendly" in prompt, (
            "Should include available modifiers"
        )

    def test_system_prompt_with_empty_modifiers(self):
        """Should handle accounts with no modifiers."""
        account = {
            "account_type": "individual",
            "persona": "test_persona",
            "modifiers": {},
        }

        prompt = generate_system_prompt(account)
        assert "test persona" in prompt.lower(), (
            "Should still generate prompt with no modifiers"
        )
        assert "No specific characteristics defined" in prompt, (
            "Should indicate missing modifiers"
        )

    def test_generate_posts_for_account_with_minimal_data(self):
        """Should handle minimal account data."""
        account = {
            "account_type": "individual",
            "persona": "minimal_test",
            "modifiers": {},
        }

        result = generate_posts_for_account(account)

        assert "account_profile" in result
        assert "system_prompt" in result
        assert "instructions" in result
        assert "metadata" in result
        assert result["metadata"]["generation_ready"] is True


class TestRandomness:
    """Test randomness and variation in generation."""

    def test_multiple_samples_show_variation(self):
        """Multiple samples should show variation in modifiers."""
        samples = []
        for _ in range(20):
            modifiers = sample_modifiers("individual", "unmatched_persona")
            samples.append(modifiers["communication_style"])

        # Should have some variation
        unique_values = set(samples)
        assert len(unique_values) > 1, "Should show variation in random sampling"

    def test_account_type_sampling_shows_variation(self):
        """Multiple account type samples should show variation."""
        samples = []
        for _ in range(50):
            account_type = sample_account_type()
            samples.append(account_type)

        unique_types = set(samples)
        assert len(unique_types) > 1, "Should generate different account types"
        # "individual" should be most common due to 0.60 weight
        assert samples.count("individual") > 20, "Individual accounts should be common"

    def test_persona_sampling_within_type_shows_variation(self):
        """Multiple persona samples within same type should vary."""
        samples = []
        for _ in range(30):
            persona = sample_persona("individual")
            samples.append(persona)

        unique_personas = set(samples)
        assert len(unique_personas) > 1, (
            "Should generate different personas within account type"
        )


class TestBoundaryConditions:
    """Test boundary conditions and limits."""

    def test_very_long_persona_name(self):
        """Should handle very long persona names."""
        long_persona = (
            "very_long_persona_name_that_goes_on_and_on_with_many_words_" * 10
        )
        modifiers = sample_modifiers("individual", long_persona)
        assert len(modifiers) > 0, "Should handle long persona names"

    def test_persona_with_special_characters(self):
        """Should handle persona names with special characters."""
        special_personas = [
            "persona-with-dashes",
            "persona.with.dots",
            "persona with spaces",
            "persona123with456numbers",
        ]

        for persona in special_personas:
            modifiers = sample_modifiers("individual", persona)
            assert len(modifiers) > 0, f"Should handle persona '{persona}'"

    def test_case_sensitivity_in_persona_matching(self):
        """Test case sensitivity in persona keyword matching."""
        # These should be treated differently
        upper_persona = "ANXIETY_RIDDEN_HIGH_SCHOOLER"
        lower_persona = "anxiety_ridden_high_schooler"

        upper_modifiers = sample_modifiers("individual", upper_persona)
        lower_modifiers = sample_modifiers("individual", lower_persona)

        # Lower case should match our patterns, upper case should fall back to random
        assert lower_modifiers["life_stage"] == "teenager", (
            "Lowercase should match pattern"
        )
        # Upper case may or may not match depending on implementation
        # Both should still return valid modifiers
        assert "life_stage" in upper_modifiers, "Should return modifiers for uppercase"
        assert "life_stage" in lower_modifiers, "Should return modifiers for lowercase"


class TestConsistencyChecks:
    """Test consistency across multiple generations."""

    def test_same_persona_gets_consistent_deterministic_mappings(self):
        """Same persona should get same deterministic mappings multiple times."""
        persona = "anxiety_ridden_high_schooler"

        life_stages = []
        communication_styles = []
        education_levels = []

        for _ in range(10):
            modifiers = sample_modifiers("individual", persona)
            life_stages.append(modifiers["life_stage"])
            communication_styles.append(modifiers["communication_style"])
            education_levels.append(modifiers["education_level"])

        # Life stage should always be deterministic for this persona
        assert all(stage == "teenager" for stage in life_stages), (
            "Life stage should be deterministic for anxiety_ridden_high_schooler"
        )

        # Communication style should be deterministic for this specific persona
        assert all(style == "anxious_oversharing" for style in communication_styles), (
            "Communication should be deterministic for anxiety_ridden_high_schooler"
        )

        # Education should be from the restricted set
        valid_education = {"high_school_dropout", "high_school_grad"}
        assert all(edu in valid_education for edu in education_levels), (
            "Education should be from valid teen set"
        )

    def test_parent_personas_always_get_family_topics(self):
        """All parent personas should consistently get family topics."""
        parent_personas = [
            "helicopter_mom_of_twins",
            "single_dad_juggling_work_life",
            "homeschooling_parent_activist",
        ]

        for persona in parent_personas:
            for _ in range(5):  # Test multiple times
                modifiers = sample_modifiers("individual", persona)
                assert modifiers["life_stage"] == "parent", (
                    f"{persona} should always be parent"
                )
                assert modifiers["primary_topic"] == "family_kids", (
                    f"{persona} should always focus on family"
                )

    def test_professor_always_gets_graduate_degree(self):
        """Retired professor should always get graduate degree."""
        persona = "retired_professor_still_teaching"

        for _ in range(10):
            modifiers = sample_modifiers("individual", persona)
            assert modifiers["life_stage"] == "retired", "Professor should be retired"
            assert modifiers["education_level"] == "graduate_degree", (
                "Professor should have graduate degree"
            )
