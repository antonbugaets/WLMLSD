from workers_src.start_worker import celery_app


@celery_app.task(name="make_scenario")
def scenario_creation(text: str, prompt: str):
    print(f"Text: {text}")
    print(f"Prompt: {prompt}")
    pass
