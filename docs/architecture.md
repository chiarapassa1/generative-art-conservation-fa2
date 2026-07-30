Architecture
Overview

The contract combines a standard FA2 NFT implementation with preservation-oriented metadata designed for generative artworks.

Rather than recording only ownership, it stores information that supports the long-term preservation of software-based artworks, including artist intent, renderer provenance, generative identity and decentralized storage references.

Each token represents a generative artwork whose behaviour is defined by deterministic parameters stored on-chain. The contract also maintains structured conservation metadata that can support future migration and preservation activities.

Main storage areas

Core FA2 storage:

administrator
last_id
ledger
token_metadata

Generative layer:

token_params

Artist intent:

acceptable_reinterpretation
requires_interactivity
intent_cid
allowed_migrations
forbidden_actions
authenticity_rule
intent_history

Renderer provenance:

renderer_original_hash
renderer_history
renderer_version_count
renderer_canonical_version

Preservation metadata:

parameter_identity_flags
edition_behaviours
storage_backups
Generative identity

Each token stores a deterministic set of parameters generated during minting:

seed
mode
personalityA
personalityB
personalityC

These values define the generative identity of the artwork independently of any specific rendering technology.

The contract additionally distinguishes between identity-defining parameters and rendering parameters through parameter_identity_flags, allowing future conservation strategies to preserve conceptual identity while accommodating technological evolution.

Artist intent

Artist intent is stored at the contract level.

Preservation preferences can be updated by the administrator, with every modification permanently recorded in the append-only intent_history.

This creates a transparent record of how conservation policies evolve throughout the lifetime of the artwork.

Renderer provenance

The contract maintains independent provenance records for each token renderer.

For every artwork it stores:

the immutable original renderer hash;
an append-only history of registered renderer versions;
the currently designated canonical renderer.

This architecture documents software evolution without overwriting previous implementations.

Edition documentation

Each generative mode (0–9) can be associated with descriptive documentation through edition_behaviours.

This enables every edition of the artwork to include preservation-oriented contextual information while remaining independent of the rendering software itself.

Decentralized preservation resources

External preservation resources may be referenced using decentralized storage.

The contract stores backup URIs through storage_backups, allowing multiple preservation locations for documents such as artist intent statements and related conservation resources.

Roles
Administrator (Artist)

The administrator can:

mint new artworks;
update artist intent;
register renderer provenance;
select canonical renderers;
configure edition behaviours;
classify identity-defining parameters;
register decentralized storage backups.
Collector

Collectors own and transfer FA2 tokens using the standard NFT functionality.

The contract separates ownership from preservation metadata, allowing conservation information to evolve independently from token transfers.

Preservation workflow
Mint a token.
Store deterministic generative parameters.
Register the original renderer.
Register additional renderer versions when required.
Select the canonical renderer.
Update artist intent when conservation policies evolve.
Register edition documentation.
Maintain decentralized backup references for preservation resources.
Design philosophy

The contract does not attempt to perform conservation automatically.

Instead, it provides a structured on-chain framework for documenting the technical and conceptual evolution of generative artworks while remaining compatible with standard FA2 token ownership.
