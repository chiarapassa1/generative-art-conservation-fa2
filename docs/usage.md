# Usage Guide

## Mint a token

The administrator (artist) mints a token and assigns it to a destination address.

During minting the contract also generates deterministic parameters that define the behaviour of the generative sculpture.

These parameters include:

- `seed`
- `mode`
- `personalityA`
- `personalityB`
- `personalityC`

They are stored on-chain and used by the artwork viewer to render the sculpture.

## Authorize a conservator

The administrator can authorize a conservator address.

Authorized conservators can participate in the conservation workflow by recording restoration events for a token.

## Log a restoration

A restoration record can be appended by:

- the token owner
- an authorized conservator
- the administrator (artist)

The entry usually contains a CID pointing to a conservation document stored on IPFS.

Examples of restoration documents include:

- migration reports
- technical compatibility reports
- exhibition packages
- browser support documentation
- checksum audits

## Add an artifact version

The administrator can register a canonical artifact version for a token.

This records a reference implementation of the artwork after an update or migration.

Typical examples:

- `v1.0_webgl`
- `v2.0_webgpu`
- `v2.1_browser_patch`

## Update artist intent

The administrator can update the artist intent configuration stored in the contract.

This may include:

- acceptable reinterpretation policies
- whether interactivity must be preserved
- allowed migration types
- forbidden actions
- references to an off-chain artist intent document (`intent_cid`)

## Direct sales from a website

For direct sales from a website, keep the artwork token as an **FA2 NFT**.

Two common approaches are:

- use a **sale contract** that receives tez and mints or transfers the NFT
- add a public **buy() or mint() entrypoint**

From the frontend, connect the user wallet (for example **Temple**) through **Beacon**.