# v0.3.1

- Fixed bug that caused server to return 500 when given empty string for phone number
    - Given phone number now must be a valid American phone number
    - Formatting and non digit characters are ignored

# v0.3.0

- /mail route now uses CORS policy.

# v0.2.0

- Added ability to configure encrypted environment variables
- Service now connects to production data store

# v0.1.2-alpha

- Message max length is now 2000
- Fixed bug that did not allow for meaning information to be communicated when request body was used incorrectly.
- Fixed bug that was not applying correct created and update dates to newly created messages

# v0.1.1-alpha

- Sender alias max length is now 50

# v0.1.0-alpha
- Contact Message creation endpoint
