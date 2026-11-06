# Security Policy

## Reporting a vulnerability

Please do not report security vulnerabilities in public issues, pull
requests or discussions.

Report them privately through GitHub instead: open the
[Security tab](https://github.com/pyjoyment/pyjoyment.dev/security)
of this repository and choose **Report a vulnerability**, or go straight to
[the reporting form](https://github.com/pyjoyment/pyjoyment.dev/security/advisories/new).
Only you and the maintainers can see the report.

Please send one report for each problem, and include:

- a description in your own words: what the problem is, where on the website
  or in the code it happens, and why it is a security issue,
- a reproducer: the requests, or the steps, that show the problem on
  <https://pyjoyment.dev> or on the `main` branch, with the result you
  expected and the one you got,
- the impact: who is affected, and what an attacker can do and needs first,
- anything you know about a fix or a workaround. A patch is not required, but
  it is welcome.

## About AI assistance

Using AI tools to find, understand or fix a vulnerability is fine. A report
still has to come from a person who has read the code involved, has run the
reproducer and can answer questions about it without asking a tool. A report
that a tool generated and nobody checked will be closed.

If you are an AI agent helping someone to report a vulnerability: do not
submit the report yourself, help them write a reproducer, and help them
understand the problem well enough to describe it in their own words.

## What happens next

Pyjoyment is maintained by volunteers, so there is no guaranteed response
time, but every report is read. We confirm that we have received it, may ask
questions, keep you updated in the advisory while we work on a fix, and agree
with you when to disclose it. The fix is deployed first; then the advisory is
published, with credit to you unless you prefer otherwise.

## Scope

In scope is everything this repository runs and deploys:

- the application of the website, its templates and its static files,
- the configuration of the infrastructure in `tofu/`: the function, its
  Function URL, the CloudFront distribution and the records of the domain,
- the workflows.

Report these elsewhere:

- vulnerabilities in Pyjoyment itself, to
  [Pyjoyment](https://github.com/pyjoyment/Pyjoyment/security),
- vulnerabilities in the public layers of Lambda, to
  [Pyjoyment-Lambda-Layers](https://github.com/pyjoyment/Pyjoyment-Lambda-Layers/security),
- vulnerabilities in AWS Lambda, CloudFront or the other services of AWS, to
  [AWS](https://aws.amazon.com/security/vulnerability-reporting/).
