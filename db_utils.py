from pymongo import MongoClient
from datetime import datetime
from config import MONGO_URI, DB_NAME

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

def get_kpi_data(date):
    date_start = f"{date}T00:00:00Z"
    date_end = f"{date}T23:59:59Z"
    date_range = {"$gte": date_start, "$lt": date_end}

    try:
        cursor = db.call_session_histories.aggregate([
            {"$match": {"created_at": date_range}},
            {"$group": {
                "_id": None,
                "avg_response_time": {"$avg": "$assistant_response_time"}
            }}
        ])
        avg_time = next(cursor, {"avg_response_time": 0})["avg_response_time"]
    except Exception:
        avg_time = 0

    return {
        "new_visitors": db.users.count_documents({"created_at": date_range}),
        "new_signups": db.users.count_documents({"created_at": date_range}),
        "signups_with_demo_calls": db.users.count_documents({
            "created_at": date_range,
            "has_demo_call": True
        }),
        "total_demo_calls": db.call_session_histories.count_documents({
            "created_at": date_range,
            "campaignId": "demo"
        }),
        "total_campaign_calls": db.call_session_histories.count_documents({
            "created_at": date_range
        }),
        "subscriptions_canceled": db.subscriptions.count_documents({
            "canceled_at": date_range
        }),
        "new_subscriptions": db.subscriptions.count_documents({
            "created_at": date_range
        }),
        "total_active_subscriptions": db.subscriptions.count_documents({
            "status": {"$in": [
                "Trial Monthly", "Trial Yearly", 
                "Starter Monthly", "Starter Yearly",
                "Growth Monthly", "Growth Yearly",
                "Elite Monthly", "Elite Yearly"
            ]}
        }),
        "calls_without_errors": db.call_session_histories.count_documents({
            "created_at": date_range,
            "error": None
        }),
        "calls_connected": db.call_session_histories.count_documents({
            "created_at": date_range,
            "status": "connected"
        }),
        "calls_longer_than_29_sec": db.call_session_histories.count_documents({
            "created_at": date_range,
            "duration": {"$gt": 29}
        }),
        "average_assistant_response_time": round(avg_time, 2)
    }