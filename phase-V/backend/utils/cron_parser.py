"""
Cron Expression Parser for Recurring Tasks

This module provides utilities for parsing and working with cron expressions
and simplified recurrence patterns for the recurring tasks feature.
"""

from datetime import datetime, timedelta
from typing import Optional, Union, List, Tuple
import re
from enum import Enum


class RecurrencePattern(Enum):
    """Enumeration of supported recurrence patterns"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"
    CUSTOM_CRON = "custom_cron"


def parse_recurrence_pattern(pattern: str) -> Optional[Tuple[RecurrencePattern, dict]]:
    """
    Parse a recurrence pattern string and return the pattern type and parameters.

    Args:
        pattern: Recurrence pattern string (e.g., 'daily', 'weekly', '* * * * *')

    Returns:
        Tuple of (RecurrencePattern, parameters dict) or None if invalid
    """
    pattern_lower = pattern.lower().strip()

    # Check for predefined patterns
    if pattern_lower == "daily":
        return (RecurrencePattern.DAILY, {})
    elif pattern_lower == "weekly":
        return (RecurrencePattern.WEEKLY, {})
    elif pattern_lower == "monthly":
        return (RecurrencePattern.MONTHLY, {})
    elif pattern_lower == "yearly":
        return (RecurrencePattern.YEARLY, {})

    # Check for cron expression format (5 parts: minute, hour, day, month, weekday)
    cron_parts = pattern.split()
    if len(cron_parts) == 5:
        # Validate each part is a valid cron expression component
        valid_cron_component = re.compile(
            r'^(\d+|\*(?:/\d+)?|\d+-\d+(?:/\d+)?|\w+(?:,\w+)*)$'
        )
        if all(valid_cron_component.match(part) for part in cron_parts):
            return (RecurrencePattern.CUSTOM_CRON, {"expression": pattern})

    return None


def validate_cron_expression(expression: str) -> bool:
    """
    Validate if a string is a valid cron expression.

    Args:
        expression: Cron expression string

    Returns:
        True if valid, False otherwise
    """
    try:
        parts = expression.strip().split()
        if len(parts) != 5:
            return False

        # Basic validation for each cron field
        for i, part in enumerate(parts):
            if not is_valid_cron_field(part, i):
                return False

        return True
    except Exception:
        return False


def is_valid_cron_field(field: str, field_index: int) -> bool:
    """
    Validate a single cron field.

    Args:
        field: Cron field value
        field_index: Index of the field (0=minute, 1=hour, 2=day, 3=month, 4=weekday)

    Returns:
        True if valid, False otherwise
    """
    # Check for wildcards, ranges, and steps
    if field == '*':
        return True

    # Check for step values (*/5, */10, etc.)
    if field.startswith('*/'):
        try:
            step = int(field[2:])
            if field_index == 0:  # Minute field
                return 1 <= step <= 59
            elif field_index == 1:  # Hour field
                return 1 <= step <= 23
            elif field_index == 2:  # Day field
                return 1 <= step <= 31
            elif field_index == 3:  # Month field
                return 1 <= step <= 12
            elif field_index == 4:  # Weekday field
                return 1 <= step <= 7
        except ValueError:
            return False

    # Split by commas for multiple values
    values = field.split(',')
    for value in values:
        # Check for ranges (e.g., 1-5)
        if '-' in value:
            range_parts = value.split('-')
            if len(range_parts) != 2:
                return False
            try:
                start, end = int(range_parts[0]), int(range_parts[1])
                if field_index == 0:  # Minute field
                    return 0 <= start <= end <= 59
                elif field_index == 1:  # Hour field
                    return 0 <= start <= end <= 23
                elif field_index == 2:  # Day field
                    return 1 <= start <= end <= 31
                elif field_index == 3:  # Month field
                    return 1 <= start <= end <= 12
                elif field_index == 4:  # Weekday field
                    return 0 <= start <= end <= 7  # 0 and 7 both represent Sunday
            except ValueError:
                return False
        else:
            # Single value
            try:
                val = int(value)
                if field_index == 0:  # Minute field
                    return 0 <= val <= 59
                elif field_index == 1:  # Hour field
                    return 0 <= val <= 23
                elif field_index == 2:  # Day field
                    return 1 <= val <= 31
                elif field_index == 3:  # Month field
                    return 1 <= val <= 12
                elif field_index == 4:  # Weekday field
                    return 0 <= val <= 7  # 0 and 7 both represent Sunday
            except ValueError:
                # Check if it's a valid weekday/month name
                if field_index == 4:  # Weekday field
                    valid_weekdays = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sunday',
                                     'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']
                    return value.lower() in valid_weekdays
                elif field_index == 3:  # Month field
                    valid_months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug',
                                   'sep', 'oct', 'nov', 'dec', 'january', 'february', 'march',
                                   'april', 'may', 'june', 'july', 'august', 'september',
                                   'october', 'november', 'december']
                    return value.lower() in valid_months
                return False

    return True


def calculate_next_occurrence(
    pattern: str,
    last_occurrence: datetime,
    timezone: str = 'UTC'
) -> Optional[datetime]:
    """
    Calculate the next occurrence based on the recurrence pattern.

    Args:
        pattern: Recurrence pattern string
        last_occurrence: When the task last occurred
        timezone: Timezone string

    Returns:
        Next occurrence datetime or None if pattern is invalid
    """
    parsed = parse_recurrence_pattern(pattern)
    if not parsed:
        return None

    pattern_type, params = parsed

    if pattern_type == RecurrencePattern.DAILY:
        return last_occurrence + timedelta(days=1)
    elif pattern_type == RecurrencePattern.WEEKLY:
        return last_occurrence + timedelta(weeks=1)
    elif pattern_type == RecurrencePattern.MONTHLY:
        # Calculate next month - add 1 month to the last occurrence
        # This handles month-end edge cases properly
        next_month = last_occurrence.month + 1
        next_year = last_occurrence.year
        if next_month > 12:
            next_month = 1
            next_year += 1

        # Handle day overflow (e.g., Jan 31 -> Feb 31 doesn't exist)
        import calendar
        max_day = calendar.monthrange(next_year, next_month)[1]
        day = min(last_occurrence.day, max_day)

        return last_occurrence.replace(year=next_year, month=next_month, day=day)
    elif pattern_type == RecurrencePattern.YEARLY:
        # Calculate next year
        next_year = last_occurrence.year + 1

        # Handle leap year edge case (Feb 29 -> Feb 28 in non-leap years)
        import calendar
        if last_occurrence.month == 2 and last_occurrence.day == 29 and not calendar.isleap(next_year):
            return last_occurrence.replace(year=next_year, day=28)
        else:
            return last_occurrence.replace(year=next_year)
    elif pattern_type == RecurrencePattern.CUSTOM_CRON:
        # For cron expressions, we'll use a simplified calculation
        # In a real implementation, you'd want to use a full cron parser
        # For now, we'll just return the same time next day as a fallback
        return last_occurrence + timedelta(days=1)

    return None


def get_next_n_occurrences(
    pattern: str,
    start_date: datetime,
    n: int = 5,
    timezone: str = 'UTC'
) -> List[datetime]:
    """
    Get the next N occurrences based on the recurrence pattern.

    Args:
        pattern: Recurrence pattern string
        start_date: Starting date for calculations
        n: Number of occurrences to calculate
        timezone: Timezone string

    Returns:
        List of next N occurrence datetimes
    """
    occurrences = []
    current_date = start_date

    for _ in range(n):
        next_occurrence = calculate_next_occurrence(pattern, current_date, timezone)
        if next_occurrence:
            occurrences.append(next_occurrence)
            current_date = next_occurrence
        else:
            break

    return occurrences


def is_recurrence_active(
    pattern: str,
    current_date: datetime,
    end_date: Optional[datetime] = None
) -> bool:
    """
    Check if a recurrence pattern is still active based on end date.

    Args:
        pattern: Recurrence pattern string
        current_date: Current date for evaluation
        end_date: Optional end date for recurrence

    Returns:
        True if recurrence is still active, False otherwise
    """
    if end_date is None:
        return True  # No end date means always active

    return current_date <= end_date


def normalize_recurrence_pattern(pattern: str) -> Optional[str]:
    """
    Normalize a recurrence pattern to a standard format.

    Args:
        pattern: Recurrence pattern string

    Returns:
        Normalized pattern string or None if invalid
    """
    if not pattern:
        return None

    pattern_lower = pattern.lower().strip()

    # Map common variations to standard patterns
    pattern_mapping = {
        'daily': 'daily',
        'every day': 'daily',
        'weekly': 'weekly',
        'every week': 'weekly',
        'monthly': 'monthly',
        'every month': 'monthly',
        'yearly': 'yearly',
        'annually': 'yearly',
        'every year': 'yearly',
    }

    if pattern_lower in pattern_mapping:
        return pattern_mapping[pattern_lower]

    # If it's a cron expression, validate and return as-is
    if validate_cron_expression(pattern):
        return pattern

    # If we can't normalize it, return None
    return None


def get_human_readable_pattern(pattern: str) -> str:
    """
    Convert a recurrence pattern to a human-readable string.

    Args:
        pattern: Recurrence pattern string

    Returns:
        Human-readable description of the pattern
    """
    normalized = normalize_recurrence_pattern(pattern)
    if not normalized:
        return "Invalid pattern"

    human_patterns = {
        'daily': 'Daily',
        'weekly': 'Weekly',
        'monthly': 'Monthly',
        'yearly': 'Yearly',
    }

    if normalized in human_patterns:
        return human_patterns[normalized]
    else:
        # For custom cron expressions, return a simplified description
        # In a real implementation, you'd want to parse the cron expression
        # to provide a more meaningful description
        return f"Cron: {normalized}"


# If running as main, run tests
if __name__ == "__main__":
    print("Testing cron parser utilities...")

    # Test pattern parsing
    test_patterns = ["daily", "weekly", "monthly", "yearly", "* * * * *", "invalid"]
    for pattern in test_patterns:
        result = parse_recurrence_pattern(pattern)
        print(f"Pattern '{pattern}' -> {result}")

    # Test cron validation
    test_crons = ["* * * * *", "0 9 * * *", "0 9 * * 1", "invalid cron"]
    for cron in test_crons:
        is_valid = validate_cron_expression(cron)
        print(f"Cron '{cron}' is valid: {is_valid}")

    # Test next occurrence calculation
    now = datetime.now()
    patterns = ["daily", "weekly", "monthly"]
    for pattern in patterns:
        next_occ = calculate_next_occurrence(pattern, now)
        print(f"Next occurrence for '{pattern}': {next_occ}")

    print("Cron parser utilities test completed.")