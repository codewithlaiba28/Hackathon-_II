"""
Timezone Utility Functions for Advanced Todo Features

This module provides utilities for handling timezone conversions,
date parsing, and time-related operations for the advanced features.
"""

from datetime import datetime, timezone, timedelta
import pytz
from typing import Optional, Union
import re


def utc_now() -> datetime:
    """Get current time in UTC timezone."""
    return datetime.now(timezone.utc)


def convert_to_utc(local_datetime: datetime, local_tz_str: str = 'UTC') -> datetime:
    """
    Convert a local datetime to UTC.

    Args:
        local_datetime: The datetime object to convert
        local_tz_str: The timezone string (e.g., 'US/Eastern', 'Europe/London')

    Returns:
        datetime object in UTC timezone
    """
    if local_datetime.tzinfo is not None:
        # Already timezone-aware, convert to UTC
        return local_datetime.astimezone(timezone.utc)
    else:
        # Naive datetime, localize to the given timezone first
        local_tz = pytz.timezone(local_tz_str)
        localized_dt = local_tz.localize(local_datetime)
        return localized_dt.astimezone(timezone.utc)


def convert_from_utc(utc_datetime: datetime, target_tz_str: str = 'UTC') -> datetime:
    """
    Convert a UTC datetime to a target timezone.

    Args:
        utc_datetime: The UTC datetime object to convert
        target_tz_str: The target timezone string

    Returns:
        datetime object in the target timezone
    """
    if utc_datetime.tzinfo is None:
        # Make it timezone-aware as UTC first
        utc_datetime = utc_datetime.replace(tzinfo=timezone.utc)

    target_tz = pytz.timezone(target_tz_str)
    return utc_datetime.astimezone(target_tz)


def parse_natural_language_date(date_text: str, user_timezone: str = 'UTC') -> Optional[datetime]:
    """
    Parse natural language date expressions like "tomorrow 3pm", "next Monday".

    Args:
        date_text: Natural language date string
        user_timezone: User's timezone for conversion

    Returns:
        Parsed datetime object or None if parsing fails
    """
    date_text = date_text.lower().strip()
    now = datetime.now(pytz.timezone(user_timezone))

    # Handle "today" variations
    if 'today' in date_text:
        time_match = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)?', date_text)
        if time_match:
            hour, minute, period = time_match.groups()
            hour = int(hour)
            minute = int(minute)

            if period and period.lower() == 'pm' and hour != 12:
                hour += 12
            elif period and period.lower() == 'am' and hour == 12:
                hour = 0

            return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        else:
            # Just today, default to 5pm
            return now.replace(hour=17, minute=0, second=0, microsecond=0)

    # Handle "tomorrow" variations
    elif 'tomorrow' in date_text:
        tomorrow = now + timedelta(days=1)
        time_match = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)?', date_text)
        if time_match:
            hour, minute, period = time_match.groups()
            hour = int(hour)
            minute = int(minute)

            if period and period.lower() == 'pm' and hour != 12:
                hour += 12
            elif period and period.lower() == 'am' and hour == 12:
                hour = 0

            return tomorrow.replace(hour=hour, minute=minute, second=0, microsecond=0)
        else:
            # Just tomorrow, default to 9am
            return tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)

    # Handle "next" weekday
    elif 'next' in date_text:
        # Extract day of week
        days_map = {
            'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
            'friday': 4, 'saturday': 5, 'sunday': 6
        }

        for day_name, day_num in days_map.items():
            if day_name in date_text:
                # Find next occurrence of this day
                days_ahead = day_num - now.weekday()
                if days_ahead <= 0:  # Target day already happened this week
                    days_ahead += 7
                target_date = now + timedelta(days=days_ahead)

                time_match = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)?', date_text)
                if time_match:
                    hour, minute, period = time_match.groups()
                    hour = int(hour)
                    minute = int(minute)

                    if period and period.lower() == 'pm' and hour != 12:
                        hour += 12
                    elif period and period.lower() == 'am' and hour == 12:
                        hour = 0

                    return target_date.replace(hour=hour, minute=minute, second=0, microsecond=0)
                else:
                    # Default to 9am
                    return target_date.replace(hour=9, minute=0, second=0, microsecond=0)

    # Handle specific time formats (HH:MM)
    time_match = re.search(r'(\d{1,2}):(\d{2})\s*(am|pm)?', date_text)
    if time_match:
        hour, minute, period = time_match.groups()
        hour = int(hour)
        minute = int(minute)

        if period and period.lower() == 'pm' and hour != 12:
            hour += 12
        elif period and period.lower() == 'am' and hour == 12:
            hour = 0

        # If no date specified, assume today
        if not any(day in date_text for day in ['today', 'tomorrow'] + list(days_map.keys())):
            return now.replace(hour=hour, minute=minute, second=0, microsecond=0)

    # If no natural language patterns matched, try standard datetime parsing
    return None


def format_datetime_for_display(dt: datetime, user_timezone: str = 'UTC', fmt: str = '%Y-%m-%d %H:%M') -> str:
    """
    Format a datetime for display in user's timezone.

    Args:
        dt: The datetime object to format
        user_timezone: User's timezone
        fmt: Format string

    Returns:
        Formatted datetime string
    """
    if dt.tzinfo is None:
        # Assume UTC if not timezone-aware
        dt = dt.replace(tzinfo=timezone.utc)

    user_tz = pytz.timezone(user_timezone)
    local_dt = dt.astimezone(user_tz)
    return local_dt.strftime(fmt)


def is_overdue(dt: datetime, user_timezone: str = 'UTC') -> bool:
    """
    Check if a datetime is in the past (overdue).

    Args:
        dt: The datetime to check
        user_timezone: User's timezone for comparison

    Returns:
        True if the datetime is in the past, False otherwise
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    return dt < now


def calculate_reminder_time(due_date: datetime, offset_minutes: int) -> datetime:
    """
    Calculate the reminder time based on due date and offset.

    Args:
        due_date: The due date
        offset_minutes: Minutes before due date to send reminder

    Returns:
        The calculated reminder time
    """
    if due_date.tzinfo is None:
        due_date = due_date.replace(tzinfo=timezone.utc)

    return due_date - timedelta(minutes=offset_minutes)


def get_timezone_offset_minutes(tz_str: str) -> int:
    """
    Get the offset in minutes for a timezone.

    Args:
        tz_str: Timezone string (e.g., 'US/Eastern')

    Returns:
        Offset in minutes from UTC
    """
    tz = pytz.timezone(tz_str)
    now = datetime.now()
    local_time = tz.localize(now)
    utc_time = local_time.astimezone(timezone.utc)
    offset = utc_time - now
    return int(offset.total_seconds() // 60)


def validate_timezone(tz_str: str) -> bool:
    """
    Validate if a timezone string is valid.

    Args:
        tz_str: Timezone string to validate

    Returns:
        True if valid, False otherwise
    """
    try:
        pytz.timezone(tz_str)
        return True
    except Exception:
        return False


# If running as main, run tests
if __name__ == "__main__":
    # Test the functions
    print("Testing timezone utilities...")

    # Test current time
    now = utc_now()
    print(f"Current UTC time: {now}")

    # Test timezone conversion
    est_time = convert_from_utc(now, 'US/Eastern')
    print(f"Time in EST: {est_time}")

    # Test natural language parsing
    test_dates = ["tomorrow 3pm", "next Monday", "today 10:30 AM"]
    for date_str in test_dates:
        parsed = parse_natural_language_date(date_str, 'US/Eastern')
        if parsed:
            print(f"'{date_str}' -> {parsed}")
        else:
            print(f"'{date_str}' -> Could not parse")

    print("Timezone utilities test completed.")