from strategy.context import MotorProcessor
from strategy.occ_mundial_strategy import OccMundialStrategy

JOB_TITLE = "python"
JOB_LOCATION = "Mexico"
OCC_MOTOR = "https://www.occ.com.mx"


occ_strategy = OccMundialStrategy(
    job_title=JOB_TITLE,
    job_location=JOB_LOCATION
    )
motor_processor = MotorProcessor(strategy=occ_strategy, url=OCC_MOTOR)
motor_processor.search_job()
