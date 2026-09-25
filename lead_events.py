from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, func


def register_lead_event_routes(app, Base, engine, get_db, Worker):
    class LeadEvent(Base):
        __tablename__ = "lead_events"
        id = Column(Integer, primary_key=True, index=True)
        worker_id = Column(Integer, nullable=False, index=True)
        route = Column(String, nullable=False, index=True)
        action = Column(String, nullable=False, index=True)
        created_at = Column(String, nullable=False, index=True)

    Base.metadata.create_all(bind=engine)

    class LeadEventIn(BaseModel):
        worker_id: int
        route: str
        action: str

    @app.post("/events/lead", status_code=201)
    def record_lead(data: LeadEventIn, db=Depends(get_db)):
        action = (data.action or "").strip().lower()
        route = (data.route or "").strip()

        if action not in ("call", "whatsapp"):
            raise HTTPException(400, "Unsupported lead action")
        if not route.startswith("/artisan/") or len(route) > 160:
            raise HTTPException(400, "Invalid directory route")

        worker = db.query(Worker).filter(Worker.id == data.worker_id).first()
        if not worker:
            raise HTTPException(404, "Worker not found")

        event = LeadEvent(
            worker_id=data.worker_id,
            route=route,
            action=action,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        db.add(event)
        db.commit()
        return {"ok": True}

    @app.get("/analytics/leads/summary")
    def lead_summary(days: int = 30, db=Depends(get_db)):
        days = min(max(days, 1), 365)
        since = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()
        rows = (
            db.query(LeadEvent.route, LeadEvent.action, func.count(LeadEvent.id))
            .filter(LeadEvent.created_at >= since)
            .group_by(LeadEvent.route, LeadEvent.action)
            .order_by(func.count(LeadEvent.id).desc())
            .all()
        )
        totals = {"call": 0, "whatsapp": 0}
        by_route = {}
        for route, action, count in rows:
            count = int(count)
            totals[action] = totals.get(action, 0) + count
            if route not in by_route:
                by_route[route] = {"call": 0, "whatsapp": 0, "total": 0}
            by_route[route][action] = by_route[route].get(action, 0) + count
            by_route[route]["total"] += count

        return {
            "days": days,
            "since": since,
            "total": sum(totals.values()),
            "by_action": totals,
            "by_route": [
                {"route": route, **counts}
                for route, counts in sorted(by_route.items(), key=lambda item: item[1]["total"], reverse=True)
            ],
        }
