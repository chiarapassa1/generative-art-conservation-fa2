Artist Intent

Artist intent is often critical in the conservation of generative and software-based art.

This contract includes several contract-level fields that help guide future migration and restoration decisions.

These fields provide a minimal, machine-readable statement of the artist's conceptual boundaries for the work.

Included fields
acceptable_reinterpretation
requires_interactivity
intent_cid
allowed_migrations
forbidden_actions
authenticity_rule

These fields are stored at the contract level, meaning they apply to the artwork collection as a whole rather than individual tokens.

Why this matters

When software becomes obsolete, conservators often need to decide whether a work can be:

reimplemented
emulated
migrated to new technologies
partially substituted

These fields help document the artist's preferences in a structured form that can guide future preservation decisions.

acceptable_reinterpretation, requires_interactivity, intent_cid, and allowed_migrations are guidelines rather than strict enforcement rules — they provide valuable context for conservators and institutions, but nothing in the contract prevents an admin action that contradicts them.

forbidden_actions works differently. Values are restricted on-chain to a fixed vocabulary of action codes:

changing_seed
changing_mode
changing_identity_parameters
removing_interactivity
static_capture_as_canonical
unregistered_renderer_override

Any other string is rejected by the contract (BAD_FORBIDDEN_ACTION). This makes forbidden_actions a structured, machine-checkable declaration rather than free-form prose — the artwork viewer can read these codes and enforce them directly (for example, disabling seed regeneration or forcing interactivity controls to remain enabled). At present the viewer enforces a subset of these codes; the remaining ones are recorded on-chain and available for enforcement once the viewer is updated to check them.

authenticity_rule declares the invariant the viewer checks before treating a token's on-chain parameters as authoritative (currently fixed to seed_must_match). Unlike forbidden_actions, this is a single declared rule rather than a list, and the contract restricts it to the one recognized value.

Change history

Every update to any of these fields — through the update_artist_intent entrypoint — is recorded in an append-only intent history log (intent_history), capturing the field changed, its previous and new value, who made the change, and when. This means the artist's intent is not just a current snapshot: its evolution over time is itself part of the on-chain conservation record.

Behavioural parameters

Each token also stores a set of deterministic parameters that define the behaviour of the generative sculpture.

These parameters include:

seed
mode
personalityA
personalityB
personalityC

They are generated at mint time and stored on-chain.

The artwork viewer uses these parameters to determine structural variations, motion, and interaction behaviour of the digital sculpture.

The contract also distinguishes, per parameter, whether it is identity-defining or rendering-related (see parameter_identity_flags). By default, seed and mode are identity-defining and should remain unchanged to preserve the artwork's identity, while personalityA/B/C are rendering-related and may be adapted during future conservation activities. Future implementations of the artwork should preserve the conceptual role of the identity-defining parameters, even if the underlying rendering technology changes.

For example, if the artwork is migrated from WebGL to WebGPU or another graphics environment, the behavioural logic driven by these parameters should remain consistent so that each edition retains its identity.

Example questions this can help answer
Is a renderer rewrite acceptable?
Can the work be ported from WebGL to WebGPU?
Is reduced interactivity forbidden?
Can browser dependencies be updated?
Should behavioural parameters remain stable across migrations?
Is color correction acceptable?
Which parameters are identity-defining, and which may be reinterpreted?
What rule must hold for a rendered token to be considered authentic?
Recommended practice

Keep a fuller artist intent statement off-chain as a text or PDF document.

Upload that document to IPFS and store its CID in the intent_cid field so that future conservators can access the complete statement. Consider registering backup locations for that document via the decentralized storage backup registry (storage_backups), so the statement remains accessible even if the original pinning service becomes unavailable.
