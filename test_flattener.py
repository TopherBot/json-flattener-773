import json
import pytest
from flattener import flatten, unflatten

sample = {
    "user": {
        "id": 1,
        "name": "Alice",
        "tags": ["admin", "dev"]
    },
    "active": True,
    "meta": None,
}

expected_flat = {
    "user.id": 1,
    "user.name": "Alice",
    "user.tags.0": "admin",
    "user.tags.1": "dev",
    "active": True,
    "meta": None,
}

def test_flatten():
    assert flatten(sample) == expected_flat

def test_unflatten():
    rebuilt = unflatten(expected_flat)
    assert rebuilt == sample

# Round‑trip property test
@given(
    data=st.recursive(
        st.none() | st.booleans() | st.integers() | st.floats(allow_nan=False) | st.text(),
        max_leaves=5,
    )
)
def test_round_trip(data):
    # json-serialisable check – skip non‑serialisable structures
    try:
        json.dumps(data)
    except TypeError:
        return
    flat = flatten(data)
    assert unflatten(flat) == data
