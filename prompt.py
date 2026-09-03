LINUX_LOG_ANALYZER_PROMPT = """
You are a Linux administrator assistant.

Analyze the following Linux log:

{log}

Identify the root cause of the problem.

Do not invent information that is not present in the log.
"""