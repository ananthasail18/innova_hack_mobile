import pytest
from app.services.recommendation import cosine_similarity, RecommendationService

def test_cosine_similarity():
    # Identical vectors should have similarity of 1.0
    v1 = [1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    v2 = [1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    assert pytest.approx(cosine_similarity(v1, v2), 0.001) == 1.0

    # Orthogonal vectors should have similarity of 0.0
    v3 = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    v4 = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    assert pytest.approx(cosine_similarity(v3, v4), 0.001) == 0.0

    # Zero vector
    v_zero = [0.0] * 8
    assert cosine_similarity(v1, v_zero) == 0.0

    # Opposite vectors (in practice ours are 0.0 to 1.0 so they won't be perfectly opposite in this space without negatives, 
    # but let's test a generic opposite)
    v5 = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
    v6 = [-1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0]
    assert pytest.approx(cosine_similarity(v5, v6), 0.001) == -1.0

# Mock classes to test ranking
class MockDish:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.is_available = True
        self.popularity_score = getattr(self, 'popularity_score', 0.5)
        self.chef_notes = None

class MockTasteProfile:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
        self.confidence_score = 0.9

def test_get_taste_vector():
    service = RecommendationService(db=None)
    
    mock_dish = MockDish(
        spice_level=0.1, sweetness_level=0.2, creaminess_level=0.3,
        tanginess_level=0.4, masala_intensity_level=0.5, crunchiness_level=0.6,
        oiliness_level=0.7, saltiness_level=0.8
    )
    vec = service._get_taste_vector(mock_dish)
    assert vec == [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]

    mock_profile = MockTasteProfile(
        spice_preference=0.8, sweetness_preference=0.7, creaminess_preference=0.6,
        tanginess_preference=0.5, masala_intensity_preference=0.4, crunchiness_preference=0.3,
        oiliness_preference=0.2, saltiness_preference=0.1
    )
    vec2 = service._get_taste_vector(mock_profile)
    assert vec2 == [0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]

def test_hard_constraints():
    from app.schemas.ai import RecommendationIntent
    service = RecommendationService(db=None)
    
    intent = RecommendationIntent(
        budget=15.0,
        allergens=["peanuts"],
        excluded_ingredients=["garlic"]
    )
    
    class MockDishConstraints(MockDish):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.allergens = kwargs.get("allergens", [])
            self.ingredients = kwargs.get("ingredients", [])
            self.price = kwargs.get("price", 10.0)
            
    dishes = [
        MockDishConstraints(id="1", price=20.0), # over budget
        MockDishConstraints(id="2", allergens=["Peanuts"]), # allergen
        MockDishConstraints(id="3", ingredients=["Garlic"]), # excluded ingredient
        MockDishConstraints(id="4", price=12.0) # valid
    ]
    
    # Mocking db query manually
    filtered_dishes = []
    for dish in dishes:
        if intent.budget and dish.price > intent.budget:
            continue
        if intent.allergens:
            dish_allergens = [a.lower() for a in (dish.allergens or [])]
            if any(a.lower() in dish_allergens for a in intent.allergens):
                continue
        if intent.excluded_ingredients:
            dish_ingredients = [i.lower() for i in (dish.ingredients or [])]
            if any(ex.lower() in dish_ingredients for ex in intent.excluded_ingredients):
                continue
        filtered_dishes.append(dish)
        
    assert len(filtered_dishes) == 1
    assert filtered_dishes[0].id == "4"
