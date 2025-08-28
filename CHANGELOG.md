# Change Log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [0.0.9] - 2022-05-10

### Changed

- Resources and Destinations must now be imported using their full path.
- Tests can now be run with a single command. See README for details.

## [0.0.10] - 2022-05-24

### Added

- Added pre-commit and pre-commit hooks for Black

## [0.0.11] - 2022-07-25

### Added

- Added option to pass a manual schema to GCP Destination from a JSON Resource

## [0.0.12] - 2022-08-09

### Added

- Bug fix for manual schema option

## [0.0.13] - 2022-08-17

### Added

- Support manual schema option for CSVResource
- Support custom Hive paths for CSVResource

## [0.0.14] - 2022-09-22

### Added

- Add py.typed marker so that dependent libraries can use type vestapol type annotations

## [0.0.15] - 2022-09-28

### Removed

- Removed functionality that creates a header metadata file for `CSVResource`s
- Removed the `has_header` parameter for `CSVResource`s

### Fixed
- Fixed a bug where the BigQuery external table would ignore the first row of all CSV data, even if the data did not contain a header row.

### Added
- Added an optional `skip_leading_rows` parameter to `CSVResource` to specify andinteger indicating the number of header rows in the source data.

## [0.0.16] - 2022-09-29

### Fixed
- Fixed issue where an invalid `None` value could be passed to the `skip_leading_rows` parameter

## [0.0.17] - 2022-10-17

### Added
- Added support for deeply nested manual schemans in `gcp_destination`.

## [0.0.18] - 2022-10-24

### Fixed
- Fixed a bug where the `skip_leading_rows` parameter in  `csv_resource` was not being passed to the base class.


## [0.0.22] - 2023-10-23
- Added support for specifying delimiter in csv files in `CSVResource`
- Added support for allowing quoted newlines in csv files in `CSVResource`

## [0.0.23] - 2023-12-22
- Updated the `manual_schema` parameter in `CSVResource` to use the Optional type

## [0.0.24] - 2024-03-07
- Updated the parameter data type in write_list (json_resource class)

## [0.0.26] - 2024-04-29
- Updated the parameter data type in write_list (json_resource class)

## [0.0.27] - 2025-08-28
- Updated external_tables.py to set allow_jagged_rows to true