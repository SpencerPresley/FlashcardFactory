def load_test_data() -> str:
    with open("../static/StrategyPatternInClassExercise.txt", "r") as file:
        content = file.read()
        print(f"Loaded {len(content)} characters")
        return content