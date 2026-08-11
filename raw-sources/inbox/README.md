# Inbox

Drop zone for anything not yet ingested. Files here are read once by `/ingest`, then moved to `raw-sources/archive/` — never edited in place.

No naming convention or frontmatter required — that's the point of an inbox. But for YouTube transcripts specifically, use this shape so ingest has enough context to cite the source properly:

```markdown
# <Video Title>

Source: <YouTube URL>
Channel: <channel name, if known>
Captured: YYYY-MM-DD

## Transcript

<pasted transcript text>
```

This file itself is not a source — delete or ignore it; it won't be ingested.
