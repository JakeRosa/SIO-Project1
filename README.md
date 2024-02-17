# DETI Memorabilia - 1º SIO Project - Group 32

## Members of the group

| Nmec | Name | Email | Github |
| --- | --- | --- | --- |
| 107849 | Alexandre Cotorobai | <alexandrecotorobai@ua.pt> | [AlexandreCotorobai](https://github.com/AlexandreCotorobai) |
| 108215 | Hugo Correia | <hf.correia@ua.pt> |   [MrLoydHD](https://github.com/MrLoydHD) |
| 109089 | Joaquim Rosa | <joaquimvr15@ua.pt> | [JakeRosa](https://github.com/JakeRosa) |
| 108073 | Bernardo Figueiredo | <bernardo.figueiredo@ua.pt> | [LeikRad](https://github.com/LeikRad) |

<br>

## Project description

The DETI memorabilia is a web service that allows the common user to view various products offered by DETI, as well as their own merchandise and more specialized materials for everyday university life without the need to log in. The user can also add products to the shopping cart and, if logged in, proceed to checkout. If they only want to save products for a future purchase, they can always add them to their wish list. A logged-in user can also view their profile, edit their personal information, and see their purchase history. The administrator can edit products, including stock updates when necessary.

<br>

## Running the project

To run both applications simultaneously, simply execute the following command in the project's root folder:

```bash
docker-compose up --build # --build only if it's the first time you're running the command
```

To run only one of the applications, just run the same command with a slight adjustment:

```bash
docker-compose up --build (api_unsec | api_sec) # --build only if it's the first time you're running the command
```

Please note that `(api_unsec | api_sec)` is a placeholder for the specific application you want to run, and you should replace it with the actual name of the application you want to start (e.g., "api_unsec" or "api_sec").

<br>

## Vulnerabilities find and fixed

* [CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')](https://cwe.mitre.org/data/definitions/79.html)
* [CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')](https://cwe.mitre.org/data/definitions/89.html)
* [CWE-522: Insufficiently Protected Credentials](https://cwe.mitre.org/data/definitions/522.html)
* [CWE-521: Weak Password Requirements](https://cwe.mitre.org/data/definitions/521.html)
* [CWE-257: Storing Passwords in a Recoverable Format](https://cwe.mitre.org/data/definitions/257.html)
* [CWE-256: Unprotected Storage of Credentials](https://cwe.mitre.org/data/definitions/256.html)
* [CWE-311: Missing Encryption of Sensitive Data](https://cwe.mitre.org/data/definitions/311.html)
* [CWE-200: Exposure of Sensitive Information to an Unauthorized Actor](https://cwe.mitre.org/data/definitions/200.html)
* [CWE-434: Unrestricted Upload of File with Dangerous Type](https://cwe.mitre.org/data/definitions/434.html)
* [CWE-20: Improper Input Validation](https://cwe.mitre.org/data/definitions/20.html)
* [CWE-620: Unverified Password Change](https://cwe.mitre.org/data/definitions/620.html)
* [CWE-352: Cross-Site Request Forgery (CSRF)](https://cwe.mitre.org/data/definitions/352.html)

## Disclaimer regarding the demonstration videos

The demonstration videos showcasing the vulnerability exploits are not viewable in the PDF document because it does not support video embedding. They can, however, be viewed by clicking on the links below the respective "video". The videos are also available in the [videos](/analysis/videos/) folder of the project.
