"""
Google Analytics Data API Service
Fetches real-time and historical analytics data from Google Analytics 4
"""

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    RunRealtimeReportRequest
)
from google.oauth2 import service_account
from datetime import datetime, timedelta
import os

# Google Analytics Property ID
GA_PROPERTY_ID = "5161391734"  # Planet Fitness Resource Hub property

# Initialize the client
def get_analytics_client():
    """Create and return authenticated Analytics Data API client"""
    import json
    
    # Try to get credentials from environment variable (Render deployment)
    credentials_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS_JSON')
    
    if credentials_json:
        # Parse JSON from environment variable
        credentials_info = json.loads(credentials_json)
        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=['https://www.googleapis.com/auth/analytics.readonly']
        )
    else:
        # Fall back to local file for development
        credentials_path = os.path.join(os.path.dirname(__file__), 'ga-credentials.json')
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/analytics.readonly']
        )
    
    return BetaAnalyticsDataClient(credentials=credentials)


def get_date_range(range_type='30days'):
    """Convert range type to start/end dates"""
    today = datetime.now().date()
    
    ranges = {
        'today': (today, today),
        'yesterday': (today - timedelta(days=1), today - timedelta(days=1)),
        '7days': (today - timedelta(days=7), today),
        '30days': (today - timedelta(days=30), today),
        '90days': (today - timedelta(days=90), today),
    }
    
    # Handle month ranges
    if range_type == 'thisMonth':
        start = today.replace(day=1)
        return (start, today)
    elif range_type == 'lastMonth':
        last_month = today.replace(day=1) - timedelta(days=1)
        start = last_month.replace(day=1)
        end = last_month
        return (start, end)
    
    # Handle quarter ranges
    elif range_type == 'thisQuarter':
        quarter = (today.month - 1) // 3
        start = today.replace(month=quarter * 3 + 1, day=1)
        return (start, today)
    elif range_type == 'lastQuarter':
        quarter = (today.month - 1) // 3
        if quarter == 0:
            start = today.replace(year=today.year-1, month=10, day=1)
            end = today.replace(year=today.year-1, month=12, day=31)
        else:
            start = today.replace(month=(quarter-1) * 3 + 1, day=1)
            end = today.replace(month=quarter * 3, day=1) - timedelta(days=1)
        return (start, end)
    
    # Handle year ranges
    elif range_type == 'thisYear':
        start = today.replace(month=1, day=1)
        return (start, today)
    elif range_type == 'lastYear':
        start = today.replace(year=today.year-1, month=1, day=1)
        end = today.replace(year=today.year-1, month=12, day=31)
        return (start, end)
    
    # Handle all time
    elif range_type == 'allTime':
        start = datetime(2020, 1, 1).date()  # Adjust based on when your GA started
        return (start, today)
    
    return ranges.get(range_type, ranges['30days'])


def get_realtime_data():
    """Get real-time active users and activity"""
    try:
        client = get_analytics_client()
        
        request = RunRealtimeReportRequest(
            property=f"properties/{GA_PROPERTY_ID}",
            metrics=[
                Metric(name="activeUsers"),
            ],
        )
        
        response = client.run_realtime_report(request)
        
        active_users = 0
        if response.rows:
            active_users = int(response.rows[0].metric_values[0].value)
        
        return {
            'activeUsers': active_users,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        print(f"Error fetching realtime data: {e}")
        return {
            'activeUsers': 0,
            'error': str(e)
        }


def get_overview_stats(date_range='30days', start_date=None, end_date=None):
    """Get overview statistics for the dashboard"""
    try:
        client = get_analytics_client()
        
        # Get date range
        if start_date and end_date:
            start = start_date
            end = end_date
        else:
            start, end = get_date_range(date_range)
        
        request = RunReportRequest(
            property=f"properties/{GA_PROPERTY_ID}",
            date_ranges=[DateRange(
                start_date=start.strftime('%Y-%m-%d'),
                end_date=end.strftime('%Y-%m-%d')
            )],
            metrics=[
                Metric(name="activeUsers"),
                Metric(name="totalUsers"),
                Metric(name="screenPageViews"),
                Metric(name="sessions"),
                Metric(name="averageSessionDuration"),
            ],
        )
        
        response = client.run_report(request)
        
        if response.rows:
            row = response.rows[0]
            return {
                'activeUsers': int(row.metric_values[0].value),
                'totalUsers': int(row.metric_values[1].value),
                'pageViews': int(row.metric_values[2].value),
                'sessions': int(row.metric_values[3].value),
                'avgDuration': round(float(row.metric_values[4].value) / 60, 1),  # Convert to minutes
            }
        
        return {
            'activeUsers': 0,
            'totalUsers': 0,
            'pageViews': 0,
            'sessions': 0,
            'avgDuration': 0,
        }
    except Exception as e:
        print(f"Error fetching overview stats: {e}")
        return {
            'error': str(e),
            'activeUsers': 0,
            'totalUsers': 0,
            'pageViews': 0,
            'sessions': 0,
            'avgDuration': 0,
        }


def get_traffic_data(date_range='30days', start_date=None, end_date=None):
    """Get daily traffic data for chart"""
    try:
        client = get_analytics_client()
        
        # Get date range
        if start_date and end_date:
            start = start_date
            end = end_date
        else:
            start, end = get_date_range(date_range)
        
        request = RunReportRequest(
            property=f"properties/{GA_PROPERTY_ID}",
            date_ranges=[DateRange(
                start_date=start.strftime('%Y-%m-%d'),
                end_date=end.strftime('%Y-%m-%d')
            )],
            dimensions=[Dimension(name="date")],
            metrics=[
                Metric(name="totalUsers"),
                Metric(name="sessions"),
            ],
        )
        
        response = client.run_report(request)
        
        dates = []
        users = []
        sessions = []
        
        for row in response.rows:
            date_str = row.dimension_values[0].value
            # Format: YYYYMMDD to MMM DD
            date_obj = datetime.strptime(date_str, '%Y%m%d')
            dates.append(date_obj.strftime('%b %d'))
            users.append(int(row.metric_values[0].value))
            sessions.append(int(row.metric_values[1].value))
        
        return {
            'dates': dates,
            'users': users,
            'sessions': sessions,
        }
    except Exception as e:
        print(f"Error fetching traffic data: {e}")
        return {
            'error': str(e),
            'dates': [],
            'users': [],
            'sessions': [],
        }


def get_top_pages(date_range='30days', start_date=None, end_date=None):
    """Get most visited pages"""
    try:
        client = get_analytics_client()
        
        # Get date range
        if start_date and end_date:
            start = start_date
            end = end_date
        else:
            start, end = get_date_range(date_range)
        
        request = RunReportRequest(
            property=f"properties/{GA_PROPERTY_ID}",
            date_ranges=[DateRange(
                start_date=start.strftime('%Y-%m-%d'),
                end_date=end.strftime('%Y-%m-%d')
            )],
            dimensions=[Dimension(name="pagePath")],
            metrics=[
                Metric(name="screenPageViews"),
            ],
            order_bys=[{
                'metric': {'metric_name': 'screenPageViews'},
                'desc': True
            }],
            limit=10
        )
        
        response = client.run_report(request)
        
        pages = []
        total_views = sum(int(row.metric_values[0].value) for row in response.rows)
        
        for row in response.rows:
            page = row.dimension_values[0].value
            views = int(row.metric_values[0].value)
            percent = round((views / total_views * 100), 1) if total_views > 0 else 0
            
            pages.append({
                'page': page,
                'views': views,
                'percent': percent
            })
        
        return pages
    except Exception as e:
        print(f"Error fetching top pages: {e}")
        return []


def get_geographic_data(date_range='30days', start_date=None, end_date=None):
    """Get visitor locations"""
    try:
        client = get_analytics_client()
        
        # Get date range
        if start_date and end_date:
            start = start_date
            end = end_date
        else:
            start, end = get_date_range(date_range)
        
        request = RunReportRequest(
            property=f"properties/{GA_PROPERTY_ID}",
            date_ranges=[DateRange(
                start_date=start.strftime('%Y-%m-%d'),
                end_date=end.strftime('%Y-%m-%d')
            )],
            dimensions=[
                Dimension(name="country"),
                Dimension(name="region"),
            ],
            metrics=[
                Metric(name="totalUsers"),
                Metric(name="sessions"),
            ],
            order_bys=[{
                'metric': {'metric_name': 'totalUsers'},
                'desc': True
            }],
            limit=10
        )
        
        response = client.run_report(request)
        
        locations = []
        for row in response.rows:
            country = row.dimension_values[0].value
            region = row.dimension_values[1].value
            location = f"{region}, {country}" if region != '(not set)' else country
            
            locations.append({
                'location': location,
                'users': int(row.metric_values[0].value),
                'sessions': int(row.metric_values[1].value)
            })
        
        return locations
    except Exception as e:
        print(f"Error fetching geographic data: {e}")
        return []


def get_all_analytics_data(date_range='30days', start_date=None, end_date=None):
    """Get all analytics data in one call"""
    return {
        'realtime': get_realtime_data(),
        'overview': get_overview_stats(date_range, start_date, end_date),
        'traffic': get_traffic_data(date_range, start_date, end_date),
        'topPages': get_top_pages(date_range, start_date, end_date),
        'locations': get_geographic_data(date_range, start_date, end_date),
    }
