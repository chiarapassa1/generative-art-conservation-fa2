# Generative FA2
# SmartPy contract for generative artworks on Tezos
# For MOMIxTezos fellowship:
# Ten generative behaviours and N personalities
# Artist intent + conservation fields
# Author: Chiara Passa

import smartpy as sp
from smartpy.templates import fa2_lib as fa2

# FA2-lib "main"
main = fa2.main


@sp.module
def my_module():
    import main

    class GenerativeFA2(
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

            # --- FA2 core init ---
            main.OnchainviewBalanceOf.__init__(self)
            main.BurnNft.__init__(self)

            ledger = {}
            token_metadata = []

            main.Nft.__init__(self, contract_metadata, ledger, token_metadata)
            main.Admin.__init__(self, admin_address)

            # ------------------------------------------------------------
            # Generative layer
            # ------------------------------------------------------------
            self.data.last_id = 0

            self.data.token_params = sp.big_map()

            # ------------------------------------------------------------
            # Artist intent
            # ------------------------------------------------------------
            self.data.acceptable_reinterpretation = True
            self.data.requires_interactivity = True
            self.data.intent_cid = ""
            self.data.allowed_migrations = []
            self.data.forbidden_actions = []
            self.data.authenticity_rule = "seed_must_match"

            # ------------------------------------------------------------
            # Per-token renderer identity & provenance
            # 1) renderer_original_hash[token_id]: immutable original hash
            # 2) renderer_history[(token_id, version)]: append-only versions
            # 3) renderer_canonical_version[token_id]: current authority pointer
            # Registration may happen after minting; the contract proves who
            # registered each value and that the original cannot be overwritten,
            # but it cannot prove retrospectively which renderer ran at mint time.
            # ------------------------------------------------------------
            self.data.renderer_original_hash = sp.big_map()
            self.data.renderer_history = sp.big_map()
            self.data.renderer_version_count = sp.big_map()
            self.data.renderer_canonical_version = sp.big_map()

            # ------------------------------------------------------------
            # Generative Parameter: identity vs rendering
            # True  = identity-defining (immutable, must be preserved exactly)
            # False = rendering-only (may be reinterpreted/rebalanced)
            # ------------------------------------------------------------
            self.data.parameter_identity_flags = sp.big_map(
                {
                    "seed": True,
                    "mode": True,
                    "personalityA": False,
                    "personalityB": False,
                    "personalityC": False,
                }
            )

            # ------------------------------------------------------------
            # Edition Customization Instructions
            # key = mode (0-9), value = label + description CID
            # ------------------------------------------------------------
            self.data.edition_behaviours = sp.big_map()

            # ------------------------------------------------------------
            # Artist intent history (append-only log)
            # ------------------------------------------------------------
            self.data.intent_history = sp.big_map()
            self.data.intent_version = 0

            # ------------------------------------------------------------
            # Decentralized Storage: backup CIDs / gateways
            # key = resource name (e.g. "intent_cid"), value = list of URIs
            # ------------------------------------------------------------
            self.data.storage_backups = sp.big_map()

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

        @sp.private(with_storage="read-only")
        def _assert_valid_forbidden_actions(self, actions):
            sp.cast(actions, list[sp.string])
            for action in actions:
                assert (
                    (action == "changing_seed")
                    or (action == "changing_mode")
                    or (action == "changing_identity_parameters")
                    or (action == "removing_interactivity")
                    or (action == "static_capture_as_canonical")
                    or (action == "unregistered_renderer_override")
                ), "BAD_FORBIDDEN_ACTION"

        # ------------------------------------------------------------
        # View token params
        # ------------------------------------------------------------
        @sp.onchain_view()
        def get_token_params(self, token_id):
            sp.cast(token_id, sp.nat)
            assert self.data.token_params.contains(token_id), "NO_TOKEN"
            return self.data.token_params[token_id]

        @sp.onchain_view()
        def get_renderer_original_hash(self, token_id):
            sp.cast(token_id, sp.nat)
            assert self.data.renderer_original_hash.contains(token_id), "NO_ORIGINAL_RENDERER"
            return self.data.renderer_original_hash[token_id]

        @sp.onchain_view()
        def get_renderer_version(self, params):
            sp.cast(
                params,
                sp.record(token_id=sp.nat, version=sp.nat).layout(("token_id", "version")),
            )
            key = (params.token_id, params.version)
            assert self.data.renderer_history.contains(key), "NO_SUCH_VERSION"
            return self.data.renderer_history[key]

        @sp.onchain_view()
        def get_canonical_renderer(self, token_id):
            sp.cast(token_id, sp.nat)
            assert self.data.renderer_canonical_version.contains(token_id), "NO_RENDERER_REGISTERED"
            version = self.data.renderer_canonical_version[token_id]
            return self.data.renderer_history[(token_id, version)]

        @sp.onchain_view()
        def get_edition_behaviour(self, mode):
            sp.cast(mode, sp.nat)
            assert self.data.edition_behaviours.contains(mode), "NO_EDITION"
            return self.data.edition_behaviours[mode]

        # ------------------------------------------------------------
        # Mint
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

            seed = sp.as_nat(sp.now - sp.timestamp(0)) + token_id

            mode = sp.mod(seed, 10)
            pA = sp.mod(seed * 13, 10000)
            pB = sp.mod(seed * 997, 10000)
            pC = sp.mod(seed * 7777, 10000)

            self.data.token_params[token_id] = sp.record(
                seed=seed,
                mode=mode,
                personalityA=pA,
                personalityB=pB,
                personalityC=pC,
            )

            self.data.ledger[token_id] = params.to_
            self.data.token_metadata[token_id] = sp.record(
                token_id=token_id,
                token_info=params.token_metadata,
            )

            self.data.last_id += 1

        # ------------------------------------------------------------
        # Artist intent updates (now with append-only history log)
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
                self.data.intent_history[self.data.intent_version] = sp.record(
                    key=params.key,
                    old_value_bool=self.data.acceptable_reinterpretation,
                    new_value_bool=params.value_bool,
                    old_value_string="",
                    new_value_string="",
                    old_value_list=[],
                    new_value_list=[],
                    changed_by=sp.sender,
                    changed_at=sp.now,
                )
                self.data.intent_version += 1
                self.data.acceptable_reinterpretation = params.value_bool
            else:
                if params.key == "requires_interactivity":
                    self.data.intent_history[self.data.intent_version] = sp.record(
                        key=params.key,
                        old_value_bool=self.data.requires_interactivity,
                        new_value_bool=params.value_bool,
                        old_value_string="",
                        new_value_string="",
                        old_value_list=[],
                        new_value_list=[],
                        changed_by=sp.sender,
                        changed_at=sp.now,
                    )
                    self.data.intent_version += 1
                    self.data.requires_interactivity = params.value_bool
                else:
                    if params.key == "intent_cid":
                        self.data.intent_history[self.data.intent_version] = sp.record(
                            key=params.key,
                            old_value_bool=False,
                            new_value_bool=False,
                            old_value_string=self.data.intent_cid,
                            new_value_string=params.value_string,
                            old_value_list=[],
                            new_value_list=[],
                            changed_by=sp.sender,
                            changed_at=sp.now,
                        )
                        self.data.intent_version += 1
                        self.data.intent_cid = params.value_string
                    else:
                        if params.key == "allowed_migrations":
                            self.data.intent_history[self.data.intent_version] = sp.record(
                                key=params.key,
                                old_value_bool=False,
                                new_value_bool=False,
                                old_value_string="",
                                new_value_string="",
                                old_value_list=self.data.allowed_migrations,
                                new_value_list=params.value_list,
                                changed_by=sp.sender,
                                changed_at=sp.now,
                            )
                            self.data.intent_version += 1
                            self.data.allowed_migrations = params.value_list
                        else:
                            if params.key == "forbidden_actions":
                                self._assert_valid_forbidden_actions(params.value_list)
                                self.data.intent_history[self.data.intent_version] = sp.record(
                                    key=params.key,
                                    old_value_bool=False,
                                    new_value_bool=False,
                                    old_value_string="",
                                    new_value_string="",
                                    old_value_list=self.data.forbidden_actions,
                                    new_value_list=params.value_list,
                                    changed_by=sp.sender,
                                    changed_at=sp.now,
                                )
                                self.data.intent_version += 1
                                self.data.forbidden_actions = params.value_list
                            else:
                                if params.key == "authenticity_rule":
                                    assert params.value_string == "seed_must_match", "BAD_AUTHENTICITY_RULE"
                                    self.data.intent_history[self.data.intent_version] = sp.record(
                                        key=params.key,
                                        old_value_bool=False,
                                        new_value_bool=False,
                                        old_value_string=self.data.authenticity_rule,
                                        new_value_string=params.value_string,
                                        old_value_list=[],
                                        new_value_list=[],
                                        changed_by=sp.sender,
                                        changed_at=sp.now,
                                    )
                                    self.data.intent_version += 1
                                    self.data.authenticity_rule = params.value_string
                                else:
                                    raise "BAD_INTENT_KEY"

        # ------------------------------------------------------------
        # Per-token renderer provenance
        # ------------------------------------------------------------
        @sp.entrypoint
        def register_original_renderer(self, params):
            sp.cast(
                params,
                sp.record(
                    token_id=sp.nat,
                    renderer_hash=sp.bytes,
                    renderer_cid=sp.string,
                    note=sp.string,
                ).layout(("token_id", ("renderer_hash", ("renderer_cid", "note")))),
            )

            self._only_admin()
            # token_params is the persistent generative identity, even if the
            # transferable FA2 token is later burned.
            assert self.data.token_params.contains(params.token_id), "NO_TOKEN_IDENTITY"
            assert not self.data.renderer_original_hash.contains(params.token_id), "ORIGINAL_ALREADY_SET"

            self.data.renderer_original_hash[params.token_id] = params.renderer_hash
            self.data.renderer_history[(params.token_id, 0)] = sp.record(
                renderer_hash=params.renderer_hash,
                renderer_cid=params.renderer_cid,
                note=params.note,
                registered_by=sp.sender,
                registered_at=sp.now,
            )
            self.data.renderer_version_count[params.token_id] = 1
            self.data.renderer_canonical_version[params.token_id] = 0

        @sp.entrypoint
        def register_renderer_version(self, params):
            sp.cast(
                params,
                sp.record(
                    token_id=sp.nat,
                    renderer_hash=sp.bytes,
                    renderer_cid=sp.string,
                    note=sp.string,
                ).layout(("token_id", ("renderer_hash", ("renderer_cid", "note")))),
            )

            self._only_admin()
            assert self.data.token_params.contains(params.token_id), "NO_TOKEN_IDENTITY"
            assert self.data.renderer_original_hash.contains(params.token_id), "NO_ORIGINAL_RENDERER"

            new_version = self.data.renderer_version_count[params.token_id]
            self.data.renderer_history[(params.token_id, new_version)] = sp.record(
                renderer_hash=params.renderer_hash,
                renderer_cid=params.renderer_cid,
                note=params.note,
                registered_by=sp.sender,
                registered_at=sp.now,
            )
            self.data.renderer_version_count[params.token_id] = new_version + 1

        @sp.entrypoint
        def set_canonical_renderer(self, params):
            sp.cast(
                params,
                sp.record(token_id=sp.nat, version=sp.nat).layout(("token_id", "version")),
            )

            self._only_admin()
            assert self.data.token_params.contains(params.token_id), "NO_TOKEN_IDENTITY"
            assert self.data.renderer_history.contains((params.token_id, params.version)), "NO_SUCH_VERSION"

            self.data.renderer_canonical_version[params.token_id] = params.version

        # ------------------------------------------------------------
        # Edition behaviour table (mode -> meaning)
        # ------------------------------------------------------------
        @sp.entrypoint
        def set_edition_behaviour(self, params):
            sp.cast(
                params,
                sp.record(
                    mode=sp.nat,
                    label=sp.string,
                    description_cid=sp.string,
                ).layout(("mode", ("label", "description_cid"))),
            )

            self._only_admin()
            assert params.mode < 10, "BAD_MODE"

            self.data.edition_behaviours[params.mode] = sp.record(
                label=params.label,
                description_cid=params.description_cid,
            )

        # ------------------------------------------------------------
        # Identity vs rendering flag override
        # (kept separate from init so it stays a deliberate, logged act)
        # ------------------------------------------------------------
        @sp.entrypoint
        def set_parameter_identity_flag(self, params):
            sp.cast(
                params,
                sp.record(
                    parameter_name=sp.string,
                    is_identity=sp.bool,
                ).layout(("parameter_name", "is_identity")),
            )

            self._only_admin()
            self.data.parameter_identity_flags[params.parameter_name] = params.is_identity

        # ------------------------------------------------------------
        # Decentralized storage backup registry
        # ------------------------------------------------------------
        @sp.entrypoint
        def add_storage_backup(self, params):
            sp.cast(
                params,
                sp.record(
                    key=sp.string,
                    uri=sp.string,
                ).layout(("key", "uri")),
            )

            self._only_admin()

            if self.data.storage_backups.contains(params.key):
                self.data.storage_backups[params.key].push(params.uri)
            else:
                self.data.storage_backups[params.key] = [params.uri]


# -----------------------------------------------------------
# TEST
# -----------------------------------------------------------
@sp.add_test()
def test():
    scenario = sp.test_scenario("Generative FA2 MOMIxTezos")

    ADMIN_REAL = sp.address("tz1d7W6HtnRgNeDg4PtsQRJ6s4MvTLyphLGr")
    alice = sp.test_account("Alice")

    metadata_uri = "ipfs://bafkreidfzvery2zn5en4w4o66sapvjt6vrmsojpr6o4o73a667f5f6f3re"
    contract_metadata = sp.scenario_utils.metadata_of_url(metadata_uri)

    c = my_module.GenerativeFA2(ADMIN_REAL, contract_metadata)
    scenario += c

    # Mint 10 tokens
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

    # Show token params for all 10 tokens
    scenario.show(c.get_token_params(0))
    scenario.show(c.get_token_params(1))
    scenario.show(c.get_token_params(2))
    scenario.show(c.get_token_params(3))
    scenario.show(c.get_token_params(4))
    scenario.show(c.get_token_params(5))
    scenario.show(c.get_token_params(6))
    scenario.show(c.get_token_params(7))
    scenario.show(c.get_token_params(8))
    scenario.show(c.get_token_params(9))

    # Update artist intent
    c.update_artist_intent(
        key="intent_cid",
        value_bool=False,
        value_string="ipfs://bafkreid4bjhylhm5xe6d3c5tzojoq3czzxvisbjbq7xnntcfwttr3in24u",
        value_list=[],
        _sender=ADMIN_REAL,
    )
    c.update_artist_intent(
        key="allowed_migrations",
        value_bool=False,
        value_string="",
        value_list=[
            "browser emulation",
            "runtime migration",
            "code adaptation preserving behaviour",
        ],
        _sender=ADMIN_REAL,
    )

    c.update_artist_intent(
        key="forbidden_actions",
        value_bool=False,
        value_string="",
        value_list=[
            "changing_seed",
            "changing_mode",
            "changing_identity_parameters",
            "removing_interactivity",
            "static_capture_as_canonical",
            "unregistered_renderer_override",
        ],
        _sender=ADMIN_REAL,
    )

    c.update_artist_intent(
        key="authenticity_rule",
        value_bool=False,
        value_string="seed_must_match",
        value_list=[],
        _sender=ADMIN_REAL,
    )

    # Invalid action codes are rejected on-chain.
    c.update_artist_intent(
        key="forbidden_actions",
        value_bool=False,
        value_string="",
        value_list=["removal of interactivity"],
        _sender=ADMIN_REAL,
        _valid=False,
        _exception="BAD_FORBIDDEN_ACTION",
    )

    # Inspect the intent history log built by the above 4 valid updates.
    scenario.show(c.data.intent_history)
    scenario.verify(c.data.intent_version == 4)

    # --- Per-token renderer provenance ---
    # Register the immutable original renderer for token 0.
    c.register_original_renderer(
        token_id=0,
        renderer_hash=sp.bytes("0x1a2b3c4d5e6f"),
        renderer_cid="ipfs://bafkreirendererv0placeholder",
        note="Original Three.js renderer for token 0.",
        _sender=ADMIN_REAL,
    )
    scenario.verify(c.data.renderer_original_hash.contains(0))
    scenario.verify(c.data.renderer_version_count[0] == 1)
    scenario.verify(c.data.renderer_canonical_version[0] == 0)
    scenario.show(c.get_renderer_original_hash(0))

    # The original renderer for the same token cannot be overwritten.
    c.register_original_renderer(
        token_id=0,
        renderer_hash=sp.bytes("0xdeadbeef"),
        renderer_cid="ipfs://should-not-be-accepted",
        note="Attempted overwrite",
        _sender=ADMIN_REAL,
        _valid=False,
        _exception="ORIGINAL_ALREADY_SET",
    )

    # A different token has an independent renderer lineage.
    c.register_original_renderer(
        token_id=1,
        renderer_hash=sp.bytes("0x010203040506"),
        renderer_cid="ipfs://bafkreirenderertoken1v0placeholder",
        note="Original Three.js renderer for token 1.",
        _sender=ADMIN_REAL,
    )
    scenario.verify(c.data.renderer_version_count[1] == 1)
    scenario.verify(c.data.renderer_canonical_version[1] == 0)

    # Register token 0 renderer v1; registration alone does not promote it.
    c.register_renderer_version(
        token_id=0,
        renderer_hash=sp.bytes("0x9f8e7d6c5b4a"),
        renderer_cid="ipfs://bafkreirendererv1placeholder",
        note="Migrated to WebGL2 runtime, behaviourally equivalent to v0.",
        _sender=ADMIN_REAL,
    )
    scenario.verify(c.data.renderer_version_count[0] == 2)
    scenario.verify(c.data.renderer_canonical_version[0] == 0)

    # Explicitly promote token 0 v1, then roll back to v0.
    c.set_canonical_renderer(token_id=0, version=1, _sender=ADMIN_REAL)
    scenario.verify(c.data.renderer_canonical_version[0] == 1)
    scenario.show(c.get_canonical_renderer(0))

    c.set_canonical_renderer(token_id=0, version=99, _sender=ADMIN_REAL, _valid=False, _exception="NO_SUCH_VERSION")

    c.set_canonical_renderer(token_id=0, version=0, _sender=ADMIN_REAL)
    scenario.verify(c.data.renderer_canonical_version[0] == 0)
    scenario.show(c.get_canonical_renderer(0))
    scenario.show(c.get_renderer_version(sp.record(token_id=0, version=1)))

    # --- Edition behaviour table (mode 0-9) ---
    edition_labels = [
        "Edition I", "Edition II", "Edition III", "Edition IV", "Edition V",
        "Edition VI", "Edition VII", "Edition VIII", "Edition IX", "Edition X",
    ]
    for i in range(10):
        c.set_edition_behaviour(
            mode=i,
            label=edition_labels[i],
            description_cid="ipfs://bafkreiedition%d" % i,
            _sender=ADMIN_REAL,
        )
    scenario.show(c.get_edition_behaviour(3))

    # --- Decentralized storage backups ---
    c.add_storage_backup(
        key="intent_cid",
        uri="ar://backup-arweave-uri-placeholder",
        _sender=ADMIN_REAL,
    )
    c.add_storage_backup(
        key="intent_cid",
        uri="https://gateway2.example/ipfs/bafkreidfzvery2zn5en4w4o66sapvjt6vrmsojpr6o4o73a667f5f6f3re",
        _sender=ADMIN_REAL,
    )
    scenario.show(c.data.storage_backups)

# ----------------------------------------------------------------
# COMPILATION TARGET
# ----------------------------------------------------------------
ADMIN_REAL = sp.address("tz1d7W6HtnRgNeDg4PtsQRJ6s4MvTLyphLGr")
CONTRACT_METADATA_URI = "ipfs://bafkreidfzvery2zn5en4w4o66sapvjt6vrmsojpr6o4o73a667f5f6f3re"


def _mk_contract():
    return my_module.GenerativeFA2(
        ADMIN_REAL,
        sp.scenario_utils.metadata_of_url(CONTRACT_METADATA_URI),
    )


_act = getattr(sp, "add_compilation_target", None)
if callable(_act):
    _scenario = sp.test_scenario()
    _c = _mk_contract()
    _scenario += _c
    _act("Ghostnet_GenerativeFA2", _c)
