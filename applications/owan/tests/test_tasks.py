import owan.tasks


def test_enqueueable(image_path_factory):
    factory = owan.tasks.Factory(broker="memory://localhost")
    async_result = factory.broker.test_predict(str(image_path_factory()))
    # Because currently we have no plan to get return value from Celery,
    # we don't set any backend. So there is no way to get the task
    # complete status from Celery. As a result, we just check existence
    # of task_id here.
    assert async_result.task_id
