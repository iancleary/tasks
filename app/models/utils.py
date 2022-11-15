import json
from typing import Any
from typing import Dict
from typing import List
from typing import Union

from sqlalchemy.orm.decl_api import DeclarativeMeta


# https://stackoverflow.com/a/10664192
def new_alchemy_encoder(
    revisit_self: bool = False, fields_to_expand: List[str] = []
) -> Any:
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj: object) -> Union[List[str], object]:
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if revisit_self:
                    if obj in _visited_objs:
                        return None
                    _visited_objs.append(obj)

                # go through each field in this SQLalchemy class
                fields: Dict[str, Any] = {}
                for field in [
                    x
                    for x in dir(obj)
                    if not x.startswith("_") and x != "metadata" and x != "registry"
                ]:
                    val = obj.__getattribute__(field)

                    # is this field another SQLalchemy object, or a list of SQLalchemy objects?
                    if isinstance(val.__class__, DeclarativeMeta) or (
                        isinstance(val, list)
                        and len(val) > 0
                        and isinstance(val[0].__class__, DeclarativeMeta)
                    ):
                        # unless we're expanding this field, stop here
                        if field not in fields_to_expand:
                            # not expanding this field: set it to None and continue
                            fields[field] = None
                            continue

                    fields[field] = val
                # a json-encodable dict
                return fields

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder
