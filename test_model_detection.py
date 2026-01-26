from app.orchestrator import run_model_detection

if __name__ == "__main__":
    result = run_model_detection("samples/test_repo_multi")
    print(result)
