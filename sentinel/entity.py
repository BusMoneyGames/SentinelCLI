import xxhash

import persistence

db = persistence.Database()


class ProcessingState(persistence.PersistentEntity):
    PENDING = 1
    PROCESSING = 2
    DONE = 3

    def __init__(self):
        super().__init__()
        self.name = None
        super()._init_sql()


class RuleViolation(persistence.PersistentEntity):
    """
    An asset rule violation.
    """

    def __init__(self):
        super().__init__()
        self.rule_name = None
        self.rule = None
        self.reason = None
        super()._init_sql()


class AssetType(persistence.PersistentEntity):
    """
    The type of a game asset. The type is contained in this class instead
    of creating a separate class for each asset type to allow for handling
    of future unknown asset types.
    """

    def __init__(self):
        super().__init__()
        self.name = None
        super()._init_sql()

    def load_by_name(self):
        self.id = db.fetch_one('select id from asset_type where name = %s',
                               (self.name,))[0]
        self.load()


class AssetHash(persistence.PersistentEntity):
    """
    A hash of the contents of an asset file.
    """

    def __init__(self):
        super().__init__()
        self.value = None
        super()._init_sql()


class Asset(persistence.PersistentEntity):
    """
    A game asset like a texture or model.
    """

    def __init__(self):
        super().__init__()
        self.name: str = None
        self.filename: str = None
        self.type_id: int = None
        self.processing_state_id: int = ProcessingState.PENDING
        self._hash: str = None
        super()._init_sql()

    def load_by_filename(self):
        self.id = db.fetch_one('select id from asset where filename = %s',
                               (self.filename,))[0]
        self.load()

    def set_type(self, asset_type: AssetType):
        self.type_id = asset_type.id

    def set_processing_state(self, state_id: int):
        self.processing_state_id = state_id

    def generate_and_save_hash(self):
        fhash = xxhash.xxh64()
        with open(self.filename, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                fhash.update(chunk)
        asset_hash = AssetHash()
        self._hash = fhash.hexdigest()
        asset_hash.value = self._hash
        asset_hash.save()
        self.link_asset_hash(asset_hash)

    def link_asset_hash(self, asset_hash):
        sql = """
            insert into asset_to_asset_hash(asset_id, asset_hash_id)
            values (%s, %s)
            """
        db.execute(sql, (self.id, asset_hash.id))

    def get_hash(self):
        if self._hash:
            return self._hash

        sql = """
            select ah.value
            from asset_hash ah,
              asset_to_asset_hash atah
            where atah.asset_id = %s
              and atah.asset_hash_id = ah.id
            order by ah.id desc
            limit 1
            """
        row = db.fetch_one(sql, (self.id,))
        if row:
            return row[0]
        else:
            return None

    def add_rule_violation(self, rule_violation: RuleViolation):
        sql = """
            insert into asset_to_rule_violation(asset_id, rule_violation_id)
            values (%s, %s)
            """
        db.execute(sql, (self.id, rule_violation.id))

    def get_rule_violations(self):
        rule_violations = []

        sql = """
            select rule_violation_id
            from asset_to_rule_violation
            where asset_id = %s
            """
        rows = db.fetch_all(sql, (self.id,))
        if rows:
            for row in rows:
                rv = RuleViolation()
                rv.id = row[0]
                rv.load()
                rule_violations.append(rv)

        return rule_violations
