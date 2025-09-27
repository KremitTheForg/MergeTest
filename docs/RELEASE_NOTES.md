# Release Notes

## Authentication Hardening

- Login attempts now treat malformed password hashes as invalid credentials rather than raising an error. Accounts that were created with unhashed passwords should be recreated so that bcrypt hashes are stored correctly. Operators should update affected records by resetting the password through the admin workflow or recreating the user account.
