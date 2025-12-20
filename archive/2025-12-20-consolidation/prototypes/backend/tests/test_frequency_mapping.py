from backend.logic.frequency_mapping import list_states, map_text_to_state


def test_load_mapping_has_16_states():
    states = list_states()
    assert len(states) == 16


def test_map_text_to_describe_dye_maps_to_confused():
    r = map_text_to_state("I'm just dye on the canvas, painting tonight")
    assert r["state_id"] in (5,)


def test_map_text_to_suicidal_phrase_maps_to_despair():
    r = map_text_to_state("I'm thinking about ending it")
    assert r["state_id"] == 15
