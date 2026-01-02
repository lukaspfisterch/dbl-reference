from ensdg.boundary import Boundary
from ensdg.example_rules import AcceptAll


def test_boundary_config_hash_is_stable():
    b1 = Boundary(1, AcceptAll()).config()
    b2 = Boundary(1, AcceptAll()).config()
    assert b1.boundary_config_hash == b2.boundary_config_hash
    assert b1.boundary_version == 1
