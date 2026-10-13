# [Return Records](https://www.fastprep.io/problems/amazon-return-records)

**Easy** | **NN minutes** | **Hash Table, Simulation, String**

Simulate a website authentication service. Initially, no users are registered and no user is logged in. Process each request in attempts from left to right.

Each request has one of these forms:

register username password: register a new username. Return "Registered Successfully", or "Register Unsuccessfully" if the username already exists.login username password: log in a registered user when the password matches and the user is not already logged in. Return "Logged In Successfully" on success, or "Login Unsuccessfully" otherwise.logout username: log out a currently logged-in user. Return "Logged Out Successfully" on success, or "Logout Unsuccessfully" otherwise.A failed login does not change an existing session. Usernames and passwords are case-sensitive.

Return one result string for every request, in the same order.

## Examples

### Example 1

**Input:** `attempts = ["register user05 qwerty", "login user05 qwerty", "logout user05"]`

**Output:** `["Registered Successfully", "Logged In Successfully", "Logged Out Successfully"]`

**Explanation:** The user is registered, then logs in with the matching password, and finally logs out. All three requests succeed.

### Example 2

**Input:** `attempts = ["register david david123", "register adam 1Adam1", "login david david123", "login adam 1adam1", "logout david"]`

**Output:** `["Registered Successfully", "Registered Successfully", "Logged In Successfully", "Login Unsuccessfully", "Logged Out Successfully"]`

**Explanation:** david and adam are new usernames, so both registrations succeed.david logs in with the correct password.adam uses 1adam1, which does not match the case-sensitive password 1Adam1, so that login fails.david is logged in, so the logout succeeds.

## Constraints

- `1 <= attempts.length <= 100000`
- `1 <= username.length, password.length <= 10`
- `Usernames and passwords contain only digits and English letters.`
- `Every request has one of the three documented formats.`

## Solutions

<!-- Scaffold placeholder: the worked derivation and write-up land
     on main later. See ../../leetcode/_TEMPLATE.md for the
     expected layout, naming, and ordering conventions. -->
