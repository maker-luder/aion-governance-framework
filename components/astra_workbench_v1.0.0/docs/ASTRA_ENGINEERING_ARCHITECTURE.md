# Astra Engineering Workbench Architecture

`v1.0.0 candidate` is a new boundary, not a rename of Astra Engineering Assistant 0.3.0.

Flow: task intake → scope lock → Owner approval → isolated candidate copy → approved file/command operations → impact-based validation → rollback or package → Owner handoff → stop.

The baseline is read-only, the candidate is writable only with a task-bound unexpired grant, and output is package-only. No module performs deployment, canonical promotion, automatic cloud access, automatic external submission, or active-core self-modification.
