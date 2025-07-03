import json
import sys
import time
from typing import Any, Dict

from google.api_core import exceptions
from google.cloud import artifactregistry_v1, logging_v2, run_v2

GCP_PROJECT_ID: str = "sl1p-production"
GCP_REGION: str = "europe-west2"
JOB_NAME: str = "dave-io-test-suite"
ORIGINAL_IMAGE_NAME: str = "ghcr.io/daveio/dave-io-test-suite:latest"
AR_REMOTE_REPO_NAME: str = "ghcr-io"
POLLING_INTERVAL_S: int = 5


def log_status(message: str) -> None:
    """Logs a status message to stderr."""
    print(f"[STATUS] {message}", file=sys.stderr)


def setup_artifact_registry(
    ar_client: artifactregistry_v1.ArtifactRegistryClient,
) -> str:
    """
    Ensures the Artifact Registry remote repository exists to proxy ghcr.io.

    Args:
        ar_client: An authenticated Artifact Registry client.

    Returns:
        The full, proxied image path to be used by Cloud Run.
    """
    parent = f"projects/{GCP_PROJECT_ID}/locations/{GCP_REGION}"
    repo_path = f"{parent}/repositories/{AR_REMOTE_REPO_NAME}"

    log_status(
        f"Checking for Artifact Registry remote repository '{AR_REMOTE_REPO_NAME}'..."
    )
    try:
        ar_client.get_repository(name=repo_path)  # type: ignore
        log_status("Repository already exists.")
    except exceptions.NotFound:
        log_status(
            "Repository not found. Creating remote repository to proxy ghcr.io..."
        )
        repo = artifactregistry_v1.Repository(
            name=repo_path,
            format_=artifactregistry_v1.Repository.Format.DOCKER,
            description="Remote proxy for ghcr.io images",
            mode=artifactregistry_v1.Repository.Mode.REMOTE_REPOSITORY,
            remote_repository_config=artifactregistry_v1.RemoteRepositoryConfig(
                docker_repository=artifactregistry_v1.RemoteRepositoryConfig.DockerRepository(
                    custom_repository=artifactregistry_v1.RemoteRepositoryConfig.DockerRepository.CustomRepository(
                        uri="https://ghcr.io"
                    )
                )
            ),
        )
        create_op = ar_client.create_repository(  # type: ignore
            request={
                "parent": parent,
                "repository": repo,
                "repository_id": AR_REMOTE_REPO_NAME,
            }
        )
        create_op.result()  # type: ignore
        log_status(f"Repository '{AR_REMOTE_REPO_NAME}' created.")

    image_path_in_repo = "/".join(ORIGINAL_IMAGE_NAME.split("/")[1:])
    proxy_image_name = f"{GCP_REGION}-docker.pkg.dev/{GCP_PROJECT_ID}/{AR_REMOTE_REPO_NAME}/{image_path_in_repo}"
    log_status(f"Using proxied image path: {proxy_image_name}")
    return proxy_image_name


def deploy_job(run_client: run_v2.JobsClient, image_name: str) -> None:
    """
    Deploys the Cloud Run Job definition, creating or updating as needed.

    Args:
        run_client: An authenticated Cloud Run Jobs client.
        image_name: The container image path to use for the job.
    """
    parent = f"projects/{GCP_PROJECT_ID}/locations/{GCP_REGION}"
    job_path = f"{parent}/jobs/{JOB_NAME}"

    container = run_v2.Container(image=image_name)
    template = run_v2.ExecutionTemplate(
        template=run_v2.TaskTemplate(containers=[container])
    )
    job_definition = run_v2.Job(template=template)

    log_status(f"Deploying Cloud Run Job definition '{JOB_NAME}'...")
    try:
        run_client.get_job(name=job_path)  # type: ignore
        # Job exists, so we perform an update.
        job_definition.name = job_path
        operation = run_client.update_job(request={"job": job_definition})  # type: ignore
    except exceptions.NotFound:
        # Job doesn't exist, so we create it.
        operation = run_client.create_job(  # type: ignore
            request={"parent": parent, "job": job_definition, "job_id": JOB_NAME}
        )

    operation.result()  # type: ignore
    log_status("Job definition is up to date.")


def run_and_wait_for_job(
    run_client: run_v2.JobsClient, executions_client: run_v2.ExecutionsClient
) -> run_v2.Execution:
    """
    Executes the job and polls until completion.

    Args:
        run_client: An authenticated Cloud Run Jobs client.
        executions_client: An authenticated Cloud Run Executions client.

    Returns:
        The final, completed Execution object.
    """
    job_path = f"projects/{GCP_PROJECT_ID}/locations/{GCP_REGION}/jobs/{JOB_NAME}"

    log_status(f"Executing a new run of job '{JOB_NAME}'...")
    run_op = run_client.run_job(name=job_path)  # type: ignore

    if not run_op.metadata:  # type: ignore
        raise RuntimeError("RunJob operation did not return metadata.")

    execution_name: str = run_op.metadata.name  # type: ignore
    log_status(f"Job execution started successfully. Execution Name: {execution_name}")

    log_status("Polling for completion...")
    while True:
        execution = executions_client.get_execution(name=execution_name)  # type: ignore
        if execution.completion_time and not execution.reconciling:
            log_status("Execution has completed.")
            return execution

        last_condition = execution.conditions[-1]
        log_status(f"Current status: {last_condition.type_}. Waiting...")
        time.sleep(POLLING_INTERVAL_S)


def get_job_logs(logging_client: logging_v2.Client, execution_name_short: str) -> str:
    """
    Retrieves and concatenates the STDOUT log messages for a given execution.

    Args:
        logging_client: An authenticated Cloud Logging client.
        execution_name_short: The short name (ID) of the execution.

    Returns:
        A single string containing all STDOUT log payloads.
    """
    log_filter = (
        f'resource.type="cloud_run_job" '
        f'resource.labels.job_name="{JOB_NAME}" '
        f'labels."run.googleapis.com/execution_name"="{execution_name_short}"'
    )

    log_status("Fetching final results and logs...")
    entries = logging_client.list_entries(filter_=log_filter)  # type: ignore

    messages = [entry.payload for entry in entries if isinstance(entry.payload, str)]  # type: ignore
    return "".join(messages)


def main() -> None:
    """Main execution flow."""
    ar_client = artifactregistry_v1.ArtifactRegistryClient()
    run_client = run_v2.JobsClient()
    executions_client = run_v2.ExecutionsClient()
    tasks_client = run_v2.TasksClient()
    logging_client = logging_v2.Client(project=GCP_PROJECT_ID)

    proxy_image_name = setup_artifact_registry(ar_client)
    deploy_job(run_client, proxy_image_name)
    execution_details = run_and_wait_for_job(run_client, executions_client)
    execution_name_short = execution_details.name.split("/")[-1]
    container_output_str = get_job_logs(logging_client, execution_name_short)

    # To get the exit code, we must list the tasks for the completed execution
    # and then get the full details of the first task.
    tasks_list = list(tasks_client.list_tasks(parent=execution_details.name))  # type: ignore
    exit_code = None
    if tasks_list:
        task_name = tasks_list[0].name
        task_details = tasks_client.get_task(name=task_name)  # type: ignore
        # The exit code is on the `last_attempt_result` of the full task details.
        if task_details.last_attempt_result:
            exit_code = task_details.last_attempt_result.exit_code

    final_condition = execution_details.conditions[-1]
    status = (
        "Succeeded"
        if final_condition.state == final_condition.State.CONDITION_SUCCEEDED
        else "Failed"
    )

    container_output_json: Dict[str, Any]
    try:
        if not container_output_str:
            container_output_json = {}
        else:
            container_output_json = json.loads(container_output_str)
    except (json.JSONDecodeError, TypeError):
        log_status("Warning: Container output was not valid JSON. Wrapping raw output.")
        container_output_json = {"raw_output": container_output_str}

    final_result = {  # type: ignore
        "container_output": container_output_json,
        "metadata": {
            "task_id": execution_name_short,
            "status": status,
            "exit_code": exit_code,
            "created_at": execution_details.create_time.isoformat(),  # type: ignore
            "ended_at": execution_details.completion_time.isoformat(),  # type: ignore
        },
    }

    print(json.dumps(final_result, indent=2))


if __name__ == "__main__":
    main()
