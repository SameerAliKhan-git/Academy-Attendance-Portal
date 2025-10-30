# API Documentation - Academy Attendance Portal

## Overview
This document describes the integration points between the Flask web dashboard (Team B) and the backend API (Team A).

## Base URL
```
http://localhost:5001/api  # Development
https://api.yourdomain.com/api  # Production
```

Configure via `BACKEND_API_URL` environment variable.

---

## Authentication
Currently using session-based authentication from Flask-Login. Future versions may implement token-based API authentication.

---

## Endpoints

### 1. Get Attendance Summary

**Endpoint**: `GET /attendance/{student_id}`

**Description**: Retrieves attendance summary for a specific student.

**Parameters**:
- `student_id` (path) - Student identifier

**Response** (200 OK):
```json
{
  "student_id": "CS001",
  "percentage": 85.5,
  "total_days": 100,
  "present_days": 85,
  "absent_days": 15,
  "last_updated": "2025-10-30T10:30:00Z"
}
```

**Usage in Dashboard**:
```python
import requests
from flask import current_app

def fetch_attendance_data(student_id):
    api_url = current_app.config['BACKEND_API_URL']
    response = requests.get(f'{api_url}/attendance/{student_id}', timeout=5)
    if response.status_code == 200:
        return response.json()
    return None
```

---

### 2. Get Attendance Logs

**Endpoint**: `GET /attendance/{student_id}/logs`

**Description**: Retrieves detailed attendance records for a student.

**Parameters**:
- `student_id` (path) - Student identifier
- `start_date` (query, optional) - Filter from date (YYYY-MM-DD)
- `end_date` (query, optional) - Filter to date (YYYY-MM-DD)
- `limit` (query, optional) - Number of records (default: 100)

**Response** (200 OK):
```json
{
  "student_id": "CS001",
  "logs": [
    {
      "date": "2025-10-30",
      "day": "Thursday",
      "status": "present",
      "time_in": "08:45:00",
      "time_out": "15:30:00",
      "remarks": "On time"
    },
    {
      "date": "2025-10-29",
      "day": "Wednesday",
      "status": "absent",
      "time_in": null,
      "time_out": null,
      "remarks": "Medical leave"
    }
  ],
  "total_records": 2
}
```

**Usage in Dashboard**:
```python
def fetch_attendance_logs(student_id, start_date=None, end_date=None):
    api_url = current_app.config['BACKEND_API_URL']
    params = {}
    if start_date:
        params['start_date'] = start_date
    if end_date:
        params['end_date'] = end_date
    
    response = requests.get(
        f'{api_url}/attendance/{student_id}/logs',
        params=params,
        timeout=5
    )
    if response.status_code == 200:
        return response.json().get('logs', [])
    return []
```

---

### 3. Mark Attendance (Teacher)

**Endpoint**: `POST /attendance/mark`

**Description**: Mark attendance for students (teacher/admin only).

**Request Body**:
```json
{
  "student_id": "CS001",
  "date": "2025-10-30",
  "status": "present",
  "time_in": "08:45:00",
  "remarks": "On time"
}
```

**Response** (201 Created):
```json
{
  "success": true,
  "message": "Attendance marked successfully",
  "record_id": 12345
}
```

**Usage in Dashboard**:
```python
def mark_attendance(student_id, status, remarks=None):
    api_url = current_app.config['BACKEND_API_URL']
    data = {
        'student_id': student_id,
        'date': datetime.now().strftime('%Y-%m-%d'),
        'status': status,
        'time_in': datetime.now().strftime('%H:%M:%S'),
        'remarks': remarks
    }
    response = requests.post(
        f'{api_url}/attendance/mark',
        json=data,
        timeout=5
    )
    return response.status_code == 201
```

---

### 4. Get Department Students

**Endpoint**: `GET /departments/{dept_id}/students`

**Description**: Retrieve list of students in a department.

**Parameters**:
- `dept_id` (path) - Department identifier
- `active_only` (query, optional) - Filter active students (default: true)

**Response** (200 OK):
```json
{
  "department_id": 1,
  "department_name": "Computer Science",
  "students": [
    {
      "student_id": "CS001",
      "full_name": "John Doe",
      "email": "john@example.com",
      "enrollment_date": "2024-09-01"
    }
  ],
  "total_students": 1
}
```

---

### 5. Get Attendance Statistics

**Endpoint**: `GET /attendance/statistics`

**Description**: Get system-wide attendance statistics (admin only).

**Response** (200 OK):
```json
{
  "overall_percentage": 87.5,
  "total_students": 500,
  "present_today": 450,
  "absent_today": 50,
  "departments": [
    {
      "department_name": "Computer Science",
      "attendance_percentage": 90.5,
      "student_count": 150
    }
  ]
}
```

---

## Error Responses

All endpoints may return the following error responses:

**400 Bad Request**:
```json
{
  "error": "Bad Request",
  "message": "Invalid student_id format"
}
```

**404 Not Found**:
```json
{
  "error": "Not Found",
  "message": "Student not found"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Internal Server Error",
  "message": "Database connection failed"
}
```

---

## Error Handling in Dashboard

```python
def safe_api_call(url, method='GET', **kwargs):
    """Wrapper for safe API calls with error handling."""
    try:
        if method == 'GET':
            response = requests.get(url, timeout=5, **kwargs)
        elif method == 'POST':
            response = requests.post(url, timeout=5, **kwargs)
        
        response.raise_for_status()
        return response.json()
    except requests.Timeout:
        flash('Request timeout. Please try again.', 'warning')
        return None
    except requests.ConnectionError:
        flash('Cannot connect to backend API.', 'danger')
        return None
    except requests.HTTPError as e:
        flash(f'API Error: {e.response.status_code}', 'danger')
        return None
    except Exception as e:
        flash(f'Unexpected error: {str(e)}', 'danger')
        return None
```

---

## Rate Limiting

The API may implement rate limiting:
- **Student/Parent**: 100 requests per hour
- **Teacher**: 500 requests per hour
- **Admin**: 1000 requests per hour

Response headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1635600000
```

---

## Pagination

For endpoints returning lists, pagination is supported:

**Query Parameters**:
- `page` (integer, default: 1)
- `per_page` (integer, default: 50, max: 100)

**Response**:
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 50,
    "total_pages": 5,
    "total_items": 250
  }
}
```

---

## Testing API Integration

```python
# test_api_integration.py
import unittest
from app import create_app

class APIIntegrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        self.app_context.pop()
    
    def test_fetch_attendance_data(self):
        """Test attendance data retrieval."""
        data = fetch_attendance_data('CS001')
        self.assertIsNotNone(data)
        self.assertIn('percentage', data)
    
    def test_fetch_attendance_logs(self):
        """Test attendance logs retrieval."""
        logs = fetch_attendance_logs('CS001')
        self.assertIsInstance(logs, list)

if __name__ == '__main__':
    unittest.main()
```

---

## Future API Enhancements

Planned for future versions:
- JWT-based authentication
- WebSocket support for real-time updates
- Bulk attendance marking
- CSV export endpoints
- Parent-student linking API
- Notification system integration

---

## Support

For API-related issues:
- **Team A**: Backend API development
- **Team B**: Dashboard integration

**Last Updated**: October 30, 2025
