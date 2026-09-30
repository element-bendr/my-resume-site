# Promotion Record

date: YYYY-MM-DD
status: promoted
source_repository: <owner/repo>
destination_repository: <owner/repo>
source_record: <repository-relative path>
destination_record: <repository-relative path or issue/PR>
promotion_commit: <destination commit SHA when known, otherwise unknown>

## What moved

<concise description of authoritative material promoted>

## Authority change

From this promotion onward, the destination repository is authoritative for the promoted project-specific material.

This record remains only as a historical pointer and must not compete with destination canon.

## Source state retained here

- source context needed for traceability;
- this promotion pointer.

## Validation

Local validation may confirm required fields, source existence, and explicit authority transfer.
Remote validation must separately confirm the destination repository/record and promoted material using an appropriate connector/tool.
Never infer remote existence from this local record alone.
