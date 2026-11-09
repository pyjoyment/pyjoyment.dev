# The JUnit XML in the place of the usual output
pyjo-prove -l --formatter junit -r t > report.xml

# Both, and the summary in Markdown, as of a job of GitHub Actions
pyjo-prove -l --capture-stderr --formatter console --formatter junit=report.xml --formatter markdown=summary.md -r t

# A test script is a test suite, and each of its tests a test case, also a subtest, which fails with its TAP and the
# line of the failed test inside it
xmllint --xpath '//testcase[failure]/@line' report.xml
