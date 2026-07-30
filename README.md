# Generative Conservation FA2

SmartPy implementation of the Tezos FA2 standard for the long-term preservation of generative and software-based artworks.

**Author:** Chiara Passa  
**December 2025**

---

## Example artwork

![Example artwork](assets/OODebris0.jpg)

---

## Interaction demo

https://www.youtube.com/shorts/nrU4b1iR_uM

---

# Overview

**Generative Conservation FA2** extends the Tezos FA2 NFT standard with a preservation-oriented layer designed specifically for generative and software-based artworks.

Rather than treating an NFT solely as a proof of ownership, the project records the information required to preserve a generative artwork throughout its technical evolution.

The contract combines standard FA2 ownership with:

- deterministic generative identity
- artist intent
- renderer provenance
- structured preservation metadata

The goal is to support the long-term authenticity, migration, documentation, and reconstruction of generative artworks while remaining compatible with the FA2 ecosystem.

---

# Why this project exists

Generative artworks depend on software.

Browsers evolve, rendering engines become obsolete, libraries disappear, and execution environments change over time. Preserving a generative artwork therefore requires preserving not only ownership, but also the information needed to understand how the work should behave and how it may evolve without losing its identity.

Traditional NFT contracts generally record ownership and metadata.

This project explores how blockchain infrastructure can additionally support digital preservation by documenting the technical and conceptual evolution of an artwork throughout its lifetime.

---

# Core concepts

The contract is organized around four complementary concepts.

## Generative identity

Each token stores deterministic parameters generated during minting.

These parameters define the identity and behaviour of the artwork and are available on-chain for future compatible implementations.

The contract also distinguishes which parameters define the artwork's identity and which may be adapted during future preservation activities.

---

## Artist intent

The contract stores structured preservation metadata describing the artist's intentions for the collection.

This includes:

- acceptable reinterpretation
- interactivity requirements
- allowed migration strategies
- forbidden preservation actions
- authenticity rules
- reference to a complete off-chain artist intent document

Every modification is preserved through an append-only intent history.

---

## Renderer provenance

Software inevitably changes.

Instead of overwriting previous implementations, the contract maintains provenance for every registered renderer associated with a token.

It records:

- the original renderer
- subsequent renderer versions
- the canonical renderer currently recognized for the artwork

This allows future conservators and institutions to reconstruct the software history of each edition.

---

## Preservation metadata

Large preservation resources remain off-chain.

The contract stores compact references to resources such as:

- artist intent statements
- references to renderer implementations
- technical documentation
- decentralized backup locations

The blockchain therefore acts as a verifiable preservation index rather than an archival storage system.

---

# Main features

The current contract includes:

- FA2 NFT ownership
- administrator-controlled minting
- deterministic on-chain generative parameters
- parameter identity classification
- collection-level artist intent
- append-only artist intent history
- immutable original renderer registration
- renderer provenance tracking
- canonical renderer designation
- edition behaviour documentation
- decentralized preservation references

---

# Typical preservation workflow

A typical lifecycle is:

1. Mint a new artwork token.
2. Generate deterministic on-chain parameters.
3. Register the original renderer.
4. Transfer ownership through the FA2 standard.
5. Register future renderer implementations when migrations become necessary.
6. Designate the canonical renderer.
7. Update preservation metadata whenever required.
8. Preserve the complete provenance history on-chain.

---

# Documentation

Detailed documentation is available in the `docs/` directory.

### `architecture.md`

Describes the overall contract architecture, storage model, preservation workflow, renderer provenance, and permission model.

### `usage.md`

Provides a practical guide to the contract entrypoints and the recommended preservation workflow.

### `artist-intent.md`

Explains artist intent fields, authenticity rules, identity-defining parameters, and preservation policies.

---

# Repository structure

```text
generative-conservation-fa2/

├── assets/
├── contract/
│   └── generative_conservation_fa2.py
│
├── docs/
│   ├── architecture.md
│   ├── usage.md
│   └── artist-intent.md
│
├── examples/
├── metadata/
│
├── LICENSE
└── README.md
```

---

# Getting started

Open the SmartPy IDE:

https://smartpy.io/ide

Then:

1. Open the contract.
2. Configure the administrator address.
3. Configure contract metadata.
4. Run the included SmartPy tests.
5. Compile to Michelson.
6. Deploy to Ghostnet before deploying to Tezos Mainnet.

---

# Suggested use cases

This framework can support:

- generative artworks
- software-based art
- museum collections
- digital preservation research
- renderer provenance
- artist intent preservation
- decentralized archival references

---

# Conceptual framing

Rather than preserving software itself, the contract preserves the information required to understand, authenticate, migrate, and reconstruct a generative artwork over time.

Ownership follows the standard FA2 model, while preservation-related information—including generative identity, artist intent, renderer provenance, and decentralized documentation—is maintained as structured on-chain metadata.

The result is a preservation-oriented framework built on top of the Tezos FA2 standard.

---

# Important note

This repository is an artistic and research-oriented prototype intended to explore blockchain-assisted preservation of generative and software-based art.

Before production deployment, the contract should be carefully reviewed and independently audited.

---

# License

The source code is released under the MIT License.

Artwork files, images, media assets, and generative works remain © Chiara Passa 2025 and may not be reused without permission.
