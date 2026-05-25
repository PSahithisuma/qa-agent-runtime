from fastapi import APIRouter
from fastapi import HTTPException

from src.db.database import SessionLocal
from src.models.test_run import TestRun

router = APIRouter()


@router.get("/runs")
async def get_runs():

    db = SessionLocal()

    try:

        runs = db.query(TestRun).all()

        results = []

        for run in runs:

            results.append({

                "id": run.id,

                "success": run.success,

                "framework": run.framework,

                "coverage": run.coverage
            })

        return results

    finally:

        db.close()


@router.get("/runs/{run_id}")
async def get_run(run_id: int):

    db = SessionLocal()

    try:

        run = db.query(TestRun).filter(
            TestRun.id == run_id
        ).first()

        if not run:

            raise HTTPException(
                status_code=404,
                detail="Run not found"
            )

        return {

            "id": run.id,

            "success": run.success,

            "framework": run.framework,

            "coverage": run.coverage,

            "logs": run.logs
        }

    finally:

        db.close()