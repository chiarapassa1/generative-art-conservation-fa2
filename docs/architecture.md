# Architecture

## Overview

The contract combines a Tezos FA2 NFT ownership layer with preservation-oriented metadata for generative and software-based artworks.

Each token represents a generative artwork edition whose identity is defined by deterministic parameters stored on-chain. The contract also documents the evolution of the artwork's software implementation through per-token renderer provenance, while collection-level artist intent and preservation settings provide guidance for future migration and conservation decisions.

The architecture is organized around four main concerns:

- FA2 ownership and token metadata
- deterministic generative identity
- artist intent and preservation policy
- renderer provenance and decentralized documentation

The contract does not contain conservator roles, restoration logs, or generic artifact-version records. Preservation-related entrypoints are controlled by the administrator.

## Main storage areas

### FA2 core

- `administrator`: contract administrator and artist authority
- `last_id`: token counter used during minting
- `ledger`: token ownership mapping
- `token_metadata`: token-level FA2 metadata

### Generative identity

- `token_params`: deterministic generative parameters stored for each token
- `parameter_identity_flags`: classification of parameters as identity-defining or rendering-related
- `edition_behaviours`: descriptive documentation associated with generative modes

### Artist intent

- `acceptable_reinterpretation`: statement describing whether reinterpretation is acceptable
- `requires_interactivity`: indicates whether interactivity must be preserved
- `intent_cid`: reference to a fuller off-chain artist intent document
- `allowed_migrations`: migration strategies accepted by the artist
- `forbidden_actions`: actions considered incompatible with the artwork
- `authenticity_rule`: rule used to express an essential condition of authenticity
- `intent_history`: append-only record of artist intent updates

### Renderer provenance

- `renderer_original_hash`: immutable reference to the original renderer registered for each token
- `renderer_history`: append-only renderer-version history for each token
- `renderer_version_count`: number of renderer versions registered for each token
- `renderer_canonical_version`: renderer version currently designated as canonical for each token

### Decentralized preservation references

- `storage_backups`: alternative decentralized storage locations associated with preservation resources

## Generative layer

Each token stores deterministic parameters generated at mint time:

- `seed`
- `mode`
- `personalityA`
- `personalityB`
- `personalityC`

These values define the generative behaviour and identity of an artwork edition. The artwork viewer uses them to determine structural variation, motion, personality, and interaction.

Because the parameters are stored on-chain, future renderer implementations can retrieve the same source values even when the underlying graphics technology changes.

The `parameter_identity_flags` structure distinguishes parameters that must remain stable to preserve the identity of an edition from parameters that may be treated as rendering-related during migration.

## Artist intent model

Artist intent is stored at the contract level and therefore applies to the collection as a whole.

The administrator can update fields describing acceptable reinterpretation, interactivity requirements, migration policies, forbidden actions, authenticity conditions, and the CID of a fuller off-chain statement.

Updates are not treated as disposable replacements. Each change is also recorded in the append-only `intent_history`, creating a traceable record of how preservation guidance evolves over time.

## Renderer versioning

Renderer provenance is maintained separately for each token.

The renderer workflow uses three administrator-controlled entrypoints:

1. `register_original_renderer` records the original renderer reference for a token.
2. `register_renderer_version` appends a later renderer implementation to that token's version history.
3. `set_canonical_renderer` designates one registered version as the current canonical renderer.

The original renderer and the version history serve different purposes. The original renderer preserves provenance, while the canonical renderer identifies the implementation currently recognized as authoritative. Selecting a new canonical version does not erase earlier versions.

This model documents software evolution without using a generic `artifact_versions` list and without overwriting the historical renderer record.

## Edition behaviours

The `edition_behaviours` table associates generative modes with human-readable labels and descriptive references.

This provides documentation for the conceptual or behavioural characteristics of different editions independently of the renderer implementation used to display them.

## Decentralized storage backups

The `storage_backups` structure records alternative storage locations for preservation resources.

These references can support redundancy for artist intent documents, renderer packages, technical documentation, or related archival material stored outside the contract.

The blockchain therefore acts as an index and provenance layer rather than a replacement for full archival storage.

## Preservation model

This repository treats a generative artwork as more than a static token or media file.

Browsers, rendering engines, dependencies, and exhibition environments change over time. A renderer may therefore require migration or reimplementation while the artwork's defining parameters and conceptual boundaries remain stable.

The contract supports this distinction by keeping:

- deterministic token parameters as the basis of generative identity
- artist intent as collection-level preservation guidance
- renderer versions as per-token software provenance
- canonical renderer selection as an explicit administrative decision
- decentralized references as links to fuller documentation and archival resources

The contract does not perform conservation automatically. It provides a structured on-chain record that can support future conservation practice.

## Roles and permissions

### Administrator / artist

The administrator controls the preservation-oriented configuration of the contract and can:

- mint tokens
- update artist intent
- register the original renderer for a token
- register later renderer versions
- select the canonical renderer
- configure parameter identity flags
- define edition behaviours
- register decentralized storage backups

These preservation operations are protected by administrator-only authorization.

### Owner / collector

The owner holds the FA2 token and can transfer it according to the contract's FA2 transfer rules.

Token ownership does not grant permission to modify artist intent, renderer provenance, canonical renderer selection, edition behaviours, parameter classifications, or storage backups.

### Conservator

The contract does not define a conservator role or a conservator authorization registry.

A museum, conservator, or technical specialist may prepare off-chain documentation or renderer packages, but only the administrator can register preservation-related data through the contract's protected entrypoints.

## Preservation sequence

A typical workflow is:

1. The administrator mints a token.
2. Deterministic generative parameters are stored on-chain.
3. The original renderer is registered for that token.
4. The token may be transferred to a collector through the FA2 ownership layer.
5. A migration or renderer update is prepared off-chain when required.
6. The administrator registers the new renderer version.
7. The administrator may designate that version as canonical.
8. Artist intent, edition documentation, parameter identity flags, or storage backups are updated when necessary.
9. Earlier renderer versions and artist intent records remain available as provenance history.

## Why keep some data off-chain

Renderer packages, technical reports, artist statements, exhibition documentation, and archival records can be too large or too complex to store directly on-chain.

The contract therefore stores compact hashes, CIDs, descriptive records, and backup references, while the full resources can remain on IPFS or in institutional archival systems.

This approach keeps the on-chain record verifiable and durable without attempting to replace established conservation and archival infrastructure.
