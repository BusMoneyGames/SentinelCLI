import xxhash

import persistence


class ProcessingState(persistence.PersistentEntity):
    PENDING = 1
    PROCESSING = 2
    DONE = 3

    def __init__(self):
        super().__init__()
        self.name = None
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


class AssetHash(persistence.PersistentEntity):
    """
    A hash of the contents of an asset asset.
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
        self.asset_type_id: int = None
        self.processing_state_id: int = ProcessingState.PENDING
        self._hash: str = None
        super()._init_sql()

    def load_by_filename(self):
        self.id = self._fetch_one('select id from asset where filename = %s',
                                  (self.filename,))
        self.load()

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
        self._execute(sql, (self.id, asset_hash.id))

    def get_hash(self) -> str:
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
        return self._fetch_one(sql, (self.id,))


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

