from dataclasses import asdict
from typing import List, Type, TypeVar

T = TypeVar("T")
U = TypeVar("U")


def model_to_entity(model: T, entity_cls: Type[U]) -> U:
    """モデルからエンティティへの変換

    Parameters
    ----------
    model : T
        モデル
    entity_cls : Type[U]
        エンティティクラス

    Returns
    -------
    U
        エンティティ
    """
    model_dict = {c.name: getattr(model, c.name) for c in model.__table__.columns}
    return entity_cls(**model_dict)


def entity_to_model(entity: U, model_cls: Type[T]) -> T:
    """エンティティからモデルへの変換

    Parameters
    ----------
    entity : U
        エンティティ
    model_cls : Type[T]
        モデルクラス

    Returns
    -------
    T
        モデル
    """
    entity_dict = asdict(entity)
    return model_cls(**entity_dict)


def models_to_entities(models: List[T], entity_cls: Type[U]) -> List[U]:
    """複数のモデルからエンティティリストへの変換

    Parameters
    ----------
    models : List[T]
        モデル配列
    entity_cls : Type[U]
        エンティティクラス

    Returns
    -------
    List[U]
        エンティティ配列
    """
    return [model_to_entity(model, entity_cls) for model in models]


def entities_to_models(entities: List[U], model_cls: Type[T]) -> List[T]:
    """複数のエンティティからモデルリストへの変換

    Parameters
    ----------
    entities : List[U]
        クラス配列
    model_cls : Type[T]
        モデルクラス

    Returns
    -------
    List[T]
        モデル配列
    """
    return [entity_to_model(entity, model_cls) for entity in entities]
