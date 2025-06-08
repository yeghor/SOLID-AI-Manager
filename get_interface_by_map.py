from base_interface import ModelInterface

def get_interface_by_map(model: str, model_map: dict[str, ModelInterface]):
    interface = model_map.get(model)
    if not interface:
        raise ValueError("This model is not implemented yet")
    return interface
