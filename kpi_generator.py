import json
import os
from datetime import datetime, timedelta
from db_utils import get_kpi_data
from slack_integration import post_to_slack
from config import DATE_FORMAT

def load_daily_kpi():
    if os.path.exists('daily_kpi.json'):
        with open('daily_kpi.json', 'r') as f:
            return json.load(f)
    return {}

def save_daily_kpi(data):
    with open('daily_kpi.json', 'w') as f:
        json.dump(data, f, indent=2)

def calculate_kpi(date):
    daily_kpi = load_daily_kpi()
    kpi_data = get_kpi_data(date)
    
    previous_date = (datetime.strptime(date, DATE_FORMAT) - timedelta(days=1)).strftime(DATE_FORMAT)
    previous_kpi = daily_kpi.get(previous_date, {})
    
    kpi = {k: v for k, v in kpi_data.items()}
    
    # Calculate comparisons
    for key in kpi:
        if key in previous_kpi and previous_kpi[key] != 0:
            diff_percent = ((kpi[key] - previous_kpi[key]) / previous_kpi[key]) * 100
            if diff_percent > 0:
                kpi[f"{key}_comparison"] = f"{round(abs(diff_percent), 2)}% more than previous"
            elif diff_percent < 0:
                kpi[f"{key}_comparison"] = f"{round(abs(diff_percent), 2)}% less than previous"
            else:
                kpi[f"{key}_comparison"] = "No change from previous"
                
    daily_kpi[date] = kpi
    save_daily_kpi(daily_kpi)
    return kpi

def format_slack_message(kpi, date):
    return f"""*KPI Report for {date}*\n
*New Visitors*: {kpi['new_visitors']} ({kpi.get('new_visitors_comparison', 'N/A')})
*New Signups*: {kpi['new_signups']} ({kpi.get('new_signups_comparison', 'N/A')})
*Signups with Demo Calls*: {kpi['signups_with_demo_calls']} ({kpi.get('signups_with_demo_calls_comparison', 'N/A')})
*Total Demo Calls*: {kpi['total_demo_calls']} ({kpi.get('total_demo_calls_comparison', 'N/A')})
*Subscriptions Canceled*: {kpi['subscriptions_canceled']} ({kpi.get('subscriptions_canceled_comparison', 'N/A')})
*New Subscriptions*: {kpi['new_subscriptions']} ({kpi.get('new_subscriptions_comparison', 'N/A')})
*Total Active Subscriptions*: {kpi['total_active_subscriptions']} ({kpi.get('total_active_subscriptions_comparison', 'N/A')})
*Total Campaign Calls*: {kpi['total_campaign_calls']} ({kpi.get('total_campaign_calls_comparison', 'N/A')})
*Calls Without Errors*: {kpi['calls_without_errors']} of {kpi['total_campaign_calls']} calls
*Calls Connected*: {kpi['calls_connected']} of {kpi['calls_without_errors']} error-free calls
*Calls Longer Than 29 Sec*: {kpi['calls_longer_than_29_sec']} of {kpi['calls_connected']} connected calls
*Average Assistant Response Time*: {kpi['average_assistant_response_time']}s ({kpi.get('average_assistant_response_time_comparison', 'N/A')})"""

if __name__ == "__main__":
    yesterday = (datetime.now() - timedelta(days=1)).strftime(DATE_FORMAT)
    kpi = calculate_kpi(yesterday)
    message = format_slack_message(kpi, yesterday)
    if post_to_slack(message):
        print(f"KPI report for {yesterday} posted successfully")
    else:
        print(f"Failed to post KPI report for {yesterday}")