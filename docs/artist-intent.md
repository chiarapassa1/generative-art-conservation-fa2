# Artist Intent

Artist intent is often critical in the conservation of generative and software-based art.

This contract includes several **contract-level fields** that help guide future migration and restoration decisions.

These fields provide a minimal, machine-readable statement of the artist’s conceptual boundaries for the work.

## Included fields

- `acceptable_reinterpretation`
- `requires_interactivity`
- `intent_cid`
- `allowed_migrations`
- `forbidden_actions`

These fields are stored at the **contract level**, meaning they apply to the artwork collection as a whole rather than individual tokens.

## Why this matters

When software becomes obsolete, conservators often need to decide whether a work can be:

- reimplemented
- emulated
- migrated to new technologies
- partially substituted

These fields help document the artist’s preferences in a structured form that can guide future preservation decisions.

They are **guidelines rather than strict enforcement rules**, but they provide valuable context for conservators and institutions.

## Behavioural parameters

Each token also stores a set of deterministic parameters that define the behaviour of the generative sculpture.

These parameters include:

- `seed`
- `mode`
- `personalityA`
- `personalityB`
- `personalityC`

They are generated at mint time and stored on-chain.

The artwork viewer uses these parameters to determine structural variations, motion, and interaction behaviour of the digital sculpture.

Future implementations of the artwork should preserve the **conceptual role of these parameters**, even if the underlying rendering technology changes.

For example, if the artwork is migrated from WebGL to WebGPU or another graphics environment, the behavioural logic driven by these parameters should remain consistent so that each edition retains its identity.

## Example questions this can help answer

- Is a renderer rewrite acceptable?
- Can the work be ported from WebGL to WebGPU?
- Is reduced interactivity forbidden?
- Can browser dependencies be updated?
- Should behavioural parameters remain stable across migrations?
- Is color correction acceptable?

## Recommended practice

Keep a fuller artist intent statement off-chain as a text or PDF document.

Upload that document to IPFS and store its CID in the `intent_cid` field so that future conservators can access the complete statement.