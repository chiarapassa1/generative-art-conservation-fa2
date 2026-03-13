# Generative Conservation FA2
# SmartPy contract for generative artworks on Tezos
# Includes generative behaviour parameters and on-chain conservation records and artwork memory
# Author: Chiara Passa
# December 2025

import smartpy as sp
from smartpy.templates import fa2_lib as fa2

# FA2-lib "main"
main = fa2.main


@sp.module
def my_module():
    import main

    class GenerativeConservationFA2(
        main.Admin,
        main.Nft,
        main.BurnNft,
        main.OnchainviewBalanceOf,
    ):
        def __init__(self, admin_address, contract_metadata):
            """
            admin_address : address
            contract_metadata : big_map(string, bytes)
            """
            sp.cast(admin_address, sp.address)
            sp.cast(contract_metadata, sp.big_map[sp.string, sp.bytes])

            # --- FA2 core init (ordine come da doc) ---
            main.OnchainviewBalanceOf.__init__(self)
            main.BurnNft.__init__(self)

            # Minimal FA2 storage (vuoto, come base)
            ledger = {}          # nat -> address
            token_metadata = []  # list[map[string, bytes]]

            main.Nft.__init__(self, contract_metadata, ledger, token_metadata)
            main.Admin.__init__(self, admin_address)

            # --- Conservation + intent layer ---
            self.data.last_id = 0

            # big_map nat -> record(seed, mode, personalityA/B/C)
            self.data.token_params = sp.big_map()

            # big_map nat -> list(string) (CIDs di restauro)
            self.data.restoration_log = sp.big_map()

            # big_map nat -> list(record(version, ipfs_uri))
            self.data.artifact_versions = sp.big_map()

            # set(address)
            self.data.conservators = sp.set()

            # ------------------------------------------------------------
            # Artist intent (contract-level) (Exploration Allowed)
            # ------------------------------------------------------------
            self.data.acceptable_reinterpretation = True
            self.data.requires_interactivity = True
            self.data.intent_cid = ""
            self.data.allowed_migrations = []
            self.data.forbidden_actions = []

        # ------------------------------------------------------------
        # Helpers
        # ------------------------------------------------------------
        @sp.private(with_storage="read-only")
        def _token_exists(self, token_id):
            sp.cast(token_id, sp.nat)
            return self.data.token_metadata.contains(token_id)

        @sp.private(with_storage="read-only")
        def _only_admin(self):
            assert sp.sender == self.data.administrator, "ONLY_ARTIST"

        # ------------------------------------------------------------
        # Mint (admin-only)
        # ------------------------------------------------------------
        @sp.entrypoint
        def mint(self, params):
            sp.cast(
                params,
                sp.record(
                    to_=sp.address,
                    token_metadata=sp.map[sp.string, sp.bytes],
                ).layout(("to_", "token_metadata")),
            )

            self._only_admin()

            token_id = self.data.last_id
            assert not self._token_exists(token_id), "ALREADY_MINTED"

            # seed: timestamp + token_id (avoids same-block collisions)
            # NOTE: still deterministic (not true randomness), but less collision-prone than timestamp alone.
            seed = sp.as_nat(sp.now - sp.timestamp(0)) + token_id

            mode = sp.mod(seed, 10)
            pA = sp.mod(seed * 13, 10000)
            pB = sp.mod(seed * 997, 10000)
            pC = sp.mod(seed * 7777, 10000)

            # 1) save params on-chain
            self.data.token_params[token_id] = sp.record(
                seed=seed,
                mode=mode,
                personalityA=pA,
                personalityB=pB,
                personalityC=pC,
            )

            # 2) init conservation maps
            self.data.restoration_log[token_id] = []
            self.data.artifact_versions[token_id] = []

            # 3) FA2 NFT storage write
            self.data.ledger[token_id] = params.to_
            self.data.token_metadata[token_id] = sp.record(
                token_id=token_id,
                token_info=params.token_metadata,
            )

            # 4) advance counter
            self.data.last_id += 1

        # ------------------------------------------------------------
        # Conservation: add canonical artifact version (admin-only)
        # ------------------------------------------------------------
        @sp.entrypoint
        def add_artifact_version(self, params):
            sp.cast(
                params,
                sp.record(
                    token_id=sp.nat,
                    version=sp.string,
                    ipfs_uri=sp.string,
                ).layout(("token_id", ("version", "ipfs_uri"))),
            )

            self._only_admin()
            assert self._token_exists(params.token_id), "TOKEN_UNKNOWN"

            if not self.data.artifact_versions.contains(params.token_id):
                self.data.artifact_versions[params.token_id] = []

            self.data.artifact_versions[params.token_id].push(
                sp.record(version=params.version, ipfs_uri=params.ipfs_uri)
            )

        # ------------------------------------------------------------
        # Conservation: authorize/revoke conservator (admin-only)
        # ------------------------------------------------------------
        @sp.entrypoint
        def authorize_conservator(self, params):
            sp.cast(params, sp.record(address=sp.address).layout("address"))
            self._only_admin()
            self.data.conservators.add(params.address)

        @sp.entrypoint
        def revoke_conservator(self, params):
            sp.cast(params, sp.record(address=sp.address).layout("address"))
            self._only_admin()
            self.data.conservators.remove(params.address)

        # ------------------------------------------------------------
        # Conservation: log restoration (owner OR conservator OR admin)
        # ------------------------------------------------------------
        @sp.entrypoint
        def log_restoration(self, params):
            sp.cast(
                params,
                sp.record(
                    token_id=sp.nat,
                    cid=sp.string,
                ).layout(("token_id", "cid")),
            )

            assert self._token_exists(params.token_id), "TOKEN_UNKNOWN"
            owner = self.data.ledger[params.token_id]
            is_owner = owner == sp.sender
            is_conservator = self.data.conservators.contains(sp.sender)
            is_artist = sp.sender == self.data.administrator
            assert (is_owner or is_conservator or is_artist), "NOT_AUTHORIZED"

            if not self.data.restoration_log.contains(params.token_id):
                self.data.restoration_log[params.token_id] = []

            self.data.restoration_log[params.token_id].push(params.cid)

        # ------------------------------------------------------------
        # Artist intent updates (admin-only)
        # ------------------------------------------------------------
        @sp.entrypoint
        def update_artist_intent(self, params):
            sp.cast(
                params,
                sp.record(
                    key=sp.string,
                    value_bool=sp.bool,
                    value_string=sp.string,
                    value_list=list[sp.string],
                ).layout(("key", ("value_bool", ("value_string", "value_list")))),
            )

            self._only_admin()

            if params.key == "acceptable_reinterpretation":
                self.data.acceptable_reinterpretation = params.value_bool
            else:
                if params.key == "requires_interactivity":
                    self.data.requires_interactivity = params.value_bool
                else:
                    if params.key == "intent_cid":
                        self.data.intent_cid = params.value_string
                    else:
                        if params.key == "allowed_migrations":
                            self.data.allowed_migrations = params.value_list
                        else:
                            if params.key == "forbidden_actions":
                                self.data.forbidden_actions = params.value_list
                            else:
                                raise "BAD_INTENT_KEY"

# -----------------------------------------------------------
# TEST
# -----------------------------------------------------------
@sp.add_test()
def test():
    scenario = sp.test_scenario("FA2 + Conservation (Option B)")

    ADMIN_REAL = sp.address("tz1...YOUR_WALLET")
    alice = sp.test_account("Alice")

    metadata_uri = "ipfs://bafkreidfzvery2zn5en4w4o66sapvjt6vrmsojpr6o4o73a667f5f6f3re"
    contract_metadata = sp.scenario_utils.metadata_of_url(metadata_uri)

    c = my_module.GenerativeConservationFA2(ADMIN_REAL, contract_metadata)
    scenario += c

    # Mint 10 token 0..9
    cids = [
        "ipfs://bafkreigl7bvxf636pk5wb4a56gxqulveqgo3an2h4riual2zlkqx7zp6aa",
        "ipfs://bafkreihhuni6eehlze3tr57wfxzzgdvbbjt4x6zu3tjbt4uiekmbn5ootm",
        "ipfs://bafkreiewg4xxpej6x43cihhzpokhmqcjadx5adq3tijiudeerrjz3f2fg4",
        "ipfs://bafkreibwg5saqwiorviwwlfos3eoybksgfliosfc2arzjws7h2ayyhb3ty",
        "ipfs://bafkreibmd3ektxq7xfn5lyk6njcmbkvwglvespvge3fogsqgaoj6q25yqi",
        "ipfs://bafkreicnav556qkrppklpx45bpfiuld3zh2hgmhzdxpdfzlmbpspxe7avm",
        "ipfs://bafkreiam75a2hacurob6btjsaittonuvzbnhqz6uceqrpnbi42puopgmiu",
        "ipfs://bafkreidttfmw5ye3oklid4outlpehstnga74q3liwrbbw6h67zxkbcyeyy",
        "ipfs://bafkreif2fxqgg4w5m7hwigh4woqb57bn5rrij2doofc3eqkffof57s43v4",
        "ipfs://bafkreibyap6ssz6d6y5732jb4cp7meqvp2z6sopihh4hb7e6obcdvxch6u",
    ]

    for cid in cids:
        token_md = sp.map({"": sp.scenario_utils.bytes_of_string(cid)})
        c.mint(to_=alice.address, token_metadata=token_md, _sender=ADMIN_REAL)

    # Add canonical artifact for token 0 (token 0 exists now)
    c.add_artifact_version(
        token_id=0,
        version="v1.0_canonical",
        ipfs_uri="ipfs://bafkreiha4utz4u46ujg55dghwhfaunuzoeck4zbkdtdllq2k3z7nvvv7ae",
        _sender=ADMIN_REAL,
    )

    # Log restoration by owner (Alice)
    c.log_restoration(
        token_id=0,
        cid="ipfs://REPLACE_WITH_FIRST_RESTORATION_CID",
        _sender=alice,
    )

# ----------------------------------------------------------------
# COMPILATION TARGET (Ghostnet)
# ----------------------------------------------------------------
ADMIN_REAL = sp.address("tz1...YOUR_WALLET")
CONTRACT_METADATA_URI = "ipfs://bafkreidfzvery2zn5en4w4o66sapvjt6vrmsojpr6o4o73a667f5f6f3re"


def _mk_contract():
    return my_module.GenerativeConservationFA2(
        ADMIN_REAL,
        sp.scenario_utils.metadata_of_url(CONTRACT_METADATA_URI),
    )


_act = getattr(sp, "add_compilation_target", None)
if callable(_act):
    _scenario = sp.test_scenario()
    _c = _mk_contract()
    _scenario += _c
    _act("Ghostnet_GenerativeConservationFA2", _c)
