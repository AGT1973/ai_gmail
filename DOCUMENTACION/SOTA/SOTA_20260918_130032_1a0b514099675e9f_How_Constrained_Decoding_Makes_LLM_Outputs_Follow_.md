# 🧠 INGESTA TÉCNICA SOTA — PROYECTO POLYDIM
**Fecha de Ingesta:** 2026-09-18 13:00:32
**Cuenta Origen:** account_cursos
**Remitente:** The AiEdge <aiedge@substack.com>
**Asunto:** How Constrained Decoding Makes LLM Outputs Follow a Schema
**ID Correo:** 1a0b514099675e9f

---

## 📄 PAYLOAD TÉCNICO COMPLETO:
View this post on the web at https://newsletter.theaiedge.io/p/how-constrained-decoding-makes-llm-outputs

An LLM can return JSON that parses perfectly, matches every required field, and is still dangerous to execute. That is not a contradiction. It is the exact boundary of constrained decoding.
Normally, a language model can choose any token in its vocabulary at each generation step. Constrained decoding inserts a rule checker into that loop. The checker looks at the text already generated and removes every next token that would make the requested structure impossible to complete. The model then chooses among what remains.
Structured output has become a common connection layer between LLMs, extraction pipelines, and agent tools, yet a recent developer discussion exposed the practical surprise that matters here: a perfectly shaped object can still contain invented values, so schema-valid is not the same as safe to execute.
The central question is simple: what does the decoder actually guarantee? The compact answer is that it can guarantee membership in a supported output language, such as a JSON Schema, by blocking illegal continuations token by token. It does not prove that a legal value came from the input, reflects reality, satisfies a business rule, or deserves permission to trigger an action.
We will follow one support request through the complete mechanism. The request says: Please refund order A-17. The charge was $42.50. The desired output is a small object containing a status, an order identifier, and a refund amount in cents. First we need to separate three ideas that are often collapsed into the word “valid.” Then we can compile the schema, watch the token mask change, and see exactly where truth leaves the decoder's jurisdiction.
Three different promises hide inside “valid JSON”
JSON is a text format. A JSON parser checks punctuation and nesting: braces balance, keys are quoted, commas occur in legal places, and values have valid JSON forms. This object is valid JSON:
{"status":"ready","order_id":"A-17","refund_cents":4500}

A schema asks a narrower question about the parsed value. It can require an object, name its allowed properties, require selected keys, restrict a field to an integer, or limit a value to an enumeration. If our schema allows any non-negative integer for refund_cents, then 4500 passes. The schema has no memory of the user's $42.50.
Finally, the application asks whether the object means something acceptable in its real environment. Does order A-17 exist? Was the charge really $42.50? Is it refundable? Is this user authorized? Those are evidence, policy, and permission questions. They are not punctuation questions.
The checks therefore form a hierarchy:
Parseable means the text is legal JSON.
Schema-valid means the parsed value also obeys the declared structural rules.
Grounded and actionable means the values are supported by evidence and pass application policy.
Each level can remove failures that the previous level accepts. None can be silently substituted for the next.
Our refund extractor also needs a way to say that the message is incomplete. If a successful decode must complete a contract where every field is required and refund_cents must be an integer, every successful path puts some integer there even when no amount appears in the input. A better output contract exposes two branches:
{
  "anyOf": [
    {
      "status": "ready",
      "order_id": "string",
      "refund_cents": "non-negative integer"
    },
    {
      "status": "insufficient_info",
      "order_id": null,
      "refund_cents": null
    }
  ]
}

This is a readable sketch of the contract, not a literal complete JSON Schema. The important move is structural: uncertainty is now a legal output rather than an instruction the model must squeeze into fields that forbid it.
Here is the first design rule worth keeping: a schema should represent the failure states your application expects. Constrained decoding can only choose paths you make legal. If the contract requires a confident answer, the decoder cannot invent an abstention branch on your behalf.

Unsubscribe https://substack.com/redirect/2/eyJlIjoiaHR0cHM6Ly9uZXdzbGV0dGVyLnRoZWFpZWRnZS5pby9hY3Rpb24vZGlzYWJsZV9lbWFpbD90b2tlbj1leUoxYzJWeVgybGtJam94TmpZMU1UazJOaklzSW5CdmMzUmZhV1FpT2pJeE5qQXhPVFF6T0N3aWFXRjBJam94TnpnNU56UTBNemd4TENKbGVIQWlPakU0TWpFeU9EQXpPREVzSW1semN5STZJbkIxWWkweE1qTTRNRGMwSWl3aWMzVmlJam9pWkdsellXSnNaVjlsYldGcGJDSjkuRlRfa0dNODBCdGxlSmF5T3ZmTHpfNEdKc0dXZXYzbUEwUjFyczRfaG9fVSIsInAiOjIxNjAxOTQzOCwicyI6MTIzODA3NCwiZiI6dHJ1ZSwidSI6MTY2NTE5NjYyLCJpYXQiOjE3ODk3NDQzODEsImV4cCI6MjEwNTMyMDM4MSwiaXNzIjoicHViLTAiLCJzdWIiOiJsaW5rLXJlZGlyZWN0In0.UCGhEl9M5BwJQeTOxpepblJGe7ZUFzE5xlJHpxLKCLg?
