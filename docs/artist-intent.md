Artist Intent

Artist intent plays a central role in the long-term preservation of generative and software-based artworks.

This contract stores a set of contract-level preservation fields that document the artist's conservation preferences in a structured, machine-readable form.

These values define conceptual boundaries that can guide future preservation, migration and reinterpretation decisions.

Included fields

The contract currently stores:

acceptable_reinterpretation
requires_interactivity
intent_cid
allowed_migrations
forbidden_actions
authenticity_rule

These fields apply to the artwork collection as a whole rather than to individual tokens.

Every modification is permanently recorded through an append-only intent_history, allowing future conservators to reconstruct how the artist's preservation intentions evolved over time.

Why this matters

As software platforms evolve, artworks may require migration, emulation or adaptation to remain accessible.

The artist intent fields provide structured guidance regarding:

acceptable reinterpretation
preservation of interactivity
permitted migration strategies
actions considered incompatible with the work
authenticity verification

Rather than enforcing conservation decisions automatically, these records provide transparent documentation that can support future conservation practice.

Behavioural parameters

Each token stores a deterministic set of parameters describing its generative identity:

seed
mode
personalityA
personalityB
personalityC

These parameters are generated during minting and stored permanently on-chain.

The contract also distinguishes between identity-defining parameters and rendering parameters through parameter_identity_flags.

Identity-defining parameters should remain unchanged to preserve the identity of the artwork, while rendering parameters may be adapted when future preservation strategies require technological migration.

Authenticity

The contract currently defines the authenticity rule:

seed_must_match

This rule expresses that the deterministic generative seed is considered an essential component of the artwork's identity.

Recommended practice

The on-chain fields provide a concise preservation record rather than a complete conservation policy.

A more detailed artist intent statement should be maintained as an external document (for example PDF or Markdown), stored using decentralized storage such as IPFS, with its CID referenced by the intent_cid field.
