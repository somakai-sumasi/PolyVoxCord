from dataclasses import asdict
from typing import List, Type, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def model_to_entity(model: T, entity_cls: Type[U]) -> U:
    model_dict = {c.name: getattr(model, c.name) for c in model.__table__.columns}
    return entity_cls(**model_dict)


def entity_to_model(entity: U, model_cls: Type[T]) -> T:
    entity_dict = asdict(entity)
    return model_cls(**entity_dict)


# 複数のモデルからエンティティリストへの変換
def models_to_entities(models: List[T], entity_cls: Type[U]) -> List[U]:
    return [model_to_entity(model, entity_cls) for model in models]


# 複数のエンティティからモデルリストへの変換
def entities_to_models(entities: List[U], model_cls: Type[T]) -> List[T]:
    return [entity_to_model(entity, model_cls) for entity in entities]
