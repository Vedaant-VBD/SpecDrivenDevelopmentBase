# Capability: reports

## Purpose

The Reports capability lets a user fetch, filter, sort, and paginate the report dataset.
Internal-only fields (`internal_id`, `owner_email`) MUST NEVER appear in any user-facing
response.

## Requirements

### Requirement: List reports as JSON
THE system SHALL expose `GET /reports` returning a paginated JSON list of reports.

#### Scenario: default pagination
- **WHEN** the user calls `GET /reports` with no query parameters
- **THEN** the response SHALL contain at most 20 items
- **AND** the response SHALL include `total`, `offset`, and `limit`

#### Scenario: filter by status
- **WHEN** the user passes `?status=approved`
- **THEN** every returned item SHALL have `status` equal to `approved`

#### Scenario: filter by date range
- **WHEN** the user passes `?date_from=` and/or `?date_to=`
- **THEN** every returned item SHALL have `created_at` within the (inclusive) range

#### Scenario: sort
- **WHEN** the user passes `?sort=<field>&descending=<bool>`
- **THEN** items SHALL be sorted by that field in the requested direction
- **AND** if `<field>` is not a permitted sort field, the response SHALL be HTTP 400

### Requirement: Internal fields are never exposed
THE system SHALL never include `internal_id` or `owner_email` in any user-facing response.

#### Scenario: omitted from JSON
- **WHEN** the user receives any `/reports` response
- **THEN** the JSON SHALL NOT contain `internal_id` or `owner_email`

### Requirement: Health endpoint
THE system SHALL expose `GET /health` returning `{"status": "ok"}` with HTTP 200.

#### Scenario: liveness probe
- **WHEN** the user calls `GET /health`
- **THEN** the response status SHALL be 200
- **AND** the response body SHALL equal `{"status": "ok"}`
