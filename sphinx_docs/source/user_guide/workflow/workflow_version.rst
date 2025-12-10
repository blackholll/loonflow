Workflow Version Management
===========================

Loonflow supports multiple workflow versions. Each workflow can have the
following version types:

- **default**: The active version used when a user selects the workflow in
  Workbench to create a new ticket.
- **candidate**: A draft version for validation. Administrators can switch the
  version type or create test tickets with the candidate version.
- **archived**: A retired version. New tickets cannot be created with it, but
  existing tickets created in the past can still be processed.

  .. figure:: ../../images/workflow_version_management.png
    :width: 100%
    :align: center
    :alt: workflow version management
