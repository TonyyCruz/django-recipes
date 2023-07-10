import json

mock_recipe = json.dumps(
    {
        "title": "Mock Recipe",
        "description": "My Description",
        "preparation_time": 10,
        "preparation_time_unit": "min",
        "servings": 10,
        "servings_unit": "portions",
        "preparation_steps": """mock recipe mock recipe mock recipe mock recipe
    mock recipe mock recipe mock recipe mock recipe mock recipe mock recipe
    mock recipe mock recipe mock recipe mock recipe mock recipe mock recipe
    mock recipe mock recipe mock recipe """,
    }
)
