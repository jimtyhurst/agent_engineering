# class-02B: Student notes

## parent_and_subagents

### Error in the `save_attractions_to_state` tool

When a new attraction is added, all the other previous attractions are also added again to the list.

This line keeps adding the previous attractions into the state, causing duplicates:
```python
tool_context.state["attractions"] = existing_attractions + attractions
```

This revised version of the function worked for me, using sets to avoid duplicates, although the ToolContext value must be a list, in order to be JSON-serializable:
```python
def save_attractions_to_state(
    tool_context: ToolContext,
    attractions: set[str],
) -> dict[str, str]:
    """Save new attractions in the session state's attractions list."""
    existing_attractions = set(tool_context.state.get("attractions", []))
    tool_context.state["attractions"] = list(existing_attractions.union(attractions))
    return {"status": "success"}
```

### GOOGLE_CLOUD_PROJECT

I was using the Google Gemini API, using my personalized settings for `.env.api-key.example`. The original form of that file does not specify a `GOOGLE_CLOUD_PROJECT`, which means you use the free tier. I used my quota of tokens very quickly before completing the assignment.

The fix was to specify a project that is associated with a billing account. When I set the `GOOGLE_CLOUD_PROJECT` to one of my cloud projects, the agent was able to run without errors. Of course, I am no longer operating in the free tier, so I will be billed for my usage of the Gemini API.
