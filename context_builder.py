def build_context(results):
    context_parts = []

    for result in results:
        context_parts.append(
            result["text"]
        )

    return "\n\n".join(context_parts)