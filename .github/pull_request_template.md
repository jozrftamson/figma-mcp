name: Pull Request
description: Submit changes to the project
title: "[TYPE] Brief description"
labels: ["type/enhancement"]

body:
  - type: markdown
    attributes:
      value: |
        # Pull Request

        Thanks for contributing to Figma MCP Server! 🎉

  - type: textarea
    id: description
    attributes:
      label: Description
      description: Describe the changes you've made
      placeholder: What does this PR do?
    validations:
      required: true

  - type: textarea
    id: related_issues
    attributes:
      label: Related Issues
      description: Link to related issues (e.g., Fixes #123)
      placeholder: |
        Fixes #123
        Related to #456

  - type: checkboxes
    id: type
    attributes:
      label: Type of Change
      options:
        - label: New feature
        - label: Bug fix
        - label: Documentation update
        - label: Refactoring
        - label: Test addition
        - label: Breaking change

  - type: checkboxes
    id: testing
    attributes:
      label: Testing
      options:
        - label: Unit tests added/updated
        - label: Tested locally
        - label: No regressions

  - type: checkboxes
    id: checklist
    attributes:
      label: Checklist
      options:
        - label: Code follows style guidelines
        - label: Self-review completed
        - label: Comments added for complex logic
        - label: Documentation updated
        - label: Tests pass
        - label: No new warnings generated
      validations:
        required: true

  - type: markdown
    attributes:
      value: |
        ---
        **Thanks for contributing!** 🚀
