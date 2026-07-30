# Usage Guide

## Mint a token

The administrator (artist) mints a token and assigns it to a destination address.

During minting, the contract generates deterministic parameters defining the behaviour of the generative artwork.

Each token stores:

- `seed`
- `mode`
- `personalityA`
- `personalityB`
- `personalityC`

These parameters constitute the generative identity of the artwork and can be retrieved through on-chain views.

## Register the original renderer

After minting, the administrator may register the original renderer associated with a token.

The contract stores:

- immutable renderer hash
- renderer CID
- registration metadata

The original renderer can only be registered once.

## Register renderer versions

Additional renderer implementations can be registered whenever the artwork is migrated or adapted to new execution environments.

Each version records:

- renderer hash
- renderer CID
- descriptive note
- registration timestamp
- registering address

Renderer histories are append-only.

## Select the canonical renderer

The administrator may designate one registered renderer version as the current canonical implementation.

Changing the canonical renderer does not remove previous versions, allowing conservation decisions to remain fully documented.

## Configure artist intent

The administrator can update preservation-related information stored on-chain.

Supported fields include:

- acceptable reinterpretation
- interactivity requirement
- artist intent document (`intent_cid`)
- allowed migrations
- forbidden actions
- authenticity rule

Every modification is recorded in an append-only intent history.

## Define edition behaviours

Each generative mode (0–9) may be associated with a human-readable label and a description document.

This allows every edition of the artwork to carry its own conservation and interpretative documentation.

## Configure parameter identity

The administrator may specify whether a generative parameter is identity-defining or rendering-related.

Identity-defining parameters should remain unchanged to preserve the artwork's identity, while rendering parameters may be adapted during future conservation activities.

## Register decentralized storage backups

Alternative storage locations can be registered for preservation resources such as artist intent documents.

Multiple backup URIs may be associated with the same resource, facilitating long-term preservation across decentralized storage systems.
