# Architecture

## Overview

The contract combines an NFT ownership layer with conservation-oriented records and generative behaviour parameters.

It extends a standard FA2 NFT model with structures designed to document both the **technical life of the artwork** and the **behavioural parameters that define each generative edition**.

Each token represents a generative artwork whose behaviour is defined by deterministic parameters stored on-chain. The contract also records conservation events and canonical implementations as the artwork evolves over time.

## Main storage areas

- `administrator`: contract administrator / artist
- `last_id`: token counter
- `ledger`: token ownership mapping
- `token_metadata`: token-level metadata
- `token_params`: generative behaviour parameters per token
- `conservators`: authorized conservation addresses
- `restoration_log`: list of restoration-report CIDs per token
- `artifact_versions`: list of canonical implementations per token
- artist intent fields at contract level

## Generative layer

Each token stores deterministic parameters generated at mint time.

These parameters include:

- `seed`
- `mode`
- `personalityA`
- `personalityB`
- `personalityC`

These values define how the generative sculpture behaves when rendered by the artwork viewer.

Because these parameters are stored on-chain, the behaviour of each edition can always be reconstructed, even if the rendering engine or software environment changes.

## Preservation model

This repository treats the artwork as more than a static token.

Each token points to a software-based artwork whose implementation may evolve over time. Technologies, browsers, and rendering engines change, and the artwork may require technical migration to remain accessible.

The contract does not replace archival practice. Instead, it creates an **on-chain index of preservation decisions, behaviour parameters, and canonical states**.

## Roles

### Artist / administrator

The administrator can:

- mint tokens
- authorize conservators
- register canonical artifact versions
- update artist intent fields

### Owner / collector

The owner can hold and transfer the token.

In the current prototype, the owner can also participate in restoration logging.

### Conservator

A trusted address that can append restoration evidence to the conservation record.

## Conservation sequence

1. Mint token
2. Generative parameters are stored on-chain
3. Transfer token to owner
4. Authorize conservator
5. Create an off-chain conservation report
6. Upload the report to IPFS
7. Record the CID in `restoration_log`
8. Register the updated canonical implementation in `artifact_versions`

## Why keep some data off-chain

Detailed technical conservation records can be large and may evolve over time.

The contract therefore stores **compact references (CIDs)** while the full documentation can live on IPFS or institutional archival systems.