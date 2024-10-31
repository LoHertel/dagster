from collections import namedtuple
from typing import Sequence

from dagster import (
    AssetSpec,
    _check as check,
)

from dagster_tableau.translator import TableauTagSet


class ParsedTableauAssetSpecs(
    namedtuple("_ParsedTableauAssetSpecs", ["external_asset_specs", "materializable_asset_specs"])
):
    """Used to represent the parsed Tableau asset specs
    as returned by the `parse_tableau_external_and_materializable_asset_specs` function below.
    """

    def __new__(cls, external_asset_specs, materializable_asset_specs):
        return super(ParsedTableauAssetSpecs, cls).__new__(
            cls,
            external_asset_specs=check.list_param(
                external_asset_specs, "external_asset_specs", AssetSpec
            ),
            materializable_asset_specs=check.list_param(
                materializable_asset_specs, "materializable_asset_specs", AssetSpec
            ),
        )


def parse_tableau_external_and_materializable_asset_specs(
    specs: Sequence[AssetSpec],
) -> ParsedTableauAssetSpecs:
    external_asset_specs = [
        spec for spec in specs if TableauTagSet.extract(spec.tags).asset_type == "data_source"
    ]

    materializable_asset_specs = [
        spec
        for spec in specs
        if TableauTagSet.extract(spec.tags).asset_type in ["dashboard", "sheet"]
    ]

    return ParsedTableauAssetSpecs(
        external_asset_specs=external_asset_specs,
        materializable_asset_specs=materializable_asset_specs,
    )
