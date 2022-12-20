import dpdata

def test_load():
    s = dpdata.LabeledSystem("input.out", fmt="psi4")
    assert len(s) == 1
