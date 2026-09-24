from vestapol import external_tables


def test_get_external_data_configuration_default_ignore_unknown_values():
    external_config = external_tables.get_external_data_configuration(
        "gs://bucket/prefix/",
        ["gs://bucket/prefix/*/data.csv"],
        "csv",
    )

    assert external_config.ignore_unknown_values is False


def test_get_external_data_configuration_ignore_unknown_values_enabled():
    external_config = external_tables.get_external_data_configuration(
        "gs://bucket/prefix/",
        ["gs://bucket/prefix/*/data.csv"],
        "csv",
        ignore_unknown_values=True,
    )

    assert external_config.ignore_unknown_values is True


def test_get_external_data_configuration_ignore_unknown_values_jsonl():
    external_config = external_tables.get_external_data_configuration(
        "gs://bucket/prefix/",
        ["gs://bucket/prefix/*/data.json"],
        "jsonl",
        ignore_unknown_values=True,
    )

    assert external_config.ignore_unknown_values is True
