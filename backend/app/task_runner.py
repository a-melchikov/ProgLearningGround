import docker
from task_data_loader import open_tasks_json, TEST_CASES, INPUT, OUTPUT
from code_tester import get_testing_code
from logger_setup import get_logger

logger = get_logger(__name__)


def run_code_in_docker(task_name: str, user_code: str) -> str:
    """
    Runs the user's code in a Docker container and validates it against test cases.

    Args:
        task_name (str): The name of the task to be tested.
        user_code (str): The user's Python code as a string.

    Returns:
        str: A summary string indicating the number and percentage of tests passed.

    Raises:
        FileNotFoundError: If the tasks JSON file is not found.
        docker.errors.DockerException: If there is an issue with Docker.
    """
    client = docker.from_env()
    passed_tests = 0

    try:
        data = open_tasks_json(task_name)
        logger.info(f"Loaded tasks for {task_name} successfully.")
    except FileNotFoundError as e:
        logger.error(f"Task file not found: {e}")
        return "Error: Task file not found."

    test_cases = data.get(TEST_CASES, [])

    if not test_cases:
        logger.warning(f"No test cases found for task '{task_name}'.")
        return "Warning: No test cases found."

    for idx, test_case in enumerate(test_cases, start=1):
        test_input = test_case[INPUT]
        expected_output = test_case[OUTPUT]

        test_script = get_testing_code(user_code, test_input, expected_output)

        try:
            logger.info(f"Running test case {idx} with input: {test_input}")
            container = client.containers.run(
                "python:3.12-slim",
                command=["python", "-c", test_script],
                detach=True,
                stderr=True,
                stdout=True,
                remove=True,
                mem_limit="128m",
                cpu_quota=50000,
            )
            container.wait()
            logs = container.logs().decode("utf-8").strip()

            logger.debug(f"Container logs for test case {idx}: {logs}")

            if "PASS" in logs:
                passed_tests += 1
                logger.info(f"Test case {idx} passed.")
            else:
                logger.warning(
                    f"Test case {idx} failed. Expected: {expected_output}, Got: {logs}"
                )
        except docker.errors.ContainerError as e:
            logger.error(
                f"Test case {idx} failed due to a container error: {e.stderr.decode('utf-8')}"
            )
        except docker.errors.DockerException as e:
            logger.error(f"Test case {idx} failed due to a Docker error: {str(e)}")

    total_tests = len(test_cases)
    percentage = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    result_string = (
        f"{passed_tests} out of {total_tests} tests passed ({percentage:.2f}%)."
    )
    logger.info(f"Testing summary for {task_name}: {result_string}")
    client.close()
    return result_string


if __name__ == "__main__":
    task_name = "sum_with_inversion"

    user_code = """
number = int(input())
reversed_number = int(str(number)[::-1])
print(f"{number} + {reversed_number} = {number + reversed_number}")
    """

    summary = run_code_in_docker(task_name, user_code)
    print(summary)
